#!/usr/bin/env python3
"""Sincronizza gli eventi di Spartans Manager con un calendario Google (a senso unico: app -> calendario).

Legge da Firebase (account di servizio in SOLA LETTURA) gli eventi e le impostazioni di "La mia struttura",
poi allinea il calendario Google (account di servizio con permesso "Apporta modifiche agli eventi").

Principi:
  * Ogni evento Google ha un id DERIVATO da quello dell'app (gli allenamenti automatici, che l'app rigenera
    con id nuovi a ogni modifica del corso, da corso+data+ora): niente stato da conservare, il job e' idempotente.
  * Il job tocca SOLO gli eventi che ha creato (marcati con extendedProperties.private.spartans=1).
  * Non cancella mai eventi gia' passati (la storia resta nel calendario anche dopo la chiusura stagione).
  * Valvola di sicurezza: se il database sembra vuoto o le cancellazioni sono troppe, si ferma.
  * Il repository e' PUBBLICO e i log delle Actions sono pubblici: qui si stampano solo conteggi, mai titoli,
    note, nomi o l'id del calendario.

Variabili d'ambiente:
  FIREBASE_SA_JSON  chiave dell'account di servizio con ruolo di sola lettura sul Realtime Database
  GOOGLE_SA_JSON    chiave dell'account di servizio con accesso al calendario
  FIREBASE_DB_URL   indirizzo del Realtime Database (non segreto)
  SIMULA=1          non scrive nulla: mostra solo cosa farebbe
  FORZA=1           salta la valvola di sicurezza (solo dopo aver capito perche' scatta)
"""
import os, re, sys, json, time, base64, hashlib, datetime as dt
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROMA = 'Europe/Rome'
CAL_API = 'https://www.googleapis.com/calendar/v3/calendars/{cal}/events'
PAUSA = 0.25  # secondi tra una scrittura e l'altra (Google limita le scritture ravvicinate)

# colore (colorId di Google Calendar), durata predefinita di un evento con orario, promemoria.
TIPI = {
    'gara':        {'ico': '⚔️', 'colore': '11', 'durata': 120},
    'allenamento': {'ico': '🏒', 'colore': '9',  'durata': 90},
    'attivita':    {'ico': '📌', 'colore': '5',  'durata': 60},
    'scadenza':    {'ico': '⏰', 'colore': '6',  'durata': 30},
}
TIPI_PREDEFINITI = {k: True for k in TIPI}


def oggi_roma():
    return dt.datetime.now(ZoneInfo(ROMA)).date()


def tipo_effettivo(e):
    """Un tipo sconosciuto (dati vecchi) si tratta come attivita', come fa l'app per l'aspetto neutro."""
    return e.get('tipo') if e.get('tipo') in TIPI else 'attivita'


def id_google(chiave):
    """Id evento valido per Google (solo a-v e 0-9, 5-1024 caratteri), stabile per la stessa chiave."""
    h = hashlib.sha1(chiave.encode('utf-8')).digest()
    return 'sm' + base64.b32hexencode(h).decode().lower().rstrip('=')


def chiave_evento(e):
    if e.get('autoCorsoId'):
        return f"a|{e['autoCorsoId']}|{e.get('data', '')}|{e.get('ora', '')}"
    return f"e|{e.get('id', '')}"


def promemoria(tipo, tutto_il_giorno, fatto):
    """Promemoria in minuti prima dell'inizio. Per i giorni interi: ore 09:00 del giorno (inizio = 00:00)."""
    if fatto or tipo == 'allenamento':
        return {'useDefault': False, 'overrides': []}
    giorno = lambda n: (n * 1440 - 540) if tutto_il_giorno else n * 1440  # n giorni prima (09:00 se tutto il giorno)
    if tipo == 'scadenza':
        o = [('popup', giorno(7)), ('popup', giorno(1)), ('email', giorno(1))]
    else:
        o = [('popup', giorno(1))]
    return {'useDefault': False, 'overrides': [{'method': m, 'minutes': mi} for m, mi in o]}


def costruisci(e):
    """Corpo dell'evento Google a partire da un evento dell'app, o None se la data non e' valida."""
    data = str(e.get('data') or '')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', data):
        return None
    try:
        giorno = dt.date.fromisoformat(data)
    except ValueError:
        return None
    tipo = tipo_effettivo(e)
    t = TIPI[tipo]
    fatto = bool(e.get('fatto'))
    titolo = str(e.get('titolo') or '(senza titolo)')
    summary = ('✓ ' if fatto else '') + f"{t['ico']} {titolo}"
    righe = []
    if e.get('squadraNome'):
        righe.append(f"Squadra: {e['squadraNome']}")
    if e.get('note'):
        righe.append(str(e['note']))
    righe.append('— Gestito da Spartans Manager: le modifiche fatte qui vengono sovrascritte.')
    m = re.fullmatch(r'(\d{1,2}):(\d{2})', str(e.get('ora') or '').strip())
    corpo = {'summary': summary, 'description': '\n'.join(righe), 'colorId': '8' if fatto else t['colore']}
    if e.get('luogo'):
        corpo['location'] = str(e['luogo'])
    if m and int(m.group(1)) < 24 and int(m.group(2)) < 60:
        inizio = dt.datetime.combine(giorno, dt.time(int(m.group(1)), int(m.group(2))))
        fine = inizio + dt.timedelta(minutes=t['durata'])
        corpo['start'] = {'dateTime': inizio.isoformat(), 'timeZone': ROMA}
        corpo['end'] = {'dateTime': fine.isoformat(), 'timeZone': ROMA}
        tutto = False
    else:
        corpo['start'] = {'date': data}
        corpo['end'] = {'date': (giorno + dt.timedelta(days=1)).isoformat()}
        tutto = True
    corpo['reminders'] = promemoria(tipo, tutto, fatto)
    if tipo in ('scadenza', 'attivita') or fatto:
        corpo['transparency'] = 'transparent'
    return corpo


def impronta(corpo):
    return hashlib.sha1(json.dumps(corpo, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:16]


def calcola_desiderati(eventi, tipi):
    """{id_google: corpo} per gli eventi dei tipi abilitati. Ritorna anche i conteggi per tipo e gli scartati."""
    desiderati, per_tipo, scartati = {}, {}, 0
    for e in eventi:
        if not isinstance(e, dict):
            continue
        tipo = tipo_effettivo(e)
        if not tipi.get(tipo, False):
            continue
        corpo = costruisci(e)
        if corpo is None:
            scartati += 1
            continue
        gid = id_google(chiave_evento(e))
        corpo['extendedProperties'] = {'private': {'spartans': '1', 'h': impronta(corpo)}}
        desiderati[gid] = corpo
        per_tipo[tipo] = per_tipo.get(tipo, 0) + 1
    return desiderati, per_tipo, scartati


# ───────────────────────── Google Calendar ─────────────────────────
def _motivo(r):
    try:
        return r.json()['error']['errors'][0]['reason']
    except Exception:
        return ''


def chiama(sess, metodo, url, **kw):
    """Richiesta con nuovi tentativi (attesa crescente) sugli errori temporanei e sui limiti di frequenza."""
    r = None
    for tentativo in range(6):
        r = getattr(sess, metodo)(url, **kw)
        limite = r.status_code == 403 and _motivo(r) in ('rateLimitExceeded', 'userRateLimitExceeded', 'quotaExceeded')
        if r.status_code in (429, 500, 502, 503, 504) or limite:
            time.sleep(min(2 ** tentativo, 32) * (PAUSA > 0))
            continue
        return r
    return r


def errore(r, cosa):
    try:
        msg = r.json().get('error', {}).get('message', '')
    except Exception:
        msg = ''
    aiuto = {403: "l'API Google Calendar non e' abilitata o il calendario non e' condiviso con l'account di servizio ('Apporta modifiche agli eventi')",
             404: "id del calendario errato o calendario non condiviso con l'account di servizio",
             401: "chiave dell'account di servizio non valida"}.get(r.status_code, '')
    sys.exit(f'Google Calendar: {cosa} ha risposto {r.status_code} {msg}. {aiuto}'.strip())


def elenca(sess, cal):
    """Eventi creati da questo job: {id: evento}."""
    url, esistenti, token = CAL_API.format(cal=quote(cal, safe='')), {}, None
    while True:
        params = {'privateExtendedProperty': 'spartans=1', 'maxResults': 2500, 'showDeleted': 'false'}
        if token:
            params['pageToken'] = token
        r = chiama(sess, 'get', url, params=params)
        if r.status_code >= 300:
            errore(r, "l'elenco degli eventi")
        j = r.json()
        for ev in j.get('items', []):
            if ev.get('status') != 'cancelled':
                esistenti[ev['id']] = ev
        token = j.get('nextPageToken')
        if not token:
            return esistenti


def data_inizio(ev):
    s = ev.get('start', {})
    return (s.get('date') or s.get('dateTime') or '')[:10]


def piano(esistenti, desiderati, oggi):
    creare = [g for g in desiderati if g not in esistenti]
    aggiornare = [g for g, c in desiderati.items()
                  if g in esistenti and esistenti[g].get('extendedProperties', {}).get('private', {}).get('h') != c['extendedProperties']['private']['h']]
    # mai cancellare il passato: un evento non piu' nell'app resta se e' gia' avvenuto
    eliminare = [g for g, ev in esistenti.items() if g not in desiderati and data_inizio(ev) >= oggi.isoformat()]
    invariati = len(desiderati) - len(creare) - len(aggiornare)
    return creare, aggiornare, eliminare, invariati


def valvola(esistenti, desiderati, eliminare, forza):
    """Ferma il job se i numeri non tornano (database letto vuoto, eventi spariti per errore...)."""
    if forza:
        return
    if not desiderati and len(esistenti) > 10:
        sys.exit(f"STOP di sicurezza: nessun evento da sincronizzare ma nel calendario ce ne sono {len(esistenti)} creati dall'app. "
                 "Se e' voluto, rilancia con FORZA=1.")
    if len(eliminare) > max(25, len(esistenti) // 2):
        sys.exit(f"STOP di sicurezza: dovrei eliminare {len(eliminare)} eventi su {len(esistenti)}. "
                 "Se e' voluto, rilancia con FORZA=1.")


def scrivi(sess, cal, gid, corpo, nuovo):
    base = CAL_API.format(cal=quote(cal, safe=''))
    if nuovo:
        r = chiama(sess, 'post', base, json={**corpo, 'id': gid})
        if r.status_code != 409:
            if r.status_code >= 300:
                errore(r, 'la creazione')
            return
        # 409: l'id esiste gia' (un evento cancellato in passato): lo si ripristina con i dati nuovi
    r = chiama(sess, 'patch', f'{base}/{gid}', json={**corpo, 'status': 'confirmed'})
    if r.status_code >= 300:
        errore(r, "l'aggiornamento")


def elimina(sess, cal, gid):
    r = chiama(sess, 'delete', f"{CAL_API.format(cal=quote(cal, safe=''))}/{gid}")
    if r.status_code >= 300 and r.status_code not in (404, 410):
        errore(r, "l'eliminazione")


def sincronizza(sess, cal, eventi, tipi, oggi, simula=False, forza=False):
    desiderati, per_tipo, scartati = calcola_desiderati(eventi, tipi)
    esistenti = elenca(sess, cal)
    creare, aggiornare, eliminare, invariati = piano(esistenti, desiderati, oggi)
    valvola(esistenti, desiderati, eliminare, forza)
    if not simula:
        for g in creare:
            scrivi(sess, cal, g, desiderati[g], True)
            time.sleep(PAUSA)
        for g in aggiornare:
            scrivi(sess, cal, g, desiderati[g], False)
            time.sleep(PAUSA)
        for g in eliminare:
            elimina(sess, cal, g)
            time.sleep(PAUSA)
    return {'desiderati': len(desiderati), 'per_tipo': per_tipo, 'scartati': scartati, 'esistenti': len(esistenti),
            'creati': len(creare), 'aggiornati': len(aggiornare), 'eliminati': len(eliminare), 'invariati': invariati}


# ───────────────────────── Firebase ─────────────────────────
def normalizza_lista(v):
    """Firebase restituisce gli array come lista (con eventuali None) o come dizionario di indici."""
    if v is None:
        return []
    if isinstance(v, dict):
        v = list(v.values())
    return [x for x in v if isinstance(x, dict)]


def leggi_firebase(sess, db_url):
    base = db_url.rstrip('/') + '/spartans/data/'
    out = {}
    for nome in ('struttura', 'eventi'):
        r = chiama(sess, 'get', base + nome + '.json')
        if r.status_code >= 300:
            sys.exit(f'Firebase ha risposto {r.status_code} leggendo "{nome}". Controlla FIREBASE_DB_URL e che '
                     "l'account di servizio abbia il ruolo di lettura sul Realtime Database.")
        out[nome] = r.json()
    return out['struttura'] or {}, normalizza_lista(out['eventi'])


def impostazioni(struttura):
    tipi = dict(TIPI_PREDEFINITI)
    if isinstance(struttura.get('gcalTipi'), dict):
        tipi.update({k: bool(v) for k, v in struttura['gcalTipi'].items() if k in TIPI})
    return bool(struttura.get('gcalAttivo')), str(struttura.get('gcalId') or '').strip(), tipi


def main():
    raw_fb, raw_g = os.environ.get('FIREBASE_SA_JSON', '').strip(), os.environ.get('GOOGLE_SA_JSON', '').strip()
    db_url = os.environ.get('FIREBASE_DB_URL', '').strip()
    simula, forza = os.environ.get('SIMULA') == '1', os.environ.get('FORZA') == '1'
    if not raw_fb or not raw_g or not db_url:
        print('Sincronizzazione non configurata: mancano i Secrets FIREBASE_SA_JSON / GOOGLE_SA_JSON o FIREBASE_DB_URL. Nessuna azione.')
        return
    try:
        info_fb, info_g = json.loads(raw_fb), json.loads(raw_g)
    except ValueError:
        sys.exit('Uno dei due Secrets non e\' un JSON valido: incolla l\'intero contenuto del file scaricato.')
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    s_fb = AuthorizedSession(service_account.Credentials.from_service_account_info(
        info_fb, scopes=['https://www.googleapis.com/auth/firebase.database', 'https://www.googleapis.com/auth/userinfo.email']))
    struttura, eventi = leggi_firebase(s_fb, db_url)
    attivo, cal, tipi = impostazioni(struttura)
    if not attivo:
        print("Sincronizzazione disattivata in 'La mia struttura'. Nessuna azione.")
        return
    if not cal:
        sys.exit("Sincronizzazione attiva ma manca l'ID del calendario in 'La mia struttura'.")
    s_g = AuthorizedSession(service_account.Credentials.from_service_account_info(
        info_g, scopes=['https://www.googleapis.com/auth/calendar']))
    res = sincronizza(s_g, cal, eventi, tipi, oggi_roma(), simula, forza)
    print(('SIMULAZIONE (nessuna scrittura) - ' if simula else '') + 'eventi nell\'app: %d | da sincronizzare: %d (%s) | scartati per data non valida: %d'
          % (len(eventi), res['desiderati'], ', '.join(f'{k}: {v}' for k, v in sorted(res['per_tipo'].items())) or 'nessuno', res['scartati']))
    print('nel calendario: %d | creati: %d | aggiornati: %d | eliminati: %d | invariati: %d'
          % (res['esistenti'], res['creati'], res['aggiornati'], res['eliminati'], res['invariati']))


if __name__ == '__main__':
    main()
