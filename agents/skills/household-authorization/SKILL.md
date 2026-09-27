---
name: household-authorization
description: Verificare isolamento dei nuclei, inviti e revoca degli accessi.
---

# household-authorization

## Quando usarla

Verificare isolamento dei nuclei, inviti e revoca degli accessi.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [backend](../../roles/backend.md).

## Procedura

1. Ricavare l’identità da una sessione verificata sul server.
2. Caricare membership e ruolo per ogni risorsa richiesta; non fidarsi del nucleo dichiarato dal client.
3. Applicare lo scope household anche a sync, changelog, WebSocket, export e operazioni in coda.
4. Controllare la membership corrente anche nei retry prima di restituire un risultato idempotente.
5. Coordinare autorizzazione delle scritture e revoca nella transazione per evitare controlli obsoleti.
6. Usare token di invito non prevedibili, con scadenza e stato; non registrarli nei log.
7. Garantire unicità della membership e comportamento idempotente di accettazione invito.
8. Definire la pulizia dei dati locali alla revoca rilevata e al logout; un dispositivo offline non riceve una cancellazione istantanea.
9. Limitare audit e diagnostica a identificativi e informazioni necessarie; non esporre contenuti di spesa o token.
10. Verificare con due nuclei accessi diretti a ID altrui, cursori altrui, inviti invalidi e sessioni revocate.

## Verifica

- Ogni via di accesso ha test negativi tra nuclei.
- I risultati memorizzati non eludono la revoca.
- Nessun messaggio di errore rivela dettagli non autorizzati.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
