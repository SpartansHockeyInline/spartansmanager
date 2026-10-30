# Spartans Manager — istruzioni per Claude Code

Gestionale web (PWA) per ASD sportive, nato per ASD Spartans Hockey Inline e commercializzato ad altre associazioni. Versione corrente: v6.7.1. Il repository è **pubblico**: non committare mai segreti, dati di tesserati, chiavi di licenza reali o nominativi.

## Architettura (verificata sul codice)
- **Un solo file**: quasi tutto sta in `index.html` (~9.400 righe): HTML, CSS e un unico `<script>` principale (da riga ~2995). Nessun build, nessun bundler, nessun framework, nessun `package.json`.
- Moduli di stampa/contratto separati: `modulo_*.html` (iscrizione, ricevuta, fattura sponsor, contratto sponsor, co.co.co., verbale CD, ecc.). Ricevono i dati come parametri dall'app (es. `asdPec`).
- Pagine = sezioni `id="page-<nome>"` mostrate da `showPage()`.
- Stato globale: oggetto `DB` (soci, staff, corsi, abbonamenti, entrate/uscite, eventi, presenze, struttura, ...).
- Persistenza: `saveDB()` → `localStorage['spartans_db']` + `driveScheduleSave()` → Firebase Realtime Database (`spartans/data`, scritto con `set()` sull'intero DB). Backup automatici in `spartans/backupsAutomatici`. Contatori fattura/XML in `spartans/contatori/...`.
- Firebase (SDK 10.12 compat da CDN) con login Google. Esiste un utente demo (`DEMO_UID`, `_isDemo`) in sola lettura: **ogni funzione di salvataggio deve iniziare con il controllo `_isDemo`**, come le `save*()` esistenti.
- `.github/scripts/sync_calendario.py` + workflow `sync-calendario.yml`: sincronizza gli eventi con Google Calendar (cron orario). Python 3.12, secrets `FIREBASE_SA_JSON` e `GOOGLE_SA_JSON`. Log pubblici: stampare solo conteggi, mai nomi/titoli.
- Deploy: GitHub Pages (`/spartansmanager/`).

## Regole di modifica
1. **Modifiche minime e mirate.** Non riformattare né spostare blocchi di `index.html`; non estrarre moduli senza richiesta esplicita. Il file è grande: leggere solo la funzione interessata (`grep -n "function nome"`), mai l'intero file.
2. **Non rompere il formato dati.** `DB` vive già nei browser e su Firebase degli utenti: nuovi campi devono avere un default e funzionare con dati vecchi (vedi `riparaPresenzeOrphane`, `riparaTipologieMancanti`). Mai rinominare/eliminare campi esistenti senza una migrazione.
3. **Mai scritture massive non richieste su `spartans/data`.** `set()` sovrascrive tutto il database: ogni modifica a quel flusso va discussa prima.
4. **Date**: usare `oggiLocale()` e `_giorniA()` (data locale italiana). Non usare `new Date('YYYY-MM-DD')` né `toISOString()` per "oggi" o per giorni alla scadenza (bug già corretto in v6.6.0).
5. **Sicurezza/XSS**: l'app usa molto `innerHTML` con dati inseriti dagli utenti. Nel nuovo codice o nel codice toccato, escapare i valori inseriti dall'utente prima di inserirli in HTML; non introdurre `eval` o handler costruiti da stringhe utente.
6. **Dati personali** (anche di minori, dati sanitari, CF, documenti): non finiscono in log, titoli del calendario, messaggi di commit, esempi o test. Nei test usare dati inventati.
7. **Fatturazione elettronica** (`generaXmlFatturaPA`, `validaFatturaXml`) e contratti: modificare solo se richiesto, perché hanno valore fiscale/legale.
8. Niente nuove dipendenze o CDN senza motivo e senza chiederlo.

## Versione e changelog
Per ogni rilascio aggiornare **tutti** questi punti: `APP_VERSION` (inizio script), footer `#app-footer`, voce nel modal changelog (`cl-ver`), `CURRENT_VER` (~riga 9102), `CHANGELOG.md`, e la Guida in-app se cambia un flusso utente. Messaggio di commit nello stile esistente: `v6.7.1: <sintesi in italiano>`.

## Come verificare (non esistono test automatici)
- Aprire `index.html` in un browser (meglio `python3 -m http.server`, poi `http://localhost:8000/`) e provare il flusso toccato, con l'utente demo o dati finti. Controllare la console del browser: nessun errore.
- Per lo script Python: eseguire con `SIMULA=1` (non scrive nulla) prima di qualunque modifica reale.
- Prima di dichiarare finito un lavoro: rileggere il diff (`git diff`), cercare errori di sintassi JS, verificare che le funzioni `save*()` abbiano il controllo `_isDemo`.
- Test automatici: non obbligatori. Se ne aggiungono, che siano E2E con Playwright sui flussi critici (iscrizione, ricevuta, fattura sponsor, presenze) e senza toccare Firebase reale. Nessuna soglia di copertura: il progetto non ha test e non va cambiato in massa.

## Cose da non fare
- Non committare `licenze.json` con chiavi reali (oggi contiene solo una chiave di test), né credenziali o token (`wa_api_token`, chiavi di account di servizio).
- Non modificare `.github/workflows/` o i secrets senza richiesta esplicita.
- Non fare push su `main` senza richiesta: lavorare su un branch.
