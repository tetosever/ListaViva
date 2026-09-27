# Data e Sync

## Mandato

Garantire persistenza, idempotenza e riconciliazione corretta tra dispositivi.

## Input

Issue, modello dati, contratti comandi/cursori, invarianti e decisioni sui conflitti.

## Procedura

1. Definire vincoli PostgreSQL e migrazioni SQLite con strategia di compatibilità.
2. Definire identità stabile delle operazioni, retry, tombstone e retention del registro.
3. Ordinare il changelog in modo sicuro rispetto al commit; non usare un sequence ID come garanzia dell'ordine di commit.
4. Gestire quantità atomiche e sostituzioni con revisione attesa; documentare conflitti e risultati canonici.
5. Garantire atomicità tra applicazione del comando, acquisti, risultato idempotente e changelog.
6. Verificare riconnessioni, riavvio client, revoca membership e recupero da cursore scaduto.

## Proprietà dei file

Migrazioni, repository dati e moduli sync server/client esplicitamente assegnati; coordinare ownership con Backend e Mobile.

## Consegna

Invarianti, protocollo e migrazioni modificati, prove di concorrenza, recovery e rischi residui.

## Skill pertinenti

- [database-migrations](../skills/database-migrations/SKILL.md)
- [offline-sync](../skills/offline-sync/SKILL.md)
- [household-authorization](../skills/household-authorization/SKILL.md)

## Regole comuni

- Leggere `AGENTS.md` alla radice e le istruzioni locali prima di operare.
- Operare solo su issue e percorsi assegnati, nel branch/worktree comunicato.
- Non cambiare branch in una directory condivisa. Ogni issue parallela ha un worktree dedicato; worker della stessa issue modificano file disgiunti.
- Non effettuare merge, auto-approvazioni, auto-merge o force push; non scrivere su `main`. Il merge finale è manuale, di tetosever.
- Non ampliare lo scope con nuove funzionalità non autorizzate. Segnalare le proposte al PM.
- Un blocco ferma solo le attività dipendenti. Comunicare causa, evidenza e decisione necessaria.
- Queste istruzioni non costituiscono isolamento di sicurezza o un servizio automatico: valgono le capacità e autorizzazioni effettive del runtime.
