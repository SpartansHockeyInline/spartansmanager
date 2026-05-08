# Spartans Manager — Changelog

---

## v2.2 · Maggio 2026

### Nuove funzionalità
- **Filtri avanzati anagrafiche** — filtra per tipologia, corso/squadra, stato (attivo/sospeso/inattivo) e fascia d'età (under 12, under 18, over 18); pulsante reset filtri
- **Ordinamento colonne** — click sull'intestazione ordina alfabeticamente o per data, crescente/decrescente, su tutte le colonne della tabella anagrafiche
- **Numerazione righe fissa** — contatore progressivo (#) indipendente da filtri e ordinamento; contatore "Totale visualizzati" sopra la tabella
- **Assicurazione socio** — campo dedicato nella scheda anagrafica con stato (pagata/non pagata/in attesa), data scadenza, compagnia/ente e numero polizza
- **Badge abbonamento automatico** — la tabella anagrafiche mostra se il socio ha un abbonamento attivo nel mese corrente, calcolato automaticamente dalla sezione Abbonamenti
- **Changelog in-app** — cliccando sulla versione nel footer si apre il modal con lo storico completo delle versioni

### Modifiche
- Tabella anagrafiche: aggiunte colonne Assicurazione e Abbonamento corrente
- Footer versione reso cliccabile con indicatore ℹ️

---

## v2.1 · Maggio 2026

### Nuove funzionalità
- **Sincronizzazione live tra dispositivi** — polling automatico ogni 30 secondi su Google Drive; aggiornamento automatico con notifica visiva
- **Foto profilo** — caricabile in anagrafica (max 2MB); sostituisce le iniziali ovunque
- **Dati biometrici e taglie** — altezza, peso, taglia guanti/ginocchiere/gomitiere/abbigliamento, numero maglia gara
- **Corso/squadra nell'anagrafica** — associazione diretta socio↔corso al momento dell'inserimento
- **Icona impianti** — selettore visivo con 12 icone
- **Modifica movimenti** — pulsante ✏️ su ogni entrata/uscita in amministrazione
- **Importazione massiva da Google Sheets** — via URL CSV pubblico o incolla diretta
- **Versioning nel footer** — numero versione e data di rilascio sempre visibili

### Modifiche
- Dashboard: sostituiti "ultimi soci aggiunti" con "prossimi eventi"
- Palette colori sociali Spartans (nero, rosso, bianco, oro)
- Linea decorativa rosso→oro→rosso sotto il topbar

### Fix
- Corretti errori JavaScript per dichiarazioni duplicate di `convEventoId` e `restoreTargetIdx`
- Gestione versioni standardizzata

---

## v2.0

### Riscrittura completa
- Titolo "Spartans Manager" e favicon
- 11 tipologie socio + 2 tessere con scadenze (ASD e FISR)
- Allegati multipli per ogni anagrafica (doc. identità, visite mediche ecc.)
- Corsi con selezione multipla giorni e orari inizio/fine per ciascuno
- Registro presenze con toggle e storico sessioni
- Calendario mensile con gare (rosso) e allenamenti (blu)
- Convocazioni per gare con gestione rosa
- Stagioni sportive con archiviazione, snapshot e storico
- Allenamenti automatici nel calendario dai corsi attivi
- Backup automatico con 3 snapshot (localStorage + Drive)
- Scadenze in dashboard con alert colorati a 30 giorni
- Fix scroll su tutti i dispositivi (mobile, tablet, desktop)

---

## v1.4

### Fix
- Rimosso monkey-patch di `showPage` che bloccava l'intera applicazione al caricamento
- Logica pagina Impostazioni integrata direttamente nella funzione `showPage` originale

---

## v1.3

### Nuove funzionalità
- Tema chiaro/scuro con selettore visivo nella sezione Impostazioni
- Preferenza tema salvata in localStorage per dispositivo

---

## v1.2

### Nuove funzionalità
- Deploy su GitHub Pages — accesso da qualsiasi dispositivo su `https://mascio79.github.io/sportmanager`
- Configurazione OAuth per origine `https://mascio79.github.io`
- Account `spartanshockeyinline@gmail.com` aggiunto come utente di test OAuth

---

## v1.1

### Nuove funzionalità
- Integrazione Google Drive — login OAuth, sincronizzazione automatica su `appDataFolder`
- Barra di stato con indicatore connessione (verde/giallo/rosso)
- Token salvato in localStorage per sessioni successive
- Export/Import JSON come backup di emergenza sempre disponibile

---

## v1.0 — Versione iniziale

### Funzionalità base
- La mia struttura (IDS, sport praticati, documenti, logo)
- Anagrafiche soci con ricerca, stato, numero tessera
- Abbonamenti con piani personalizzabili e assegnazione soci
- Corsi e squadre con tecnico, impianto, giorno e orario
- Impianti sportivi con tipo e capienza
- Maestri/Tecnici con qualifica e disciplina
- Amministrazione: entrate, uscite, saldo
- Persistenza localStorage + export/import JSON
- UI: sidebar collassabile, tema scuro, modali, toast, badge contatori

---

*Spartans Hockey In-Line — ASD Spartans Bari*


---

## v2.1 · Maggio 2026

### Nuove funzionalità
- **Sincronizzazione live tra dispositivi** — polling automatico ogni 30 secondi su Google Drive; se un altro dispositivo modifica i dati, la pagina si aggiorna automaticamente con notifica visiva
- **Foto profilo** — ogni anagrafica può avere una foto caricata (max 2MB); sostituisce le iniziali in tabelle, presenze e convocazioni
- **Dati biometrici e taglie** — nuovi campi in anagrafica: altezza, peso, taglia guanti, ginocchiere, gomitiere, abbigliamento, numero maglia gara
- **Corso/squadra nell'anagrafica** — al momento dell'inserimento si può associare il socio direttamente a un corso/squadra; le presenze filtrano automaticamente per corso
- **Icona impianti** — selettore visivo con 12 icone tra cui scegliere al posto dell'emoji automatica per tipo
- **Modifica movimenti** — ogni entrata/uscita in amministrazione ha ora il pulsante ✏️ oltre al 🗑️
- **Importazione massiva da Google Sheets** — pulsante "📊 Importa da Sheets" in Anagrafiche; supporta URL CSV pubblico e incolla diretta del CSV
- **Versioning nel footer** — numero di versione e data di rilascio visibili in fondo alla pagina; cliccabile per visualizzare il changelog completo (dalla v2.2)

### Modifiche
- **Dashboard** — rimossi gli "ultimi soci aggiunti", sostituiti con i "prossimi eventi" in evidenza; riepilogo economico spostato nella colonna laterale
- **Colori sociali** — palette aggiornata con i colori ufficiali degli Spartans: nero, rosso, bianco e oro; gradiente rosso→oro su bottoni, tab attivi e barra superiore
- **Barra superiore** — aggiunta linea decorativa rosso→oro→rosso sotto il topbar

### Fix
- Corretti errori JavaScript per dichiarazioni duplicate di `convEventoId` e `restoreTargetIdx`
- Gestione versioni standardizzata: incremento 0.1 per ogni sessione di modifiche, data aggiornata al mese di rilascio

---

## v2.0 · (rilascio precedente)

### Nuove funzionalità
- **Titolo e identità** — rinominato "Spartans Manager", favicon con elmo spartano
- **Anagrafiche** — 11 tipologie di socio selezionabili (atleta, dirigente, tecnico, genitore, presidente, vice-presidente, segretario, tesoriere, attrezzista, cronometrista, segnapunti); 2 tessere con scadenze (ASD e FISR); allegati multipli per documento d'identità, visite mediche, ecc.
- **Corsi e squadre** — selezione multipla dei giorni di allenamento con orario inizio/fine per ciascuno
- **Registro presenze** — toggle presente/assente per ogni atleta, salvataggio per data/corso, storico sessioni con conteggio
- **Calendario mensile** — visualizzazione gare (rosso) e allenamenti (blu), navigazione per mese
- **Convocazioni** — gestione rosa convocati/disponibili per ogni gara
- **Stagioni sportive** — creazione, attivazione, modifica e archiviazione stagioni; snapshot automatico a chiusura con risultati sportivi e bilancio; storico stagioni con dettaglio completo
- **Allenamenti automatici** — i corsi con giorni/orari generano automaticamente gli eventi di allenamento nel calendario per tutta la durata della stagione attiva
- **Backup automatico** — snapshot dei dati ad ogni apertura; ultimi 3 backup conservati in localStorage e su Drive (`spartans_backup.json`); ripristino con un click dalla sezione Impostazioni
- **Dashboard scadenze** — alert colorati per tessere e abbonamenti in scadenza entro 30 giorni

### Modifiche
- Riscrittura completa del codebase per pulizia e manutenibilità
- Sidebar aggiornata con tutte le nuove sezioni
- Fix scroll su tutti i dispositivi (mobile, tablet, desktop)

---

## v1.4 · (rilascio precedente)

### Fix
- Rimosso il monkey-patch di `showPage` che bloccava l'intera applicazione al caricamento
- Logica pagina Impostazioni integrata direttamente nella funzione `showPage` originale

---

## v1.3 · (rilascio precedente)

### Nuove funzionalità
- **Tema chiaro/scuro** — sezione Impostazioni con selettore visivo; preferenza salvata in localStorage per dispositivo; tema chiaro con palette alternativa su sfondo grigio chiaro

---

## v1.2 · (rilascio precedente)

### Nuove funzionalità
- **Deploy su GitHub Pages** — applicazione accessibile da qualsiasi dispositivo all'indirizzo `https://mascio79.github.io/sportmanager`

### Modifiche
- Aggiunta origine autorizzata OAuth (`https://mascio79.github.io`) nella Google Cloud Console
- Aggiunto account `spartanshockeyinline@gmail.com` come utente di test OAuth

---

## v1.1 · (rilascio precedente)

### Nuove funzionalità
- **Integrazione Google Drive** — login OAuth Google; sincronizzazione automatica su `appDataFolder` di Drive; barra di stato in basso con indicatore connessione (verde/giallo/rosso); token salvato in localStorage per sessioni successive; rilevamento token scaduto con re-login automatico
- **Export/Import JSON** — backup di emergenza sempre disponibile nella barra inferiore indipendentemente dallo stato Drive

---

## v1.0 · (rilascio iniziale)

### Funzionalità iniziali
- **La mia struttura** — dati identificativi ASD (IDS), sport praticati, documenti struttura, caricamento logo
- **Anagrafiche** — gestione soci con ricerca, stato (attivo/sospeso/inattivo), numero tessera
- **Abbonamenti** — piani abbonamento personalizzabili, assegnazione soci con date e metodo di pagamento
- **Corsi e squadre** — gestione corsi con tecnico, impianto, giorno e orario
- **Impianti** — anagrafica impianti sportivi con tipo e capienza
- **Maestri/Tecnici** — registro tecnici con qualifica e disciplina
- **Amministrazione** — entrate e uscite con categorie, metodo pagamento e saldo
- **Persistenza dati** — localStorage come storage primario, export/import JSON come backup manuale
- **UI** — sidebar collassabile, tema scuro, modali, toast notifications, badge contatori

---

*Spartans Hockey In-Line — ASD Spartans Bari*
