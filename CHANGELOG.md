# Spartans Manager — Changelog

---

## v5.5.0 · Settembre 2026

### Nuove funzionalità
- **Stato "Sospeso" escluso dai pagamenti** — un atleta con stato "Sospeso" non compare più tra le quote arretrate in Dashboard, non è selezionabile come "Atleta collegato" in una nuova entrata/ricevuta, e il suo stato pagamenti mostra "⏸ Sospeso" invece di un giudizio di regolarità: resta congelato finché non torna Attivo o passa a Inattivo.
- **Periodi di inattività con date specifiche** — nella scheda atleta (tab Anagrafica) è possibile registrare uno o più periodi di inattività (data inizio, data fine facoltativa se ancora in corso, motivo). I mesi coperti da un periodo NON vengono conteggiati come dovuti nel calcolo dei pagamenti mensili — a differenza di "Sospeso", l'atleta resta normalmente conteggiato per gli altri mesi, e il periodo resta valido anche se in seguito lo stato torna "Attivo" (utile per pause temporanee — infortuni, trasferimenti, ecc. — che non devono generare falsi arretrati).
- Le selezioni "Atleta collegato" in Amministrazione e Genera documenti ora includono anche gli atleti "Inattivo" (possono comunque dover pagare mesi fuori dal periodo escluso), escludendo solo i "Sospeso".

---

## v5.4.2 · Settembre 2026

### ⚠ Fix critico — riapertura di un'entrata/uscita mostrava l'atleta/fornitore sbagliato
- **Il campo "Atleta collegato" (o "Fornitore") non veniva mai ripristinato aprendo ✏️ un movimento esistente** — data, descrizione, importo e categoria tornavano corretti, ma il menu a tendina restava fermo su qualunque valore fosse rimasto dall'ultima registrazione fatta in precedenza. Risultato: riaprendo una vecchia entrata dopo averne registrata una nuova per un altro atleta, sembrava che quella vecchia fosse collegata al secondo atleta — mentre il dato salvato era in realtà sempre corretto. **Attenzione:** se in quella situazione si premeva "Salva" senza accorgersi del valore sbagliato nel menu, il collegamento veniva davvero sovrascritto. Riprodotto e verificato con un test automatico (simulazione dell'esatta sequenza segnalata, con jsdom) prima di correggerlo.
- Se hai già modificato e salvato movimenti in questa condizione, controlla in Amministrazione che l'Atleta collegato di ciascuna entrata corrisponda davvero alla persona giusta — usa lo "Storico pagamenti" nella scheda di ogni atleta (corretto in v5.4.1) come riferimento incrociato.

---

## v5.4.1 · Settembre 2026

### ⚠ Fix critico — pagamenti di un fratello comparivano su un altro
- **Storico pagamenti errato per famiglie con più figli** — nella scheda atleta, lo "Storico pagamenti" cercava le entrate anche per corrispondenza testuale sul cognome nella descrizione, oltre che per collegamento esplicito. Per fratelli che condividono lo stesso cognome (anche solo in parte, es. un cognome materno composto), questo faceva comparire il pagamento di un fratello anche nella scheda dell'altro, raddoppiando il totale mostrato. Ora il collegamento è solo tramite "Atleta collegato" (socioId): se un'entrata storica non risulta collegata a nessun atleta, va corretta da Amministrazione selezionando l'atleta giusto.

### Modifiche di forma alla tabella Atleti
- **Numero Tessera ASD di nuovo visibile** — torna a mostrare il numero effettivo (ordinabile cliccando sull'intestazione), utile per individuare a colpo d'occhio il numero successivo da assegnare a un nuovo atleta. Tessera FISR, Visita medica e Assicurazione restano invece semplici flag ✓/✗.
- **Colonna Atleta sempre visibile** — insieme al numero di riga, resta fissa a sinistra durante lo scroll orizzontale, così anche scorrendo verso le colonne più a destra si vede sempre a quale atleta si riferisce la riga.
- **Intestazione su un solo livello** — rimossa la riga di raggruppamento "Checklist iscrizione": tutte le intestazioni di colonna sono ora allo stesso livello. Le colonne della checklist sono rinominate con un ✓ (es. "Corso ✓") per non confondersi con le colonne dati omonime (es. "Corso").
- **Colonne più compatte** — ridotti font e spaziatura delle colonne meno critiche, per una tabella meno dispersiva scorrendo l'elenco.

---

## v5.4.0 · Settembre 2026

### Fix
- **Impossibile registrare un'entrata a zero euro** — la validazione trattava l'importo 0 come "dato mancante" (comportamento di JavaScript), bloccando la registrazione di abbonamenti/quote gratuite. Ora un importo di 0€ è accettato; resta bloccato solo il campo lasciato vuoto o un valore negativo. La Checklist ("primo pagamento") e il calcolo dei pagamenti mensili riconoscono inoltre come "in regola" un atleta con un piano assegnato a costo zero, anche senza nessuna entrata registrata.
- **Registro storico presenze mostrava una pagina vuota all'apertura** — richiedeva di selezionare prima un corso specifico. Ora mostra di default lo storico di tutti i corsi insieme (con colonna Corso per distinguerli), lasciando comunque la possibilità di filtrare su un singolo corso.

### Nuove funzionalità
- **Registro Ricevute** — nuovo tab "🧾 Ricevute" in Amministrazione: ogni ricevuta generata viene ora registrata in modo permanente (numero, data, atleta, importo, causale, metodo), non solo contata. Se il PDF/la stampa di una ricevuta va perso, può essere rigenerato identico in un click dal registro — prima questa informazione non veniva salvata da nessuna parte e andava persa non appena si chiudeva la scheda del documento.
- **Link Google Drive nei documenti dell'atleta** — nel tab Documenti della scheda atleta, oltre ad allegare un file, ora si può collegare direttamente il link di un documento salvato su Google Drive (utile per moduli scansionati/firmati recuperati con strumenti come DocHub o Adobe), senza dover scaricare e ricaricare il file nell'app.

### Nota aperta
- **Fornitori — persistenza tra stagioni**: verificato che `chiudiStagione()` non tocca in alcun modo `DB.fornitori` nel codice attuale — la perdita dati segnalata risale quasi certamente allo stesso incidente di giugno già diagnosticato (chiusura stagione che allora cancellava anche altri dati, prima dei fix). Nessuna azione di codice necessaria per il futuro su questo punto specifico.
- **Campo con testo non pertinente nella pagina Fornitori**: non individuato tramite revisione del codice (titolo pagina e campo di ricerca risultano corretti) — serve uno screenshot per localizzarlo con certezza.

---

## v5.3.0 · Settembre 2026

### ⚠ Fix sostanziale — calcolo pagamenti mensili
- **Il conteggio dei mesi dovuti partiva dalla data sbagliata** — usava la data di creazione della scheda atleta, che spesso risale a molto prima della reale iscrizione (es. importazioni o test precedenti), gonfiando artificialmente i mesi risultati arretrati. Ora il conteggio parte dalla data di inizio dell'abbonamento effettivamente assegnato all'atleta, impostabile liberamente.
- **Gestione di tariffe diverse in mesi diversi** — se un atleta ha avuto più abbonamenti assegnati in sequenza (es. un piano per il mese di iscrizione e uno successivo per la quota a regime), il calcolo ora somma correttamente l'importo atteso per ciascun periodo con il piano/prezzo di competenza, invece di applicare un unico piano a tutta la stagione.
- **Campo data di inizio nella scheda atleta** — il campo Abbonamento ora ha anche una data di inizio modificabile, invece di essere sempre fissata a "oggi" al momento dell'assegnazione.

### Nuove funzionalità
- **Quote mensili arretrate in Dashboard** — nuova card "💳 Quote mensili arretrate" che elenca direttamente gli atleti non in regola (calcolato sui pagamenti reali, non sulla sola scadenza "grezza" dell'abbonamento), con pulsanti per sollecitare subito via email o WhatsApp.

---

## v5.2.1 · Settembre 2026

### Modifiche di forma alla tabella Atleti
- **Tessere, visita medica e assicurazione come flag** — le colonne Tessera ASD, Tessera FISR, Vis. Medica e Assicurazione mostrano ora un semplice ✓/✗ invece del numero o della data per esteso, con il dettaglio completo disponibile passando il mouse sopra. Le scadenze imminenti restano comunque segnalate con 60 giorni di anticipo in Dashboard, quindi in tabella basta sapere se la pratica è a posto.

### Abbonamento nella scheda atleta
- **Campo Abbonamento ripristinato** — accanto al N° Maglia, la scheda atleta mostra ora il piano assegnato e lo stato dei pagamenti, con possibilità di assegnare o cambiare il piano direttamente da qui (senza dover passare dalla pagina Abbonamenti). Cambiare piano e salvare crea un nuovo abbonamento da oggi, senza cancellare lo storico dei piani precedenti.
- **Pagamenti mensili calcolati sul piano effettivo dell'atleta** — se è assegnato un abbonamento con un prezzo/durata riconoscibili, lo stato "in regola"/"arretrato" ora confronta i pagamenti ricevuti con la quota mensile DI QUEL piano specifico, non con uno standard generico: un atleta con una quota scontata/agevolata che paga regolarmente secondo il proprio piano risulta correttamente "in regola". Senza un piano assegnato, resta il conteggio per presenza di pagamento mensile già introdotto in precedenza.

---

## v5.2.0 · Settembre 2026

### Nuove funzionalità
- **Metodo di pagamento nella ricevuta** — la card "Ricevuta pagamento" in Genera documenti ora ha un menu per scegliere il metodo (Contanti, Bonifico, Carta, POS, Altro), che prima era fissato sempre a "Contanti" indipendentemente da come era stato effettuato il pagamento.
- **Proposta automatica di ricevuta dopo un'entrata** — quando registri in Amministrazione un'entrata collegata a un atleta (quota associativa, mensile o qualsiasi altro incasso), l'app chiede subito se vuoi generare la ricevuta, già precompilata con atleta, importo, causale e metodo appena inseriti — senza dover tornare su Genera documenti e reinserire gli stessi dati a mano.

---

## v5.1.1 · Settembre 2026

### Fix
- **Pagamenti mensili non si aggiornavano** — la colonna "Pagamenti mensili" e la voce "Primo pagamento" della Checklist cercavano le entrate con nomi di campo sbagliati (`atletaId`/`causale`) mentre Amministrazione le salva come `socioId`/`cat`/`descr`: nessun pagamento veniva mai riconosciuto, qualunque descrizione o categoria si usasse. Corretto — ora riconosce le entrate con categoria "Quota associativa" o "Abbonamento", o descrizione contenente "quota"/"abbonamento".
- **Nessuna modifica possibile per gli abbonamenti** — la tabella "Abbonamenti attivi" permetteva solo di assegnare un nuovo abbonamento o eliminarne uno esistente, senza alcuna possibilità di correggere quello già assegnato. Aggiunto il pulsante ✏️ per modificare socio, piano, date, importo e metodo di un abbonamento esistente.

### Altre modifiche
- **Checklist dettagliata invece di un unico campo** — nella tabella Atleti, i 7 passi della checklist non sono più raggruppati in un unico badge "N/7": ognuno ha ora la propria colonna (✓/✗) sotto l'intestazione di gruppo "Checklist iscrizione", per un controllo immediato senza dover passare il mouse sopra per vedere il dettaglio.
- **Rimossa la colonna "Tipo"** dalla tabella Atleti — nella vista per singola tipologia (es. tutti "atleta") era un valore ripetuto su ogni riga senza reale utilità; resta comunque disponibile come filtro sopra la tabella.

---

## v5.1.0 · Settembre 2026

### Nuove funzionalità
- **Checklist consolidata in tabella Anagrafiche** — la colonna "Moduli" è sostituita da "Checklist": un riepilogo compatto dei 7 passi di iscrizione (anagrafica completa, corso assegnato, moduli iscrizione/privacy firmati, primo pagamento, tessera FISR, certificato medico) direttamente nella tabella, con conteggio "N/7" e 7 pallini colorati (verde = fatto), senza dover aprire la scheda di ogni singolo atleta. Passa il mouse sopra per vedere il dettaglio di quali passi mancano.
- **Stato pagamenti mensili in tabella** — nuova colonna che segnala a colpo d'occhio se un atleta è "in regola" con la quota mensile o quanti mesi risulta arretrato, calcolato confrontando i mesi trascorsi da quando è iscritto con i pagamenti registrati in Amministrazione (causale contenente "quota"). È una stima basata sui dati già presenti, non un registro di rate separato: se serve un controllo puntuale mese per mese, è un possibile sviluppo futuro.
- **Eliminazione atleta spostata nella scheda singola** — il pulsante 🗑️ non è più nella tabella (per ridurre il rischio di click accidentali scorrendo l'elenco): ora si trova nella scheda di modifica dell'atleta, accanto al pulsante "Salva".

---

## v5.0.2 · Agosto 2026

### Fix
- **Verbale CD — esito della votazione poco chiaro** — il verbale generato non dichiarava esplicitamente l'approvazione della delibera: elencava solo chi aveva votato a favore e chi si era astenuto, senza concludere che la delibera risultava approvata. Ora il verbale afferma esplicitamente "la delibera risulta approvata" (all'unanimità, o a maggioranza con il dettaglio di favorevoli/astenuti).
- **Verbale CD — tipo "Altro" (testo libero)** — il testo inserito come "testo della delibera" veniva ripetuto nella premessa e poi sostituito, nella sezione DELIBERA vera e propria, da un generico "quanto esposto in premessa". Ora il testo inserito diventa direttamente il contenuto della delibera, come atteso.
- **A-capo non visualizzati** — corretto un errore che impediva la corretta formattazione degli a-capo nei campi a testo libero (ordine del giorno assemblea, testo delibera).

---

## v5.0.1 · Agosto 2026

### Fix
- **Menu a tendina del generatore verbali non aggiornati** — nei menu "Consigliere interessato" e "Responsabile nominato" del Verbale Consiglio Direttivo potevano comparire solo alcuni membri (es. il solo Presidente) se i dati del Consiglio Direttivo arrivavano da Firebase dopo l'apertura della pagina "Genera documenti", perché quella pagina non veniva mai aggiornata automaticamente. Ora si aggiorna da sola quando cambia la composizione del Consiglio Direttivo, senza però azzerare un verbale che si sta compilando se a cambiare sono dati non collegati (es. un nuovo atleta).

---

## v5.0.0 · Agosto 2026

### Nuove funzionalità
- **Consiglio Direttivo strutturato** — nuova sezione in "La mia struttura": elenco completo e ripetibile dei membri del Consiglio Direttivo (ruolo, dati anagrafici, CF, residenza, documento d'identità, rappresentanza legale, durata mandato), non più limitato al solo Presidente. Sostituisce i vecchi campi fissi "Presidente/Legale rappresentante" (migrati automaticamente al primo avvio) e resta valido sia in caso di cambio cariche sia per una nuova installazione dell'app presso un altro cliente.
- **Verbale Consiglio Direttivo generico** — nuovo generatore in "Genera documenti": intestazione, elenco presenti e quorum letti automaticamente dal Consiglio Direttivo, con sei tipologie di delibera pronte all'uso (apertura conto corrente, contratto co.co.co. istruttore/collaboratore, nomina Responsabile Safeguarding, convocazione assemblea, determinazione quote associative, e un tipo a testo libero per tutto il resto — regolamenti, deleghe, nomine di commissioni, provvedimenti disciplinari, modifiche statutarie). Gestione generica di conflitto d'interesse: ogni consigliere può essere segnato come "interessato" (astensione automatica dal voto) con eventuale delega di rappresentanza per la firma, riutilizzando lo schema già validato per i contratti co.co.co. di Presidente e Vicepresidente.
- **Contratti e documenti aggiornati** — il contratto co.co.co. sportivo e il contratto di sponsorizzazione ora leggono i dati del legale rappresentante dal nuovo Consiglio Direttivo invece dei vecchi campi fissi.

### File aggiunti
- `modulo_verbale_cd.html`

---

## v4.5.0 · Agosto 2026

### ⚠ Fix critico
- **Chiusura stagione azzerava entrate e uscite** — la funzione "Chiudi stagione" cancellava silenziosamente tutti i movimenti di Amministrazione (entrate/uscite), senza salvarne una copia da nessuna parte. Il bug contraddiceva quanto dichiarato fin dalla v4.2.0 (i dati finanziari dovevano restare esclusi dalla chiusura stagione) ed era presente dalla stessa versione, quindi ogni chiusura stagione eseguita da giugno 2026 in poi ha cancellato i dati finanziari. Ora la chiusura stagione non tocca più entrate/uscite: restano sempre visibili in Amministrazione, indipendentemente da quante stagioni vengono chiuse.

### Nuove funzionalità
- **Backup cloud automatico** — nuovo snapshot completo giornaliero salvato su Firebase (non solo in locale sul dispositivo/browser come il backup automatico esistente), consultabile e ripristinabile da Impostazioni → Backup automatico cloud, conservato per 90 giorni a rotazione. Pensato per proteggere da errori come quello descritto sopra: anche se un bug futuro dovesse cancellare dei dati, resta sempre disponibile una copia recente indipendente dal dispositivo usato.

---

## v4.4.2 · Agosto 2026

### Nuove funzionalità
- **Contratto co.co.co. sportivo** — nuovo documento in Genera documenti: collaborazione coordinata e continuativa nell'area del dilettantismo (art. 25, D.Lgs. 36/2021), con mansione, periodo, compenso e ore settimanali personalizzabili, campo per il firmatario ASD (utile quando il collaboratore è lo stesso Presidente e serve un delegato alla firma), avviso automatico se il compenso supera la soglia di esenzione IRPEF di 15.000 €/anno, pronto per la doppia firma.

### Fix — Importazione Google Sheets
- **Validazione link CSV** — se il link inserito restituisce una pagina HTML invece del CSV grezzo (es. link di condivisione anziché di export diretto), l'app lo segnala subito con un messaggio chiaro invece di tentare l'importazione e fallire silenziosamente.
- **Colonne Nome/Cognome non trovate** — se l'intestazione del CSV non contiene le colonne obbligatorie l'importazione si ferma con un errore esplicito, invece di segnalare genericamente "N righe saltate" senza indicarne il motivo.
- **Log di debug righe saltate** — le righe scartate durante l'importazione (nome o cognome mancante) vengono ora elencate in console con numero di riga e contenuto, per un controllo rapido.
- **Data di nascita e scadenza visita medica** — corretta la conversione dal formato italiano (GG/MM/AAAA) usato dal modulo Google al formato interno dell'app; risolve l'età mostrata come "NaN" e la categoria FISR calcolata in modo errato per gli atleti importati.
- **Campi Genitore/Tutore 1 e 2** — il riconoscimento delle colonne (nome, cognome, rapporto, CF, telefono, email) ora si basa sul contenuto dell'intestazione invece che su un testo fisso, quindi resta valido anche se le domande del modulo vengono rinominate (es. da "genitore" a "genitore / tutore").
- **Rapporto di parentela** — il valore importato (es. "Padre", "Madre") viene normalizzato per essere riconosciuto correttamente dal menu a tendina nella scheda atleta.
- **Corso/Squadra** — il testo libero del modulo viene ora confrontato con i corsi configurati in "Corsi e squadre" e collegato automaticamente se corrisponde; se non trova corrispondenza, l'app avvisa quali corsi vanno assegnati manualmente.
- **Istruzioni modale import CSV** — aggiornate per riflettere il riconoscimento delle colonne per nome (non più per posizione fissa) e il formato reale del modulo Google di iscrizione Spartans.

### Fix — Interfaccia
- **Colonna Azioni sempre visibile** — resta agganciata a destra durante lo scroll orizzontale in tutte le tabelle dell'app.
- **Intestazioni tabella sempre visibili** — tutte le tabelle ora hanno un'altezza massima con scroll interno: l'intestazione delle colonne resta agganciata in alto durante lo scroll verticale, e la barra di scorrimento orizzontale resta sempre raggiungibile senza dover scorrere fino in fondo a tabelle lunghe.
- **Footer versione** — spostato dentro la barra di sincronizzazione in fondo alla pagina; risolto un difetto per cui il footer bloccava lo scroll orizzontale/verticale sopra le tabelle.

### File aggiunti
- `modulo_cocoo_sportivo.html`

---

## v4.4.1 · Luglio 2026

### Nuove funzionalità
- **Auto-login demo via link** — aggiunto supporto al parametro `?demo=1` nell'URL: aprendo il link diretto alla demo l'app accede automaticamente con le credenziali demo senza inserirle manualmente. Utile per link condivisi su social e materiali promozionali.
- **Importazione Google Sheets — merge atleti esistenti** — l'importazione CSV non salta più gli atleti già presenti in anagrafica, ma ne aggiorna i campi vuoti con i dati presenti nel foglio. Il toast finale mostra il dettaglio: quanti aggiunti, quanti aggiornati, quanti saltati (già completi).

---

## v4.4.0 · Giugno 2026

### Nuove funzionalità
- **Nuova sezione Sponsor** — anagrafica completa (ragione sociale, CF/P.IVA, referente, contatti, logo, categoria: main sponsor, sponsor tecnico, sponsor ufficiale, fornitore-sponsor)
- **Contratto di sponsorizzazione** — descrizione, importo, periodicità (una tantum / annuale / mensile), data inizio e scadenza, stato pagamento
- **Integrazione con Amministrazione** — al contrassegno "Incassato" il contratto genera automaticamente un'entrata collegata, identificata in tabella con il badge 🤝 sponsor; aggiornamenti e cancellazioni si propagano automaticamente
- **Fattura sponsor** — documento generabile dalla tabella sponsor con numerazione progressiva, dati ASD e sponsor, dettaglio contratto e timbro digitale
- **Alert scadenza contratti** — i contratti sponsor in scadenza entro 60 giorni compaiono nelle Scadenze imminenti della dashboard
- **Oggetto della sponsorizzazione** — nuovo campo per descrivere le controprestazioni dell'ASD (es. apposizione marchio su divise, banner, social)
- **Contratto di sponsorizzazione generabile** — documento completo con dati ASD, dati sponsor, legale rappresentante di entrambe le parti, oggetto, durata e corrispettivo, pronto per la doppia firma
- **Dati Presidente/Legale rappresentante ASD** — nuova sezione in "La mia struttura" per inserire i dati anagrafici del presidente, riutilizzati automaticamente nei contratti
- **Allegato contratto firmato** — campo per archiviare il link al contratto firmato e scansionato (es. Google Drive) nella scheda sponsor

### Fix
- **Ricerca globale** — gli sponsor sono ora indicizzati nella ricerca globale (ragione sociale, categoria, referente, descrizione contratto)
- **Contratto sponsor** — corretto il Codice Fiscale dell'ASD (mostrava erroneamente quello del Presidente) e il campo "Luogo" in epigrafe (mostrava il numero civico invece della città)

### Altre modifiche
- **Documento d'identità in anagrafica** — nuovi campi tipo, numero e scadenza documento per atleti, utili per gare e procedure FISR
- **Documenti struttura con link Drive** — la tab Documenti di "La mia struttura" ora permette di allegare data e link al file per ogni documento
- **Rimossa tab Sport** da "La mia struttura" (non utilizzata)
- **Scadenza CI Presidente** — aggiunto campo data di scadenza della carta d'identità del Presidente/Legale rappresentante
- **Lettera di incarico** — nuovo documento in Genera documenti per membri dello staff: incarico per prestazioni sportive dilettantistiche (art. 67/69 D.P.R. 917/1986), con mansione presa automaticamente dal ruolo, periodo e compenso personalizzabili, pronta per la doppia firma
- **Formazione Safeguarding per lo staff** — nuovi campi in Anagrafica → Staff (data formazione, scadenza, attestato) ai sensi del Regolamento FISR per la Tutela dei Tesserati; badge di stato in tabella (✓ valida, ⚠ scaduta, ✗ mancante) e alert in dashboard per le scadenze imminenti
- **Nomina Duty Officer Safeguarding** — nuovo documento in Genera documenti per formalizzare la nomina del responsabile Safeguarding della società (artt. 17-18 Regolamento FISR), con elenco dei compiti e doppia firma
- **Informativa Safeguarding nel modulo di iscrizione** — il modulo di iscrizione ai corsi include ora una seconda pagina con il riepilogo delle politiche di tutela dei tesserati adottate dall'ASD, in conformità al Regolamento FISR, con dichiarazione di presa visione da firmare
- **Comunicati Campionati FISR** — nuova tab in Comunicati FISR, affiancata a quella esistente, con i comunicati ufficiali relativi ai campionati di hockey inline (11 stagioni storiche disponibili)
- **Fix numerazione Comunicati Campionati** — i comunicati con prefisso "CUC" (es. CUC 039) ora mostrano correttamente il proprio numero invece di "000"
- **Lettura comunicati FISR per utente** — lo stato "letto/nuovo" dei comunicati ora è sincronizzato su Firebase per ogni account, invece che salvato solo sul singolo dispositivo: ogni utente vede chi altro nello staff ha già letto i comunicati, e fino a quale numero
- **Gestione manuale stagioni FISR** — nuovo pulsante "⚙️ Gestisci stagioni" in Comunicati FISR per aggiungere il link di una nuova annata sportiva non ancora presente nell'app, o correggere un link non più funzionante, senza dover attendere un aggiornamento dell'app
- **Fix proxy CORS Comunicati FISR** — risolto un bug per cui i comunicati più recenti non comparivano a causa della cache del servizio proxy esterno; aggiunto cache-busting e un proxy di riserva automatico
- **Guida aggiornata** — nuove voci per documenti, checklist iscritto, archivio stagioni, compleanni, gestione sponsor, lettera di incarico, Safeguarding e modalità demo

### File aggiunti
- `modulo_fattura_sponsor.html`
- `modulo_contratto_sponsor.html`
- `modulo_incarico.html`
- `modulo_duty_officer.html`

---

## v4.3.0 · Giugno 2026

### Nuove funzionalità
- **Accesso demo** — login con `demo@spartansmanager.app` attiva la modalità demo: dati dimostrativi su nodo Firebase separato (`/spartans/demo/`), completamente isolato dai dati reali
- **Sola lettura** — tutte le operazioni di scrittura (salvataggio, eliminazione, importazione) sono bloccate in modalità demo con avviso toast
- **Dataset dimostrativo** — ASD Demo Hockey Inline, Milano: 15 atleti (9 Under 12 + 6 Avviamento), 3 staff, 20 eventi, presenze, abbonamenti, valutazioni e fornitori pre-popolati
- **Banner demo** — badge arancione lampeggiante 🎭 MODALITÀ DEMO in basso a destra durante la navigazione

---

## v4.2.0 · Giugno 2026

### Nuove funzionalità
- **Avvisi compleanno in Prossimi eventi** — soci e staff con compleanno entro 14 giorni appaiono in dashboard con sfondo azzurro, età che compiono e label Oggi! 🎉 / Domani / fra Ngg
- **Snapshot completo alla chiusura stagione** — alla chiusura vengono salvati integralmente: atleti, staff, corsi, presenze, eventi, abbonamenti, piani e valutazioni atleti; i dati sono navigabili in futuro senza limiti
- **Archivio stagione a 5 tab** — il dettaglio di ogni stagione archiviata mostra: Riepilogo (statistiche chiave + risultato sportivo), Atleti (tabella completa con tessere), Presenze (classifica % per atleta con barra visiva), Valutazioni (punteggi fisico/tecnico/tattico per ogni atleta al momento della chiusura), Eventi (calendario gare e allenamenti)
- **Badge snapshot** — indicatore visivo "✓ Snapshot completo" vs "⚠ Snapshot parziale" per distinguere le stagioni archiviate con la nuova logica da quelle precedenti
- **Separazione stagione sportiva / anno fiscale** — i dati finanziari (entrate/uscite) sono esclusi dallo snapshot di stagione; la chiusura fiscale sarà gestita separatamente in Amministrazione
- **Avvisi compleanno in Prossimi eventi** — soci e staff con compleanno entro 14 giorni appaiono in dashboard con sfondo azzurro, età che compiono e label Oggi! 🎉 / Domani / fra Ngg

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
