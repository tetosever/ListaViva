---
name: integration-testing
description: Verificare criteri di accettazione e rischi concreti su componenti integrati.
---

# integration-testing

## Quando usarla

Verificare criteri di accettazione e rischi concreti su componenti integrati.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [quality](../../roles/quality.md).

## Procedura

1. Associare ogni criterio della issue a un controllo osservabile.
2. Identificare percorsi e invarianti modificati dal diff prima di scegliere i test.
3. Preferire test che distinguano comportamento corretto da errore plausibile, non copie della implementazione.
4. Per flussi dati provare database reale compatibile e transazioni, dichiarando limiti degli eventuali mock.
5. Per sync provare retry, timeout dopo commit, concorrenza e ripresa da stato persistito.
6. Per autorizzazione usare almeno due identità e nuclei differenti.
7. Eseguire lint/typecheck/test previsti dal repository quando disponibili; non inventare comandi o esiti.
8. Registrare comando, commit, ambiente, esito e motivi delle verifiche non eseguite.
9. Riportare finding con severità, file/riga e scenario riproducibile; non cambiare test per nascondere un difetto.
10. Smettere di ampliare la suite quando il rischio concreto è coperto; demandare le correzioni al proprietario.

## Verifica

- Ogni successo dichiarato ha evidenza.
- Le limitazioni dei test sono visibili nella PR.
- Il codice esaminato coincide con il commit riportato.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
