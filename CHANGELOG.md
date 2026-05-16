# Spartans Manager — Changelog

---

## v3.1.0 · Maggio 2026

### Nuove funzionalità
- **Comunicati FISR** — nuova sezione nel menu (📋); mostra l'elenco aggiornato dei comunicati ufficiali Hockey Inline dalla stagione selezionata; badge rosso sui nuovi CU non letti; verifica automatica giornaliera in background all'apertura dell'app; link diretto al download PDF; pulsante "Segna tutti come visti"
- **Ordinamento amministrazione** — click sull'intestazione di ogni colonna (Data, Descrizione, Categoria, Importo, Metodo) ordina crescente/decrescente sia nelle entrate che nelle uscite; la colonna Azioni non è ordinabile
- **Fasi sensibili Martin 1982 corrette** — la scheda nella valutazione atleti è ora una guida per il tecnico: classifica le capacità in 🔴 Priorità Alta (fase attiva — allena adesso), 🟡 Media (fase prossima/in uscita), ⚪ Bassa (fuori fase — non è il momento ottimale), con finestra biologica ±2 anni per tenere conto delle differenze tra età biologica e anagrafica

---

## v3.0.0 · Maggio 2026

### Cambiamento architetturale
- **Migrazione da Google Drive a Firebase** — eliminato il sistema OAuth Google Drive con tutti i problemi di scope e verifica app; sostituito con Firebase Realtime Database + Firebase Authentication
- **Login email/password** — accesso con credenziali dedicate all'app, indipendenti dagli account Google; nessun problema di 2FA condiviso, nessuna verifica Google richiesta
- **Sincronizzazione in tempo reale** — tutti gli utenti vedono le modifiche istantaneamente tramite listener Firebase, senza polling ogni 30 secondi
- **Multi-account nativo** — ogni utente ha le proprie credenziali Firebase; tutti leggono e scrivono sullo stesso database senza restrizioni di scope OAuth

### Note versioning
Da questa versione il formato è **X.Y.Z**: X = cambiamento architetturale, Y = nuove funzionalità, Z = modifiche minori e grafiche

---

## v2.5 · Maggio 2026

### Nuove funzionalità
- **Multi-account Google** — ogni utente accede con il proprio account Google personale; l'admin crea il file dati su Drive e condivide il File ID; gli altri utenti incollano il File ID nelle Impostazioni; nessuna credenziale condivisa, nessun problema di 2FA
- **Layout responsive completo** — su tablet (< 900px) la sidebar diventa menu a tendina con bottone ☰; su mobile (< 640px) i modali si aprono dal basso, i form vanno su colonna singola, le tabelle scorrono orizzontalmente
- **PWA (Progressive Web App)** — aggiunto `manifest.json`; su Android e iOS appare il banner "Aggiungi alla schermata home"; si installa come app nativa a schermo intero senza barra del browser
- **Fasi sensibili Martin 1982 corrette** — la tab è ora una guida per il tecnico: classifica le capacità in 🔴 Priorità Alta (fase attiva), 🟡 Media (fase prossima/in uscita), ⚪ Bassa (fuori fase), con finestra biologica ±2 anni per tenere conto delle differenze tra età biologica e anagrafica

### Modifiche
- Scope OAuth: da `drive.appdata` a `drive.file` per supportare file condivisibili tra account diversi
- Login con `prompt: select_account` — ogni utente sceglie il proprio account Google
- Impostazioni: nuova sezione File ID con copia per admin e campo incolla per utenti
- Backup Drive aggiornato per il nuovo sistema di file

---

## v2.4 · Maggio 2026

### Nuove funzionalità
- **Sezione Comunicazioni** — seleziona destinatari per corso o tipologia; componi messaggio con oggetto e firma; tre canali di invio: email via mailto (BCC a tutti), copia testo per WhatsApp Broadcast List, esportazione contatti .vcf per importazione in rubrica; slot riservato per integrazione futura WhatsApp Business API con campo token
- **Sezione Valutazione atleti** — scheda completa per ogni atleta divisa in 3 tab:
  - *Psico-fisica*: capacità fisiche (resistenza, forza, rapidità, equilibrio, ritmo, coordinazione, orientamento, reazione) + tratti psicologici (aggressività agonistica, leadership, spirito di squadra, concentrazione, determinazione, voglia di apprendere, gestione pressione, autostima)
  - *Tecnica*: pattinaggio avanti/indietro, uso bastone/dribbling, passaggio, tiro, finte — basata sui Moduli A/B/C/D FISR (livelli 1-5: Principiante→Evoluto)
  - *Tattica*: individuale offensiva/difensiva + collettiva offensiva/difensiva — dalle tabelle FISR pag. 224-236
- **Fasi sensibili Martin 1982** — tab nella valutazione: per ogni capacità mostra le età sensibili (M/F separate) con evidenziazione della finestra biologica ±2 anni rispetto all'età dell'atleta
- **Modulo H2 FISR** — generazione automatica del modulo ufficiale elenco atleti per gara, compilato con dati delle convocazioni (cognome/nome, data nascita, tessera FISR, numero maglia, ruolo); accessibile dal dettaglio evento gara con pulsante "📋 Modulo H2"; stampabile/esportabile come PDF

### Modifiche
- Sidebar: nuove voci Comunicazioni (📨) e Valutazione atleti (📊)
- Dettaglio evento gara: aggiunto pulsante Modulo H2 accanto a Convocazioni
- DB: aggiunto oggetto `valutazioni` per memorizzare le schede di ogni atleta

---

## v2.3 · Maggio 2026

### Nuove funzionalità
- **Storico presenze filtrato per mese e anno** — selettori mese e anno nello storico presenze per visualizzare singoli periodi di allenamento
- **Ordinamento crescente date presenze** — lo storico è ordinato dal più vecchio al più recente (ordine cronologico)
- **Riepilogo statistico storico presenze** — per ogni sessione: numero presenti, assenti, percentuale; riepilogo con totale sessioni e media presenti nel periodo filtrato
- **Età anagrafica automatica** — campo calcolato automaticamente dalla data di nascita, non modificabile, visibile e ordinabile nella tabella anagrafiche
- **Categoria FISR automatica** — calcolata dinamicamente in base all'anno di nascita e alla stagione sportiva attiva, secondo le norme ufficiali FISR Hockey Inline (CU n.044/2022): Primi Passi (2017+), Minihockey (2015-2016), Under 10 (2013-2014), Under 12 (2011-2012), Under 14 (2009-2010), Under 16 (2007-2008), Elite (2005-2006), Under 20 (2002-2004), Seniores (2001 e precedenti), Amatori
- **Filtro per categoria FISR** — il selettore categorie usa le classificazioni ufficiali FISR; il calcolo si aggiorna automaticamente ad ogni cambio di stagione

### Modifiche
- Tabella anagrafiche: aggiunte colonne Età e Categoria FISR (ordinabili)
- Storico presenze: aggiunto riepilogo con media e percentuale presenze per sessione

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
