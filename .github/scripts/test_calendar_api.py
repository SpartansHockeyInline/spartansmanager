#!/usr/bin/env python3
"""Prova: scrivere eventi nel Google Calendar dell'associazione con un account di servizio.

Nessun invito via email: l'account di servizio (quello gia' usato da Firebase) ha il calendario
condiviso con permesso "Apporta modifiche agli eventi" e usa l'API di Google Calendar.

FASE=crea      -> crea A (tutto il giorno) e B (10:00-11:00 ora di Roma), tra due giorni
FASE=aggiorna  -> rinomina A "(AGGIORNATO)" e sposta B alle 11:00
FASE=elimina   -> cancella A e B
SERIE (solo cifre) distingue una prova dall'altra; 'aggiorna' ed 'elimina' vogliono la stessa SERIE di 'crea'.

Variabili d'ambiente (mai stampate): GOOGLE_SA_JSON (chiave dell'account di servizio),
GMAIL_USER (indirizzo Gmail = id del calendario principale).
"""
import os, sys, json, datetime as dt
from urllib.parse import quote
from zoneinfo import ZoneInfo

API = 'https://www.googleapis.com/calendar/v3/calendars/{cal}/events'

def _url(cal):
    return API.format(cal=quote(cal, safe=''))  # l'indirizzo Gmail contiene '@': va codificato (%40)
ROMA = 'Europe/Rome'

def corpi(day, serie, fase):
    """Restituisce [(id_evento, corpo)] per la fase richiesta. Gli id usano solo a-v e 0-9 (regola di Google)."""
    d0, d1 = day.isoformat(), (day + dt.timedelta(days=1)).isoformat()
    aggiornato = fase == 'aggiorna'
    ora_b = 11 if aggiornato else 10
    a = {'summary': f'PROVA {serie} Spartans Manager - A tutto il giorno' + (' (AGGIORNATO)' if aggiornato else ''),
         'description': 'Evento di prova creato da Spartans Manager. Si puo eliminare.',
         'start': {'date': d0}, 'end': {'date': d1}, 'transparency': 'transparent',
         'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 900}]}}
    b = {'summary': f'PROVA {serie} Spartans Manager - B con orario',
         'description': 'Evento di prova creato da Spartans Manager. Si puo eliminare.',
         'start': {'dateTime': f'{d0}T{ora_b:02d}:00:00', 'timeZone': ROMA},
         'end': {'dateTime': f'{d0}T{ora_b + 1:02d}:00:00', 'timeZone': ROMA}, 'transparency': 'transparent',
         'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 60}]}}
    return [(f'prova{serie}a', a), (f'prova{serie}b', b)]

def scrivi(sess, cal, eid, corpo):
    """Crea l'evento; se esiste gia' (409) lo aggiorna. Ritorna la descrizione di cosa e' successo."""
    url = _url(cal)
    r = sess.post(url, json={**corpo, 'id': eid})
    if r.status_code == 409:
        r = sess.patch(f'{url}/{eid}', json=corpo)
        verbo = 'aggiornato'
    else:
        verbo = 'creato'
    if r.status_code >= 300:
        errore(r)
    return verbo

def cancella(sess, cal, eid):
    r = sess.delete(f'{_url(cal)}/{eid}')
    if r.status_code == 404 or r.status_code == 410:
        return 'gia assente'
    if r.status_code >= 300:
        errore(r)
    return 'eliminato'

def errore(r):
    try:
        msg = r.json().get('error', {}).get('message', r.text)
    except Exception:
        msg = r.text
    aiuto = {
        403: "403: l'API di Google Calendar non e' abilitata nel progetto, oppure il calendario non e' condiviso con l'account di servizio con permesso 'Apporta modifiche agli eventi'.",
        404: "404: indirizzo del calendario errato (GMAIL_USER) oppure calendario non condiviso con l'account di servizio.",
        401: '401: chiave dell\'account di servizio non valida.',
    }.get(r.status_code, '')
    sys.exit(f'Google Calendar ha risposto {r.status_code}: {msg}\n{aiuto}'.strip())

def main():
    fase = os.environ.get('FASE', 'crea')
    serie = os.environ.get('SERIE', '1').strip() or '1'
    if fase not in ('crea', 'aggiorna', 'elimina'):
        sys.exit(f'FASE non valida: {fase}')
    if not serie.isdigit() or len(serie) > 6:
        sys.exit('SERIE non valida: solo cifre (max 6).')
    cal = os.environ.get('GMAIL_USER', '').strip()
    raw = os.environ.get('GOOGLE_SA_JSON', '').strip()
    if not cal or not raw:
        sys.exit('Mancano i Secrets GMAIL_USER e/o GOOGLE_SA_JSON.')
    try:
        info = json.loads(raw)
    except ValueError:
        sys.exit('GOOGLE_SA_JSON non e\' un JSON valido: incolla l\'intero contenuto del file scaricato da Firebase.')
    if info.get('type') != 'service_account':
        sys.exit("GOOGLE_SA_JSON non e' una chiave di account di servizio.")
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    creds = service_account.Credentials.from_service_account_info(info, scopes=['https://www.googleapis.com/auth/calendar'])
    sess = AuthorizedSession(creds)
    print(f"account di servizio: {info.get('client_email', '?')}")  # e' un indirizzo, non un segreto: serve per la condivisione
    day = dt.datetime.now(ZoneInfo(ROMA)).date() + dt.timedelta(days=2)
    for eid, corpo in corpi(day, serie, fase):
        esito = cancella(sess, cal, eid) if fase == 'elimina' else scrivi(sess, cal, eid, corpo)
        print(f'{esito}: {corpo["summary"]}  (giorno {day.isoformat()})')

if __name__ == '__main__':
    main()
