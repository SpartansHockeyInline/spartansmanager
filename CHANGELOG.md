# Spartans Manager — Changelog

---

## v3.4.0 · Maggio 2026

### Nuove funzionalità
- **Prima nota** — nuovo tab in Amministrazione: elenco cronologico di tutti i movimenti con saldo progressivo, filtro per periodo e stampa
- **Rendiconto economico** — nuovo tab: totali entrate e uscite per causale con avanzo/disavanzo di gestione, stampabile
- **Solleciti di pagamento** — nuovo tab: lista automatica quote scadute o in scadenza entro 30 giorni; invio sollecito diretto via email (Gmail) o WhatsApp con testo precompilato
- **Comunicazioni** — ora include genitori e staff nella lista destinatari; apertura Gmail diretta senza configurazione browser; account mittente fisso `spartanshockeyinline@gmail.com`

---

## v3.3.1 · Maggio 2026

### Fix
- **Scadenze dashboard** — ora include visita medica, assicurazione, tessere staff; eventi non-allenamento entro 60 giorni; grassetto per scadenze entro 7 giorni
- **Timbro documenti** — semplificato a 5 righe con dati fissi dell'associazione
- **Numero ricevuta** — progressivo salvato su Firebase, parte da 1, formato 4 cifre (0001, 0002...)
- **Comunicati FISR** — corretti URL stagioni 2013/14, 2014/15, 2015/16; filtro contenuti non pertinenti

---

## v3.3.0 · Maggio 2026

### Nuove funzionalità
- **Genera documenti** — 5 modelli pre-compilati: Certificazione 730, Giustificazione scolastica, Richiesta visita medica, Dichiarazione volontariato/Co.Co.Co., Ricevuta pagamento
- **Timbro digitale automatico** — generato con dati fissi dell'associazione in formato SVG
- **Sidebar scrollabile** — menu scorre verticalmente, tutti i pulsanti sempre raggiungibili

### File aggiunti
- `modulo_730.html`, `modulo_giustificazione.html`, `modulo_visita_medica.html`, `modulo_volontariato.html`, `modulo_ricevuta.html`

---

## v3.2.0 · Maggio 2026

### Nuove funzionalità
- **Separazione Atleti / Staff** — Anagrafiche divisa in 3 tab: Atleti, Staff, Macrogruppi
- **Scheda atleta a 6 tab** — Anagrafica, Sanitario, Genitori (2), Taglie, Pagamenti, Documenti
- **Visita medica** — tipo, scadenza, medico/struttura, allegato; badge colorato in tabella
- **Genitori strutturati** — due genitori/tutori con rapporto, CF, contatti
- **Macrogruppi** — raggruppamenti trasversali (camp estivi, attività promozionali ecc.)
- **Moduli pre-compilati** — link con dati atleta per modulo iscrizione e consenso privacy
- **Importazione Google Form** — riconosce tutte le 39 colonne; aggiorna campi vuoti se atleta esiste
- **Colonna Azioni fissa** — sempre visibile con scroll orizzontale

### File aggiunti
- `modulo_iscrizione_spartans.html`, `modulo_consenso_privacy.html`

---

## v3.1.0 · Maggio 2026

### Nuove funzionalità
- **Comunicati FISR** — stagioni dal 2013/14; badge nuovi CU; verifica giornaliera
- **Ordinamento amministrazione** — tutte le colonne ordinabili crescente/decrescente
- **Fasi sensibili Martin 1982** — guida tecnico con priorità Alta/Media/Bassa

---

## v3.0.0 · Maggio 2026

### Cambiamento architetturale
- **Migrazione da Google Drive a Firebase** — Realtime Database + Authentication
- **Login email/password** — credenziali dedicate, indipendenti da Google
- **Sincronizzazione in tempo reale** — listener Firebase, nessun polling
- **Multi-account nativo** — tutti leggono e scrivono senza restrizioni OAuth

### Note versioning
**X.Y.Z**: X = architettura, Y = funzionalità, Z = modifiche minori/grafiche

---

## v2.5 · Maggio 2026
- Responsive + PWA + sincronizzazione Google Drive multi-account

## v2.4 · Aprile 2026
- Comunicazioni, valutazione atleti, modulo H2 FISR, fasi sensibili Martin

## v2.3 · Aprile 2026
- Storico presenze, età anagrafica, categorie FISR

## v2.2 · Aprile 2026
- Filtri avanzati, ordinamento colonne, badge abbonamento, changelog in-app

## v2.1 · Aprile 2026
- Sync live Drive, foto profilo, taglie, importazione Sheets

## v2.0 · Aprile 2026
- Riscrittura completa: stagioni, calendario, presenze, valutazioni

## v1.0–v1.4 · Aprile 2026
- Base + Drive appData + tema + GitHub Pages
