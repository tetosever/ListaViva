---
name: user-story-writing
description: Scrivere user story, task tecnici e criteri di accettazione revisionabili.
---

# user-story-writing

## Quando usarla

Scrivere user story, task tecnici e criteri di accettazione revisionabili.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [pm](../../roles/pm.md).

## Procedura

1. Specificare attore, bisogno e risultato della user story.
2. Per attività tecniche descrivere il risultato operativo senza inventare un utente fittizio.
3. Indicare contesto e requisito sorgente, con riferimenti al PRD o decisione.
4. Elencare scope incluso e fuori scope con esempi concreti.
5. Scrivere criteri osservabili di successo, errore e autorizzazione quando pertinenti.
6. Specificare effetti della ripetizione, offline e concorrenza se il task modifica dati.
7. Collegare prerequisiti e contratti prima di stimare eseguibilità.
8. Indicare proprietario operativo, priorità, milestone e modalità di verifica.
9. Evitare criteri vaghi come “funziona correttamente” o copertura arbitraria al 100%.
10. Se la storia supera un cambiamento revisionabile, dividerla in risultati coerenti mantenendo la tracciabilità.

## Verifica

- Un revisore può decidere se ogni criterio è soddisfatto.
- Ogni esclusione impedisce ambiguità, senza cancellare un requisito necessario.
- Le verifiche richieste sono realizzabili nell’ambiente previsto.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
