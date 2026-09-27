---
name: database-migrations
description: Progettare schema PostgreSQL e SQLite con vincoli e migrazioni recuperabili.
---

# database-migrations

## Quando usarla

Progettare schema PostgreSQL e SQLite con vincoli e migrazioni recuperabili.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [data-sync](../../roles/data-sync.md).

## Procedura

1. Leggere invarianti e schema corrente prima di modificare tabelle.
2. Assegnare un solo proprietario alla sequenza delle migrazioni.
3. Esprimere unicità e relazioni con vincoli, includendo lo scope household.
4. Definire indici dai pattern di accesso reali, evitando ottimizzazioni speculative.
5. Usare operazioni additive e fasi di backfill quando servono client/versioni compatibili.
6. Valutare lock e durata delle migrazioni server; documentare recovery/roll-forward per passaggi irreversibili.
7. Verificare migrazione sia da database vuoto sia dalla versione precedente con dati rappresentativi.
8. Mantenere versione schema locale e transazioni di migrazione SQLite senza distruggere la coda offline.
9. Non usare sequenze PostgreSQL per dedurre ordine di commit del changelog.
10. Verificare atomicità tra mutazione, registro idempotente e cambiamenti esportati dalla sync.

## Verifica

- Vincoli impediscono duplicati anche con richieste concorrenti.
- La migrazione non elimina dati o comandi pendenti senza una decisione autorizzata.
- Piano di recupero descrive ciò che è realmente possibile.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
