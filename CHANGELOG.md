# Spartans Manager — Changelog

---

## v6.2.0 · Ottobre 2026

### Nuovo — Saldo separato tra conto corrente e cassa
- **Segnalato dall'utente**: il Riepilogo di Amministrazione mostrava solo il saldo totale, senza distinguere tra conto corrente e cassa contanti.
- **Regola di attribuzione**: i movimenti (entrate e uscite) con metodo **Bonifico, Carta, POS, Altro** aggiornano il saldo del conto corrente; quelli con metodo **Contanti** aggiornano il saldo della cassa. Un movimento senza metodo è attribuito alla cassa; un testo libero non riconosciuto al conto corrente.
- **Nuove card nel tab Riepilogo**: "Saldo conto corrente" e "Saldo cassa", ciascuna con entrate e uscite; il saldo totale resta invariato ed è sempre la somma dei due.
- **Nessuna migrazione dati**: il saldo è derivato dal campo `metodo` già presente su ogni movimento, quindi vale retroattivamente per lo storico. Per spostare un movimento da un conto all'altro basta modificarne il metodo.
- **Prima nota**: accanto al saldo del periodo compaiono il saldo del periodo per conto corrente e per cassa.
- **Coerenza dati**: l'entrata generata da un contratto sponsor registrava il metodo come `bonifico` (minuscolo); ora `Bonifico`. Il confronto del metodo ignora comunque maiuscole/minuscole e accetta diciture come "Bonifico bancario". Il metodo digitato nei rimborsi staff viene riportato alla dicitura standard quando coincide.
- **Saldo di apertura**: indicati dall'amministratore i saldi reali al 05/10/2026 (conto corrente €1.670,00, cassa €80,00). Al primo caricamento dei dati l'app calcola una *rettifica di apertura* per ciascun conto = saldo reale − saldo dei movimenti con data ≤ 05/10/2026, e la salva in `saldiApertura`. Saldo mostrato = rettifica + movimenti; alla data di riferimento coincide quindi con i valori reali e da lì segue i movimenti. L'operazione è deterministica (idempotente anche con più utenti connessi) e avviene una volta sola.
- **Riallinea saldi**: pulsante nel Riepilogo per ricalcolare la rettifica inserendo i saldi reali del momento (es. dopo una riconciliazione con l'estratto conto).
- **Nota**: Totale entrate e Totale uscite restano la somma dei movimenti; il Saldo totale include la rettifica, quindi può differire da entrate − uscite. La Prima nota mostra i flussi del periodo e non include la rettifica.

### Correzione — Calendario mensile: intestazioni dei giorni
- **Segnalato dall'utente**: nella vista mensile la riga con i nomi dei giorni (`GGCORTE`) partiva da Domenica, mentre la griglia usa l'offset lunedì-first `(getDay()+6)%7`; ogni data compariva quindi sotto il giorno sbagliato (es. giovedì 1 ottobre sotto "MER"). Gli eventi erano salvati nei giorni corretti (martedì e giovedì per gli allenamenti): il difetto era solo di visualizzazione.
- **Fix**: `GGCORTE` ora è `Lun–Dom`. Il calcolo dell'offset non è stato modificato. `GGCORTE` è usato solo in `renderCalendar()`; la generazione degli allenamenti (`generateAllenamentiCorso`) usa una mappa propria e non è coinvolta.
- **Colonne uniformi**: `.cal-grid` passa da `repeat(7,1fr)` a `repeat(7,minmax(0,1fr))` e `.cal-day` riceve `min-width:0; overflow:hidden`, così le etichette lunghe non allargano la colonna e vengono troncate con i puntini (già previsti da `.cal-event`). La riga delle intestazioni usa la stessa classe e resta allineata alla griglia.
- Nessun cambio di versione: correzione inclusa nella 6.2.0.

---

## v6.1.5 · Ottobre 2026

### Correzione — Card Dashboard: solo i comunicati realmente nuovi
- **Segnalato dall'utente il giorno stesso della v6.1.4**: la card "Comunicati FISR" in Dashboard mostrava tutti i comunicati non ancora segnati come "visti" da nessuno in struttura, non i soli nuovi arrivi — un difetto di design, non un bug di codice: se il pulsante "✓ Segna tutti come visti" non viene mai usato, quell'elenco con il tempo diventa l'intero storico della stagione.
- **Nuova definizione di "nuovo"**: ora si confronta ogni caricamento dei comunicati generali con quello precedente, e la card mostra solo i comunicati apparsi nel frattempo — in pratica nessuno la maggior parte dei giorni, uno o due quando la FISR pubblica davvero qualcosa. Il badge sul menu laterale e la lista completa nella pagina Comunicati FISR continuano invece a basarsi su "letto/non letto", comportamento diverso ma corretto per quel contesto.
- **Posizione**: spostata dalla colonna sinistra (sopra "Scadenze imminenti") alla colonna destra, subito sotto il Riepilogo economico.

---

## v6.1.4 · Ottobre 2026

### Nuovo — Comunicati FISR non letti in Dashboard
- **Nuova card "📋 Comunicati FISR" in Dashboard**: il controllo automatico all'apertura dell'app (già esistente da prima, limitato a una verifica di rete al giorno per non sovraccaricare i servizi di CORS-proxy pubblici e condivisi con cui l'app legge il sito FISR, che non espone un'API) ora mostra i comunicati generali non ancora letti direttamente nella Dashboard, non solo come numero sul badge del menu laterale.
- **"Non letto" = stato condiviso, non locale**: si basa sul pulsante "✓ Segna tutti come visti" già presente nella pagina Comunicati FISR, salvato per l'intera struttura (non per singolo dispositivo/utente). Finché nessuno lo ha mai usato, la card non mostra nulla — evita falsi allarmi su comunicati che in realtà sono sempre stati lì, non appena pubblicati.
- **Nota su "ad ogni apertura"**: la *verifica in dashboard* avviene ad ogni apertura; il *download* dai proxy resta volutamente limitato a una volta al giorno — scaricarlo ad ogni login di ogni utente avrebbe moltiplicato il traffico sui proxy pubblici appena stabilizzati in v6.1.3, vanificando quel fix.

---

## v6.1.3 · Ottobre 2026

### Fix — Proxy CORS principale sempre in errore 403
- **Causa reale trovata, non più un'ipotesi**: il fallimento "ogni tanto" dei comunicati FISR non era un sovraccarico dei servizi pubblici condivisi (ipotesi della v6.1.2, confermata insufficiente dal log della console del browser fornito dall'utente). `corsproxy.io` ha cambiato il proprio formato richiesto e ora impone il parametro `?url=<indirizzo>`: il codice costruiva l'indirizzo come `https://corsproxy.io/?<indirizzo>`, privo della chiave `url=`, causando un errore `403 Forbidden` deterministico su **ogni** richiesta al proxy principale, non occasionale.
- **Il terzo proxy aggiunto in v6.1.2 non risolveva il problema**: mascherava solo in parte il sintomo quando anche i proxy di riserva erano temporaneamente irraggiungibili, ma il proxy principale restava comunque sempre in errore.
- **Fix**: corretto il formato dell'indirizzo passato a `corsproxy.io` aggiungendo il parametro `url=` mancante.

---

## v6.1.2 · Ottobre 2026

### Fix — Comunicati FISR, scaricamento intermittente
- **Terzo proxy CORS di riserva** (`api.codetabs.com`) aggiunto ai due esistenti (`corsproxy.io`, `api.allorigins.win`). Il sito FISR non espone un'API: l'app legge la pagina pubblica tramite servizi di CORS-proxy gratuiti e condivisi con chiunque altro li usi nel mondo, senza alcuna garanzia di disponibilità — da qui i fallimenti "ogni tanto" (non un bug nel parser, che darebbe un fallimento costante, non intermittente). Il terzo tentativo riduce la probabilità che tutti i proxy risultino irraggiungibili nella stessa richiesta.
- **Non risolto alla radice**: resta una dipendenza da infrastruttura pubblica non garantita. Se le interruzioni restano frequenti, la soluzione solida è un proxy dedicato (es. un Cloudflare Worker gratuito, sotto il controllo dell'associazione e non condiviso con altri utenti).

---

## v6.1.1 · Ottobre 2026

### Correzione — Fattura elettronica obbligatoria, non più esonerata
- **La v6.1.0 presupponeva un esonero non più in vigore**: la soglia dei 65.000 € di ricavi commerciali (DL 119/2018) che esentava le ASD in regime 398/91 dalla fattura elettronica è stata abrogata gradualmente dal DL 36/2022 (Decreto PNRR 2) — obbligo dal 1° luglio 2022 per chi supera 25.000 €, e dal 1° gennaio 2024 per **tutte** le ASD con partita IVA, senza più alcuna soglia. La fattura ordinaria di carta introdotta in v6.1.0 non ha quindi più valore fiscale per le sponsorizzazioni.
- **Generatore XML FatturaPA**: il registro fatture (Amministrazione → 📄 Fatture) genera ora, per ogni riga (fattura, nota di credito, nota di debito), il file XML nel formato FatturaPA (FPR12) da caricare manualmente sul servizio gratuito "Fatture e Corrispettivi" dell'Agenzia delle Entrate — l'app non effettua alcun invio automatico al Sistema di Interscambio.
- **Nuovi campi richiesti dal tracciato XML**: "La mia struttura" ha Provincia e Regime fiscale (RF01 ordinario / RF19 forfettario); la scheda sponsor ha CAP, Comune, Provincia, Codice Destinatario SdI e PEC — tutti necessari per compilare correttamente l'anagrafica del cessionario nel file.
- **Da verificare prima del primo invio reale**: l'XML è stato costruito seguendo la documentazione pubblica del tracciato FatturaPA (nomi ed ordine degli elementi), ma non è stato validato contro lo schema XSD ufficiale da questa applicazione né da un validatore esterno. Prima di trasmettere una fattura vera, usa la funzione "Controlla file" del portale Entrate (segnala eventuali errori di formato senza alcuna conseguenza fiscale) oppure fai verificare il file al commercialista.

---

## v6.1.0 · Ottobre 2026

### Nuovo — Impianto fatture sponsor
- **Registro fatture dedicato** (Amministrazione → 📄 Fatture) — la precedente "🧾 Genera fattura" nella scheda sponsor apriva solo un documento stampabile senza lasciare traccia nel gestionale: non c'era modo di sapere quali numeri erano già stati usati, né di correggere un errore se non rigenerando lo stesso numero (rischio di doppioni). Ora ogni fattura emessa viene registrata in modo permanente (numero, data, sponsor, imponibile, aliquota IVA, imposta, totale), con numerazione progressiva dedicata — separata da quella delle ricevute — che si azzera a ogni nuovo anno (formato `NNNN/AAAA`, es. `0001/2026`) e non torna mai indietro una volta avanzata.
- **Scomposizione IVA corretta** — il documento non riporta più la dicitura "operazione fuori campo IVA", non corretta per le sponsorizzazioni (che sono imponibili IVA ad aliquota ordinaria, con detrazione forfettaria del 50% solo sul lato della liquidazione interna dell'associazione, non sull'importo addebitato allo sponsor). Ora il modulo calcola automaticamente imponibile, imposta e totale a partire dall'importo complessivo incassato indicato nel contratto sponsor (resta quello il dato che alimenta l'entrata in Amministrazione), con aliquota IVA configurabile per singolo sponsor (default 22%).
- **Nota di credito / nota di debito al posto dell'"annulla"** — a differenza delle ricevute, una fattura non si annulla né si rinumera mai una volta emessa. Due nuovi pulsanti nel registro (➖ nota di credito, per importi in diminuzione o fatture duplicate/errate; ➕ nota di debito, per importi aggiuntivi) generano un nuovo documento che riferisce sempre numero e data della fattura originale, consumando un numero della stessa sequenza annuale. La fattura originale resta sempre visibile e intatta nello storico.
- **Fattura ordinaria, non elettronica** — l'app non genera né trasmette alcun file XML/SdI. Verificato (fonti pubbliche, DL 119/2018): le ASD in regime 398/91 con ricavi commerciali annui (sponsorizzazioni comprese) non superiori a 65.000 € sono esonerate dall'obbligo di fattura elettronica — una fattura ordinaria stampata/PDF, con il contenuto minimo richiesto dall'art. 21 DPR 633/1972, è sufficiente. Da riconfermare con il commercialista che questa soglia sia rimasta invariata dopo la riforma IVA 2026 (passaggio da esclusione a esenzione, obbligo di partita IVA) prima di superarla o in caso di dubbio.
- **Nuovi campi in "La mia struttura"**: CAP e IBAN, riportati automaticamente sulle fatture generate.

> Prima di generare la prima fattura reale con questa versione: il vecchio contatore `spartans/contatori/fatture` (usato dalla versione precedente, priva di registro) va eliminato dalla Console Firebase — conteneva solo numeri di prova mai effettivamente registrati da nessuna parte. La nuova numerazione annuale parte da zero in autonomia non appena il vecchio nodo viene rimosso.

---

## v6.0.2 · Ottobre 2026

### Fix — Categoria "Iscrizione" mancante nei movimenti
- **Nuova categoria "Iscrizione associativa"** nel modulo entrate/uscite — prima l'iscrizione andava registrata come "Quota associativa" (unica categoria disponibile che si avvicinava), ma questo la faceva sommare al conteggio mensile delle quote usato per gli arretrati in Dashboard, come se fosse una rata ricorrente invece che un versamento una tantum. Rinominare solo la causale non risolveva il problema perché il controllo guarda anche il campo Categoria, non solo il testo libero. Ora selezionando "Iscrizione associativa" come categoria l'importo resta tracciato in Amministrazione ma esce dal calcolo di regolarità mensile.

---

## v6.0.1 · Ottobre 2026

### Fix — Mesi arretrati conteggiati in doppio dopo un cambio di piano
- **Corretto il doppio conteggio del mese di passaggio tra due abbonamenti** — quando a un atleta viene assegnato un nuovo piano (es. un aumento di quota mensile), il mese in cui avviene il cambio veniva contato due volte nel calcolo "mesi arretrati" in Dashboard: una come ultimo mese del piano precedente, una come primo mese di quello nuovo. Riscontrato dopo l'aumento della quota mensile a €40: due atleti risultavano con un mese arretrato in più del dovuto, e il problema peggiorava (un mese arretrato in più per ogni piano aggiuntivo) se si provava ad "aggiustare" la situazione assegnando un ulteriore abbonamento. Il calcolo ora chiude il periodo del piano uscente all'ultimo giorno del mese precedente a quello in cui inizia il piano successivo, così ogni mese viene attribuito a un solo piano e non si somma più.

> Nessun impatto sugli atleti che non hanno mai cambiato piano/abbonamento: per loro il calcolo era già corretto. L'anomalia si manifestava solo da quando esisteva più di un'assegnazione di abbonamento per lo stesso atleta.

---

## v6.0.0 · Settembre 2026

### Fix — Numerazione ricevute
- **Le entrate a €0 non propongono più una ricevuta** — un'entrata registrata con importo zero (es. quota esonerata/agevolata) non fa più scattare la richiesta automatica "Generare la ricevuta?": non essendoci un incasso da documentare, non deve consumare un numero della sequenza ufficiale. L'esonero dal pagamento resta comunque tracciato in Amministrazione e va formalizzato con una delibera del Consiglio Direttivo.
- **Annullamento reale delle ricevute** — nel registro (Amministrazione → Ricevute) ogni riga mostra ora uno stato (✓ valida / 🚫 ANNULLATA / 🧪 TEST) e un nuovo pulsante "🚫 Annulla", che richiede un motivo e marca la ricevuta come annullata senza mai alterare numero, data o importo originali. Sostituisce la precedente prassi manuale di modificare a mano il testo della causale.
- **Modalità test separata dalla numerazione ufficiale** — la card "Ricevuta pagamento" in Genera documenti ha una nuova casella "🧪 Genera in modalità test": i documenti generati così sono numerati "TEST-0001" ecc. su un contatore Firebase indipendente e il PDF è marcato "DOCUMENTO DI PROVA — NON VALIDO", così una verifica di funzionamento non incrocia mai più, per errore, la numerazione delle ricevute realmente emesse.
- **Emissione manuale con numero forzato** — nel tab "🧾 Ricevute" una nuova sezione "⚠️ Emissione manuale con numero forzato" permette, solo per regolarizzazioni concordate con il commercialista, di emettere una ricevuta scrivendo direttamente il numero (senza passare dal contatore automatico, che non può più tornare indietro una volta avanzato). Include un pulsante che compone in automatico la causale di regolarizzazione concordata, e un avviso se il numero indicato è già presente nel registro. Le ricevute emesse così sono segnalate con il badge "✍️ manuale". Il socio/atleta non è più obbligatorio: è possibile indicare un **nominativo libero** (donatore esterno non tesserato, oppure un nominativo di prova come "Prova tecnica" per i numeri da annullare), e la ristampa di queste ricevute (🔄) funziona anche senza un socioId collegato.

> Queste correzioni chiudono le "Azioni correttive" richiamate nella nota interna di regolarizzazione della numerazione delle ricevute (Settembre 2026 — commercialista dott. Francesco Chimienti), propedeutiche all'emissione delle ricevute nn. 9–22 e all'annullamento delle nn. 1–8/53/57-58.

### Guida interna
- Aggiornate le voci "Generare una ricevuta di pagamento", "Registro Ricevute" e "Registrare un abbonamento o una quota gratuita" nella sezione Sistema → Guida, e aggiunta la voce "Emissione manuale con numero forzato (regolarizzazione)", per riflettere la modalità test, l'annullamento reale, l'emissione manuale e l'esclusione delle entrate a €0 dalla generazione automatica.

---

## v5.9.1 · Settembre 2026

### Fix — Anagrafiche soci su smartphone
- **Vista a card leggibile** — da smartphone la tabella Atleti (20 colonne) diventava un elenco di numeri e spunte senza etichetta, illeggibile senza affiancare la testata. Ogni valore ora mostra il nome del campo sopra di sé, e la card si apre con nome e maglia dell'atleta come intestazione. Per restare compatta, la card mostra solo i campi utili a colpo d'occhio (età, categoria, corso, abbonamento, pagamenti, stato); tessere, visita medica, assicurazione e checklist dettagliata restano un tocco più in là, nella scheda di modifica (✏️), già raggiungibile da ogni card.

---

## v5.9.0 · Settembre 2026

### Nuove funzionalità
- **Avviso di presenza multi-utente** — quando un altro utente è collegato all'app, compare accanto allo stato di sincronizzazione un indicatore "👥 N collegati" (con l'elenco delle email al passaggio del mouse/tocco), e un toast avvisa a ogni nuovo collegamento o scollegamento. Se quell'utente sta effettivamente scrivendo sul database (ha una modifica in corso di salvataggio), compare in alto un banner lampeggiante con il suo nome, per evitare di salvare nello stesso momento sovrascrivendo a vicenda le rispettive modifiche.

### Miglioramenti
- **Verbale Consiglio Direttivo — "Varie ed eventuali" automatico** — l'ordine del giorno generato include ora sempre, come ultimo punto, "Varie ed eventuali", in linea con la prassi degli altri facsimile verbali FISR/Skate Italia.

---

## v5.8.0 · Settembre 2026

### Nuove funzionalità
- **Storico Abbigliamento** — nuova scheda "🧥 Abbigliamento" nell'anagrafica di ogni atleta, per registrare ogni capo/attrezzatura assegnato: 🛒 acquisto, 🎁 fornitura gratuita o 🔄 prestito di materiale didattico. Ogni evento ha articolo, data, note e — solo per gli acquisti — importo. I prestiti restano segnati come "in corso" finché non vengono marcati come restituiti (con relativa data), e finché sono aperti compaiono automaticamente in un nuovo promemoria di Dashboard, "🔄 Prestiti materiale in corso", con l'elenco di chi ha in mano cosa e da quando — utile per non perdere traccia del materiale didattico dato in prestito (es. caschi, pattini, protezioni condivise).

---

## v5.7.1 · Settembre 2026

### Fix — Book allenamenti
- **Istruttori selezionabili corretti** — il campo Istruttore (sia nella modale "Nuova sessione" sia nel filtro dell'elenco) proponeva tutto lo Staff, inclusi dirigenti, segretario, tesoriere e altre cariche non necessariamente abilitate all'insegnamento. Ora attinge solo dai nominativi registrati in "Maestri/Tecnici" — la stessa lista già usata per assegnare l'istruttore a un corso.

---

## v5.7.0 · Settembre 2026

### Nuove funzionalità
- **Book allenamenti** — nuova sezione "📔 Book allenamenti" per annotare esercizi e idee di ogni sessione. Ogni voce ha data (assegnabile liberamente, non legata a un corso o a un evento specifico) e istruttore, con quattro fasi strutturate (🔥 Riscaldamento, 🎯 Tecnica, 🧠 Tattica, 🏁 Defaticamento/Partitella) più un campo di note libere. Filtrabile per istruttore e per mese, visibile e compilabile da tutto lo staff — non solo da chi ha scritto una determinata sessione.

---

## v5.6.1 · Settembre 2026

### Fix — Scadenze imminenti
- **Abbonamenti doppi e falsi promemoria per chi non ha ancora pagato** — la card "Scadenze imminenti" mostrava un promemoria per ogni singolo record di abbonamento assegnato, non per atleta: con più abbonamenti in sequenza sulla stessa persona (es. quota iscrizione + quota mensile), comparivano più righe per lo stesso atleta. Inoltre il promemoria scattava sulla data di scadenza nominale del record, creata al momento dell'assegnazione del piano indipendentemente da qualunque pagamento — risultando fuorviante per chi non aveva ancora versato nulla. Rimossi gli abbonamenti da questa card: la regolarità dei pagamenti (basata sulle entrate realmente registrate, senza doppioni) è già gestita correttamente dalla card "💳 Quote mensili arretrate". Restano invece qui, senza modifiche, le vere scadenze senza equivalente altrove: tessere, visite mediche, assicurazioni, contratti sponsor ed eventi.

---

## v5.6.0 · Settembre 2026

### Nuove funzionalità
- **Spazio utilizzato** — nuova card in Impostazioni ("📊 Calcola") che stima lo spazio occupato su Firebase, scomposto per capire cosa lo fa crescere: dati correnti del database, di cui allegati incorporati (foto profilo e file caricati direttamente, non i link Drive — quelli sono solo testo), backup automatici cloud (con conteggio delle copie), e backup locali sul dispositivo. Utile prima di popolare un dataset ricco (es. la futura demo) per capire quanto pesa, e per individuare se conviene preferire i link Drive invece di allegare file di grandi dimensioni. Google Drive non è invece verificabile dall'app: quello spazio è gestito interamente dal tuo account Google.

---

## v5.5.1 · Settembre 2026

### Fix
- **Scadenze abbonamento non rispettavano lo stato dell'atleta** — la card "Scadenze imminenti" in Dashboard segnalava il rinnovo dell'abbonamento anche per atleti Sospesi o attualmente dentro un periodo di inattività registrato, cosa che non ha senso (non c'è nulla da rinnovare per chi non è al momento operativo). Ora questi casi vengono esclusi automaticamente.
- **Scadenze imminenti limitate a 8 voci, senza indicazione delle altre** — con più di 8 scadenze contemporanee, le successive sparivano silenziosamente dalla vista. Ora la card mostra tutte le scadenze entro i 60 giorni, con scroll interno se sono numerose, invece di troncarle senza avviso.

### Semplificazione — Abbonamenti
- **Rimossi i campi "Importo pagato" e "Metodo" dalla sezione Abbonamenti** — erano scollegati dal reale tracciamento dei pagamenti (che vive in Amministrazione → Entrate, la stessa fonte usata per "Pagamenti mensili" in Anagrafiche): risultavano popolati solo se inseriti manualmente da questa sezione, sempre a €0,00 se il piano veniva assegnato dalla scheda atleta — la stessa incoerenza segnalata. La sezione "Abbonamenti soci" resta comunque utile come elenco di tutti i piani assegnati e per correggerne/eliminarne uno specifico.
- **Statistiche abbonamenti ricalcolate sulla fonte corretta** — "Totale incassato", "Incasso per piano" e "Incassi per mese" ora si basano sulle entrate reali registrate in Amministrazione, non più sul campo "pagato" appena rimosso: i numeri restano quindi accurati e coerenti con il resto dell'app.

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
