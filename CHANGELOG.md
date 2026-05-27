# Spartans Manager — Changelog

---

## v4.0.0 · Maggio 2026

### Cambiamento architetturale
- **Ricerca globale** — barra di ricerca nella topbar: cerca trasversalmente su atleti, staff, fornitori, entrate, uscite ed eventi; click sul risultato porta direttamente alla sezione
- **Guida integrata** — nuova sezione in Sistema → Guida: 20 guide pratiche organizzate per argomento (Anagrafiche, Amministrazione, Presenze, Calendario, Documenti, Comunicazioni, Fornitori, Impostazioni) con ricerca interna
- **UX mobile migliorata** — le tabelle su schermi ≤640px si trasformano automaticamente in card stacked per una navigazione più comoda da smartphone
- **Pagamenti atleta unificati** — il tab Pagamenti nella scheda atleta mostra lo storico delle entrate registrate in Amministrazione; campo "Atleta collegato" nelle entrate; filtro per atleta nella Prima Nota

---

## v3.8.0 · Maggio 2026

### Nuove funzionalità
- **Solleciti abbonamenti** — lista abbonamenti scaduti o in scadenza entro 30gg; sollecito diretto via email o WhatsApp
- **Storico abbonamenti** — elenco completo con filtro per socio e piano, stato colorato, metodo di pagamento
- **Statistiche abbonamenti** — totali attivi/scaduti/incassati, breakdown per piano e grafico incassi per mese
- **Alert scadenza in scheda atleta** — avviso nel tab Pagamenti se l'abbonamento è scaduto o in scadenza entro 30 giorni

### Fix
- **Link fornitori** — il sito web si apre correttamente in una nuova scheda (https:// aggiunto automaticamente se mancante)

---

## v3.7.0 · Maggio 2026

### Nuove funzionalità
- **Vista Agenda calendario** — lista eventi del mese per giorno con icona, orario, luogo e squadra
- **Filtro corso/squadra calendario** — filtra eventi per corso in entrambe le viste
- **Esporta iCal** — formato .ics per Google Calendar e Apple Calendar
- **Oggi evidenziato** — il giorno corrente è evidenziato nella vista mensile
- **Lista iscritti per corso** — click su 👥 per vedere atleti iscritti con avatar e categoria FISR
- **Linee / Gruppi** — crea sottogruppi dentro ogni corso, assegna/rimuovi atleti per testare combinazioni; salvato su Firebase senza toccare l'anagrafica

---

## v3.6.0 · Maggio 2026

### Nuove funzionalità
- **Report % presenze** — percentuale per atleta con barra visiva colorata, periodo default = stagione corrente
- **Classifica frequenza** — ranking con medaglie 🥇🥈🥉
- **Alert bassa frequenza** — soglia configurabile (default 50%), sollecito diretto via email o WhatsApp
- **Esporta presenze CSV** — filtro per corso, mese, anno
- **Calcolo corretto** — base = sessioni totali del corso, non solo quelle dell'atleta

---

## v3.5.0 · Maggio 2026

### Nuove funzionalità
- **Gestione fornitori** — anagrafica con ragione sociale, CF/P.IVA, indirizzo, referente, categoria, sito web
- **Collegamento fornitori alle uscite** — campo opzionale nel modal Nuova uscita
- **Totale speso per fornitore** — nel riepilogo e nel Rendiconto economico

---

## v3.4.0 · Maggio 2026

### Nuove funzionalità
- **Prima nota** — movimenti cronologici con saldo progressivo, filtro periodo e atleta, stampa
- **Rendiconto economico** — totali per causale con avanzo/disavanzo, stampabile
- **Solleciti di pagamento** — quote scadute/in scadenza entro 30gg; sollecito via Gmail o WhatsApp
- **Comunicazioni** — genitori e staff nella lista; Gmail diretto; mittente fisso spartanshockeyinline@gmail.com

---

## v3.3.1 · Maggio 2026

### Fix
- **Scadenze dashboard** — visita medica, assicurazione, tessere staff, eventi non-allenamento entro 60gg
- **Timbro documenti** — 5 righe con dati fissi dell'associazione
- **Numero ricevuta** — progressivo Firebase, parte da 1, formato 4 cifre
- **Comunicati FISR** — URL corretti stagioni 2013/14, 2014/15, 2015/16

---

## v3.3.0 · Maggio 2026

### Nuove funzionalità
- **Genera documenti** — 5 modelli pre-compilati: 730, Giustificazione scolastica, Visita medica, Volontariato/Co.Co.Co., Ricevuta pagamento
- **Timbro digitale automatico** — SVG con dati fissi dell'associazione
- **Sidebar scrollabile**

### File aggiunti
- `modulo_730.html`, `modulo_giustificazione.html`, `modulo_visita_medica.html`, `modulo_volontariato.html`, `modulo_ricevuta.html`

---

## v3.2.0 · Maggio 2026

### Nuove funzionalità
- **Separazione Atleti / Staff** — 3 tab: Atleti, Staff, Macrogruppi
- **Scheda atleta a 6 tab** — Anagrafica, Sanitario, Genitori (2), Taglie, Pagamenti, Documenti
- **Visita medica, genitori strutturati, macrogruppi**
- **Importazione Google Form** — 39 colonne, aggiorna campi vuoti
- **Colonna Azioni fissa**

### File aggiunti
- `modulo_iscrizione_spartans.html`, `modulo_consenso_privacy.html`

---

## v3.1.0 · Maggio 2026
- Comunicati FISR, ordinamento amministrazione, fasi sensibili Martin 1982

## v3.0.0 · Maggio 2026
- Migrazione Firebase, login email/password, sync realtime

## v2.x · Aprile–Maggio 2026
- v2.5: PWA + Drive; v2.4: comunicazioni, valutazioni; v2.3: presenze, categorie FISR; v2.2: filtri, ordinamento; v2.1: sync live; v2.0: riscrittura completa; v1.x: base
