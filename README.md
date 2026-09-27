# ListaViva

ListaViva è un'app mobile per organizzare la spesa di un nucleo domestico. Il primo prodotto è una lista condivisa rapida e utilizzabile anche offline; lo storico degli acquisti permette poi di suggerire, con una spiegazione, cosa potrebbe mancare in casa.

> **Stato del progetto:** pianificazione tecnica. Questo repository contiene la documentazione iniziale; l'applicazione non è ancora implementata. Nome, metriche e ipotesi commerciali sono da validare con utenti reali.

## Documentazione

- [Business plan e PRD v0.1](docs/ListaViva_Business_Plan_PRD_v0.1.docx): visione, requisiti, metriche e backlog.
- [Report tecnico](docs/Report_tecnico_ListaViva.docx): proposta di architettura, stack, sincronizzazione, dati, sicurezza e test.
- [Roadmap e OKR](docs/ROADMAP.md): milestone, criteri di rilascio e timeline indicativa.

## Ambito del primo rilascio

La prima alpha introduce account, nuclei domestici e inviti, più liste condivise, aggiunta e spunta degli articoli, salvataggio locale e riconciliazione dopo la riconnessione. L'MVP successivo aggiunge storico per nucleo, autocomplete e suggerimenti deterministici con spiegazione e feedback. Inventario stimato, barcode, scontrini e funzioni di benessere arrivano in versioni distinte, solo dopo la validazione delle fasi precedenti.

## Architettura proposta

| Componente | Scelta iniziale | Responsabilità |
| --- | --- | --- |
| App iOS e Android | React Native, Expo, TypeScript | Interfaccia, operazioni ottimistiche e modalità spesa |
| Archivio sul dispositivo | SQLite tramite `expo-sqlite` | Viste locali e coda delle operazioni offline |
| Credenziali sul dispositivo | `expo-secure-store` | Conservazione dei token di sessione |
| API | NestJS, REST e notifiche di cambiamento WebSocket | Validazione, autorizzazione, comandi e sync |
| Persistenza | PostgreSQL e Drizzle | Dati autorevoli, vincoli, transazioni e migrazioni |
| Identità | Supabase Auth | Login e gestione delle sessioni |
| Web | Next.js, quando serve | Landing, waitlist ed eventuale console operativa |

Queste sono **scelte proposte**, non dipendenze già installate. Il backend parte come monolite modulare con confini Identity, Household, Shopping, Catalog, Purchase, Suggestions e Notifications. PostgreSQL è la fonte autorevole. Il client mantiene una coda di comandi con `operation_id`; il server applica ogni operazione una sola volta e restituisce lo stato canonico. WebSocket segnala che ci sono novità, mentre una API basata su cursore recupera le modifiche perse durante l'assenza di rete.

Ogni accesso alle liste verifica sul server l'appartenenza al nucleo. Le quantità concorrenti richiedono operazioni di incremento o decremento atomiche; le sostituzioni assolute usano una revisione attesa e restituiscono un conflitto esplicito quando è obsoleta. Il completamento di una lista e la creazione degli acquisti avvengono nella stessa transazione.

## Principi di prodotto e dati

- La collaborazione di base resta semplice e utilizzabile gratuitamente; il valore premium va provato prima di implementare la fatturazione.
- I suggerimenti partono da regole verificabili e mostrano il motivo. L'utente può aggiungere, ignorare, rimandare o sopprimere un suggerimento.
- Lo stock **stimato** è distinto dallo stock **verificato**. Una data di scadenza inferita non viene presentata come una data reale di sicurezza alimentare.
- Preferenze che possono rivelare dati sanitari restano fuori dall'MVP e richiedono una valutazione separata prima di un eventuale rilascio.

## Organizzazione prevista del codice

```text
apps/
  mobile/       # Expo e React Native
  api/          # NestJS
  landing/      # sito e waitlist, quando necessari
packages/
  contracts/    # schemi e tipi del protocollo pubblico
docs/           # PRD, report tecnico e roadmap
```

Questa struttura verrà introdotta con la prima vertical slice. I modelli del database non vengono importati direttamente nell'app mobile: il contratto API è versionato e verificato separatamente.

## Prima vertical slice e gate

Implementare, nell'ordine: login → creazione del nucleo → invito → lista → aggiunta e spunta offline → riconnessione di due dispositivi → completamento → storico. Prima di invitare i nuclei alpha, verificare retry idempotenti, conflitti sulle quantità, revoca della membership e isolamento dei dati tra due nuclei.

La [roadmap](docs/ROADMAP.md) indica obiettivi e soglie di validazione. Le durate sono stime part time, non date di consegna impegnative.


## Sviluppo con sub-agent

Il [sistema multi-agent](agents/README.md) definisce PM, orchestratore e specialisti, con skills del repository, backlog M1–M6 e workflow issue → branch → PR. Ogni task viene revisionato da tetosever e il merge resta manuale. La configurazione di progetto è in `.codex/`; i comandi di verifica e avvio sono nella guida.
