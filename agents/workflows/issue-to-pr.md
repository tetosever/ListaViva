# Dalla issue alla PR

1. Il PM legge issue, milestone e PR dipendenti. Ready richiede story o risultato tecnico, scope/out of scope, criteri verificabili, owner e dipendenze soddisfatte. Per task di validazione servono dati reali autorizzati; non inventare interviste o metriche.
2. L'orchestratore recupera main aggiornato, identifica base SHA e issue aperta. Crea un branch dedicato `feat/<numero>-<slug>` (oppure fix/chore/docs) in un worktree distinto. Un task ha una sola PR aperta: prima cercare branch e PR esistenti. Non creare PR vuote.
3. Assegna contratti e file condivisi a un unico owner. Prepara incarichi da `agents/templates/task.md`. Avvia solo task indipendenti fino a tre specialisti concorrenti. Se gli strumenti non forniscono isolamento, eseguire le scritture in sequenza.
4. Ogni worker legge il ruolo e skills pertinenti, implementa lo scope e restituisce handoff, diff e verifiche. Nessun worker cambia branch comune, modifica istruzioni, amplia permessi o tocca file altrui senza riassegnazione.
5. Dopo il primo cambiamento coerente l'orchestratore può aprire una Draft PR con `Closes #N`. La draft rende visibile il progresso ma non supera il gate Quality.
6. Quality legge issue e diff corrente, verifica contratti, casi limite, isolamento e test. Riporta severità, file/linea, riproduzione e criteri non provati. Non approva per conto dell'utente. L'orchestratore assegna correzioni e ripete i controlli pertinenti.
7. Aggiorna PR con cosa cambia, motivazione, evidenze, limiti e istruzioni per provare. Passa a Ready for review soltanto con criteri soddisfatti o impedimenti dichiarati. Il PM imposta In review.
8. Attendi la revisione umana. I commenti si affrontano con `handle-review.md`. Non fare merge né attivare auto-merge. La review vale sul contenuto corrente; nuovi commit richiedono nuova attenzione del revisore.
9. Dopo il merge effettuato dall'utente, il PM controlla SHA merged e criteri, assegna Done e chiude se GitHub non l'ha già fatto. Se PR chiusa senza merge, il task torna Ready/Blocked, non Done.

Per una issue che richiede più agenti, tutti contribuiscono alla stessa PR con file disgiunti. Per più issue, i worktree/branch/PR sono separati. Non accumulare implementazioni di issue dipendenti sulla PR di setup.
