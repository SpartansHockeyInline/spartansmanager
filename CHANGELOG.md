# Spartans Manager — Changelog

---

## v3.6.0 · Maggio 2026

### Nuove funzionalità
- **Report % presenze** — percentuale presenze per atleta nel periodo selezionato, con barra visiva colorata (verde ≥75%, giallo ≥50%, rosso <50%)
- **Classifica frequenza** — ranking atleti per frequenza con medaglie per i primi tre
- **Alert bassa frequenza** — lista atleti sotto soglia configurabile (default 50%); sollecito diretto via email o WhatsApp
- **Esporta presenze CSV** — storico esportabile filtrabile per corso, mese, anno

---

## v3.5.0 · Maggio 2026

### Nuove funzionalità
- **Gestione fornitori** — anagrafica fornitori con ragione sociale, CF/P.IVA, indirizzo, referente, categoria, sito web
- **Collegamento fornitori alle uscite** — campo opzionale nel modal Nuova uscita
- **Totale speso per fornitore** — nel riepilogo e nel Rendiconto economico

---

## v3.4.0 · Maggio 2026

### Nuove funzionalità
- **Prima nota** — movimenti cronologici con saldo progressivo, filtro periodo, stampa
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
