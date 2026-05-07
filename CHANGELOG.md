# Spartans Manager — Changelog

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
