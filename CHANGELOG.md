# Spartans Manager — Changelog

---

## v4.2.0 · Giugno 2026

### Nuove funzionalità
- **Snapshot completo alla chiusura stagione** — alla chiusura vengono salvati integralmente: atleti, staff, corsi, presenze, eventi, abbonamenti, piani e valutazioni atleti; i dati sono navigabili in futuro senza limiti
- **Archivio stagione a 5 tab** — il dettaglio di ogni stagione archiviata mostra: Riepilogo (statistiche chiave + risultato sportivo), Atleti (tabella completa con tessere), Presenze (classifica % per atleta con barra visiva), Valutazioni (punteggi fisico/tecnico/tattico per ogni atleta al momento della chiusura), Eventi (calendario gare e allenamenti)
- **Badge snapshot** — indicatore visivo "✓ Snapshot completo" vs "⚠ Snapshot parziale" per distinguere le stagioni archiviate con la nuova logica da quelle precedenti
- **Separazione stagione sportiva / anno fiscale** — i dati finanziari (entrate/uscite) sono esclusi dallo snapshot di stagione; la chiusura fiscale sarà gestita separatamente in Amministrazione

---

## v4.1.0 · Giugno 2026

### Nuove funzionalità
- **Certificato di iscrizione** — nuovo documento in Genera documenti: certifica l'iscrizione dell'atleta all'ASD per la stagione sportiva in corso, con testo legale formale, dati tessera ASD/FISR e firma presidente
- **Attestato di frequenza** — nuovo documento in Genera documenti: attesta la partecipazione dell'atleta alle attività sportive in un periodo personalizzabile (data inizio / data fine), con testo legale formale e firma presidente
- **Checklist nuovo iscritto** — nuovo tab "✅ Checklist" nella scheda atleta: mostra i 7 passi del processo di iscrizione (anagrafica completa, corso assegnato, modulo iscrizione firmato, modulo privacy firmato, primo pagamento, tessera FISR, certificato medico) con stato FATTO/DA FARE, barra di avanzamento % e link diretto al tab da completare
- **Badge Moduli in tabella anagrafica** — nuova colonna che indica a colpo d'occhio se i moduli iscrizione e privacy firmati sono stati caricati (✓ verde / ⚠ parziale / ✗ mancante)

### Fix
- **Presenze strutturale** — aggiunta funzione `riparaPresenzeOrphane()` che corregge automaticamente le voci di presenza quando un atleta viene spostato da un corso all'altro; il fix scatta ad ogni salvataggio, importazione, caricamento app e ripristino backup
- **Colonna # duplicata nello staff** — rimossa la seconda intestazione `#` nella tabella staff che causava lo spostamento di tutte le colonne
- **Età senza suffisso "a"** — rimosso il suffisso "a" (anni) dall'indicazione dell'età nelle tabelle anagrafica e staff

### File aggiunti
- `modulo_certificato_iscrizione.html`, `modulo_attestato_frequenza.html`

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
