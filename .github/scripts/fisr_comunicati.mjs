// Scarica i comunicati ufficiali FISR (generali e campionati) e li salva in fisr-comunicati.json,
// il file che l'app legge al posto dei proxy CORS pubblici (ormai a pagamento o fuori servizio).
//
// - Il parser e' QUELLO DELL'APP: viene estratto da index.html (parseComunicatiFisr), cosi' c'e' una
//   sola logica da mantenere. Se l'estrazione fallisce il job si ferma con un errore chiaro.
// - Le stagioni si scoprono dalle pagine indice del sito: una nuova stagione compare da sola.
// - Ogni giro rilegge le 2 stagioni piu' recenti di ogni categoria, oltre a quelle mai scaricate.
// - Il file viene riscritto SOLO se i dati cambiano (niente commit inutili); "aggiornato" e' l'ultima novita'.
// - Nessun dato personale: sono comunicati pubblici della federazione.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { setTimeout as pausa } from 'node:timers/promises';

const BASE = (process.env.FISR_BASE || 'https://www.fisr.it').replace(/\/$/, '');
const USCITA = process.env.FISR_OUT || 'fisr-comunicati.json';
const INDEX_HTML = process.env.FISR_INDEX_HTML || 'index.html';
const PAUSA_MS = process.env.FISR_PAUSA_MS !== undefined ? Number(process.env.FISR_PAUSA_MS) : 1000;
const SEMPRE_AGGIORNATE = 2;
const CATEGORIE = {
  generali: '/hockey-inline/comunicati-ufficiali.html',
  campionati: '/hockey-inline/comunicati-uff-campionati.html',
};
const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml',
  'Accept-Language': 'it-IT,it;q=0.9',
};

// ───────── parser dell'app ─────────
export function caricaParser(percorsoIndex = INDEX_HTML) {
  const s = readFileSync(percorsoIndex, 'utf8');
  const i = s.indexOf('function parseComunicatiFisr(');
  if (i < 0) throw new Error('parseComunicatiFisr non trovata in ' + percorsoIndex);
  let j = s.indexOf('{', i), d = 0, k = j;
  for (; k < s.length; k++) {
    if (s[k] === '{') d++;
    else if (s[k] === '}') { d--; if (d === 0) break; }
  }
  if (d !== 0) throw new Error('parseComunicatiFisr: parentesi non bilanciate');
  return new Function(s.slice(i, k + 1) + '\nreturn parseComunicatiFisr;')();
}

// ───────── rete ─────────
async function scarica(url) {
  let ultimo;
  for (let t = 1; t <= 3; t++) {
    try {
      const r = await fetch(url, { headers: HEADERS, signal: AbortSignal.timeout(30000), redirect: 'follow' });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.text();
    } catch (e) {
      ultimo = e;
      if (t < 3) await pausa(PAUSA_MS * t * 2);
    }
  }
  throw new Error(`${url}: ${ultimo.message}`);
}

// "621-2026-27" -> "2026-27"; "406-2020-2021" -> "2020-21"; "471-hil-22-23" -> "2022-23"
export function chiaveStagione(slug) {
  let m = slug.match(/(20\d{2})-(\d{2,4})/);
  if (m) return `${m[1]}-${m[2].slice(-2)}`;
  m = slug.match(/(\d{2})-(\d{2})/);
  return m ? `20${m[1]}-${m[2]}` : null;
}

export function scopriStagioni(htmlIndice) {
  const trovate = {};
  const re = /href="([^"#?]*\/category\/\d+-([^"#?]*)\.html)"/gi;
  let m;
  while ((m = re.exec(htmlIndice)) !== null) {
    const chiave = chiaveStagione(m[2]);
    if (!chiave || trovate[chiave]) continue;
    trovate[chiave] = m[1].startsWith('http') ? m[1] : BASE + m[1];
  }
  return trovate;
}

const ordinaDesc = (o) => Object.fromEntries(Object.entries(o).sort(([a], [b]) => b.localeCompare(a)));
const senzaData = (d) => JSON.stringify({ ...d, aggiornato: undefined });

async function main() {
  const parse = caricaParser();
  const prima = existsSync(USCITA) ? JSON.parse(readFileSync(USCITA, 'utf8')) : { versione: 1, generali: {}, campionati: {} };
  const dopo = { versione: 1, aggiornato: prima.aggiornato, generali: {}, campionati: {} };
  let scaricate = 0, fallite = 0;

  for (const [cat, pathIndice] of Object.entries(CATEGORIE)) {
    let stagioni;
    try {
      stagioni = scopriStagioni(await scarica(BASE + pathIndice));
    } catch (e) {
      console.warn(`[${cat}] pagina indice non raggiungibile: ${e.message}`);
      fallite++;
      dopo[cat] = prima[cat] || {};
      continue;
    }
    if (!Object.keys(stagioni).length) {
      console.warn(`[${cat}] nessuna stagione trovata nella pagina indice: conservo i dati precedenti`);
      fallite++;
      dopo[cat] = prima[cat] || {};
      continue;
    }
    const chiavi = Object.keys(stagioni).sort((a, b) => b.localeCompare(a));
    for (const [idx, chiave] of chiavi.entries()) {
      const vecchia = prima[cat]?.[chiave];
      const daLeggere = idx < SEMPRE_AGGIORNATE || !vecchia;
      if (!daLeggere) { dopo[cat][chiave] = vecchia; continue; }
      try {
        await pausa(PAUSA_MS);
        const comunicati = parse(await scarica(stagioni[chiave]));
        scaricate++;
        if (!comunicati.length && vecchia?.comunicati?.length) {
          console.warn(`[${cat} ${chiave}] 0 comunicati letti (prima ${vecchia.comunicati.length}): conservo i dati precedenti`);
          dopo[cat][chiave] = vecchia;
        } else {
          dopo[cat][chiave] = { url: stagioni[chiave], comunicati };
          console.log(`[${cat} ${chiave}] ${comunicati.length} comunicati`);
        }
      } catch (e) {
        fallite++;
        console.warn(`[${cat} ${chiave}] ${e.message}${vecchia ? ': conservo i dati precedenti' : ''}`);
        if (vecchia) dopo[cat][chiave] = vecchia;
      }
    }
    // stagioni non piu' elencate dal sito: restano quelle gia' note
    for (const [k, v] of Object.entries(prima[cat] || {})) if (!dopo[cat][k]) dopo[cat][k] = v;
    dopo[cat] = ordinaDesc(dopo[cat]);
  }

  if (scaricate === 0) {
    console.error('Nessuna pagina FISR scaricata: sito non raggiungibile da qui o struttura cambiata.');
    process.exit(1);
  }
  if (senzaData(dopo) === senzaData(prima)) {
    console.log(`Nessuna novita' (${scaricate} pagine controllate, ${fallite} errori): file invariato.`);
    return;
  }
  dopo.aggiornato = new Date().toISOString();
  writeFileSync(USCITA, JSON.stringify(dopo, null, 1) + '\n');
  console.log(`Scritto ${USCITA}: ${scaricate} pagine scaricate, ${fallite} errori.`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((e) => { console.error(e.message); process.exit(1); });
}
