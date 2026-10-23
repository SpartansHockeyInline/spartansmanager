#!/usr/bin/env python3
"""Prova: un invito iCalendar mandato via Gmail finisce nel Google Calendar?

Manda due inviti di prova (all-day, tra due giorni) all'indirizzo GMAIL_USER:
  A = con ORGANIZER    B = senza ORGANIZER
FASE=invita    -> manda A e B (METHOD:REQUEST, SEQUENCE 0)
FASE=aggiorna  -> manda A aggiornato (SEQUENCE 1) e annulla B (METHOD:CANCEL)

Segreti (solo da variabili d'ambiente, mai stampati): GMAIL_USER, GMAIL_APP_PASSWORD.
Con --dry-run non invia nulla: scrive i messaggi .eml nella cartella ./out.
"""
import os, sys, smtplib, ssl, datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate, make_msgid
from zoneinfo import ZoneInfo

def esc(s):
    bs = chr(92)  # backslash: evita ambiguita' di escape nel sorgente
    return s.replace(bs, bs + bs).replace(';', bs + ';').replace(',', bs + ',').replace('\n', bs + 'n')

def fold(line):
    """Righe iCalendar max 75 byte, senza spezzare un carattere UTF-8."""
    raw, parts, limit = line.encode('utf-8'), [], 75
    while len(raw) > limit:
        cut = limit
        while (raw[cut] & 0xC0) == 0x80:
            cut -= 1
        parts.append(raw[:cut].decode('utf-8'))
        raw, limit = raw[cut:], 74
    parts.append(raw.decode('utf-8'))
    return '\r\n '.join(parts)

def build_ics(method, uid, seq, summary, descr, day, user, con_organizer):
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    d0, d1 = day.strftime('%Y%m%d'), (day + dt.timedelta(days=1)).strftime('%Y%m%d')
    L = ['BEGIN:VCALENDAR', 'PRODID:-//Spartans Manager//Prova invito//IT', 'VERSION:2.0',
         'CALSCALE:GREGORIAN', f'METHOD:{method}', 'BEGIN:VEVENT',
         f'UID:{uid}', f'DTSTAMP:{stamp}', f'DTSTART;VALUE=DATE:{d0}', f'DTEND;VALUE=DATE:{d1}',
         f'SEQUENCE:{seq}', f'SUMMARY:{esc(summary)}', f'DESCRIPTION:{esc(descr)}']
    if con_organizer:
        L.append(f'ORGANIZER;CN=Spartans Manager:mailto:{user}')
    L.append(f'ATTENDEE;CN={user};ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE:mailto:{user}')
    L += ['STATUS:CANCELLED' if method == 'CANCEL' else 'STATUS:CONFIRMED', 'TRANSP:TRANSPARENT']
    if method == 'REQUEST':
        L += ['BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:Promemoria', 'TRIGGER:-PT15H', 'END:VALARM']
    L += ['END:VEVENT', 'END:VCALENDAR']
    return '\r\n'.join(fold(x) for x in L) + '\r\n'

def build_msg(user, subject, testo, ics, method):
    msg = MIMEMultipart('mixed')
    msg['From'], msg['To'], msg['Subject'] = user, user, subject
    msg['Date'], msg['Message-ID'] = formatdate(localtime=False), make_msgid(domain='spartansmanager.local')
    alt = MIMEMultipart('alternative')
    alt.attach(MIMEText(testo, 'plain', 'utf-8'))
    cal = MIMEText(ics, 'calendar', 'utf-8')
    cal.replace_header('Content-Type', f'text/calendar; charset="UTF-8"; method={method}')
    alt.attach(cal)
    msg.attach(alt)
    att = MIMEApplication(ics.encode('utf-8'), 'ics', name='invite.ics')
    att.add_header('Content-Disposition', 'attachment', filename='invite.ics')
    msg.attach(att)
    return msg

def main():
    dry = '--dry-run' in sys.argv
    fase = os.environ.get('FASE', 'invita')
    if fase not in ('invita', 'aggiorna'):
        sys.exit(f'FASE non valida: {fase}')
    user = os.environ.get('GMAIL_USER', '').strip() or ('prova@example.com' if dry else '')
    pwd = os.environ.get('GMAIL_APP_PASSWORD', '').replace(' ', '')
    if not dry and (not user or not pwd):
        sys.exit('Mancano i Secrets GMAIL_USER e/o GMAIL_APP_PASSWORD (Settings > Secrets and variables > Actions).')
    day = dt.datetime.now(ZoneInfo('Europe/Rome')).date() + dt.timedelta(days=2)
    uid_a, uid_b = 'prova-a@spartansmanager', 'prova-b@spartansmanager'
    if fase == 'invita':
        lavori = [('REQUEST', uid_a, 0, 'PROVA Spartans Manager - A (con organizzatore)', True),
                  ('REQUEST', uid_b, 0, 'PROVA Spartans Manager - B (senza organizzatore)', False)]
    else:
        lavori = [('REQUEST', uid_a, 1, 'PROVA Spartans Manager - A (AGGIORNATO)', True),
                  ('CANCEL', uid_b, 1, 'PROVA Spartans Manager - B (senza organizzatore)', False)]
    msgs = []
    for method, uid, seq, summary, con_org in lavori:
        ics = build_ics(method, uid, seq, summary, 'Invito di prova generato da Spartans Manager. Si puo eliminare.', day, user, con_org)
        prefisso = 'Annullato' if method == 'CANCEL' else ('Invito aggiornato' if seq else 'Invito')
        msgs.append((summary, build_msg(user, f'{prefisso}: {summary}', f'{prefisso}: {summary}\nGiorno: {day.isoformat()}\n', ics, method)))
    if dry:
        os.makedirs('out', exist_ok=True)
        for i, (summary, m) in enumerate(msgs):
            open(f'out/{fase}_{i}.eml', 'wb').write(m.as_bytes())
        print(f'dry-run: scritti {len(msgs)} messaggi in ./out')
        return
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context(), timeout=30) as s:
            s.login(user, pwd)
            for summary, m in msgs:
                s.send_message(m)
                print(f'inviato: {summary}  (giorno {day.isoformat()})')
    except smtplib.SMTPAuthenticationError:
        sys.exit('Gmail ha rifiutato il login: controlla GMAIL_USER e che GMAIL_APP_PASSWORD sia una password per app (non quella normale).')

if __name__ == '__main__':
    main()
