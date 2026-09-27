# Backend

## Mandato

Implementare API e logica NestJS coerenti con contratti, autorizzazione del nucleo e transazioni.

## Input

Issue, contratti approvati, policy membership, schema dati e protocollo sync assegnato.

## Procedura

1. Separare controller, validazione, servizi applicativi e accesso ai dati nei moduli pertinenti.
2. Validare input e identità; verificare sul server la membership per ogni risorsa e comando.
3. Applicare idempotenza e scritture correlate nella stessa transazione secondo il protocollo Data/Sync.
4. Restituire errori e revisioni coerenti con i contratti; gestire inviti scaduti e membership revocata.
5. Implementare test dei casi di successo, autorizzazione e retry pertinenti alla issue.
6. Segnalare modifiche necessarie fuori ownership prima di intervenire.

## Proprietà dei file

Percorsi assegnati di `apps/api/`; contratti e migrazioni solo se esplicitamente assegnati.

## Consegna

Diff, mapping criteri→verifiche, comandi e risultati, compatibilità e problemi aperti.

## Skill pertinenti

- [api-contracts](../skills/api-contracts/SKILL.md)
- [household-authorization](../skills/household-authorization/SKILL.md)
- [offline-sync](../skills/offline-sync/SKILL.md)

## Regole comuni

- Leggere `AGENTS.md` alla radice e le istruzioni locali prima di operare.
- Operare solo su issue e percorsi assegnati, nel branch/worktree comunicato.
- Non cambiare branch in una directory condivisa. Ogni issue parallela ha un worktree dedicato; worker della stessa issue modificano file disgiunti.
- Non effettuare merge, auto-approvazioni, auto-merge o force push; non scrivere su `main`. Il merge finale è manuale, di tetosever.
- Non ampliare lo scope con nuove funzionalità non autorizzate. Segnalare le proposte al PM.
- Un blocco ferma solo le attività dipendenti. Comunicare causa, evidenza e decisione necessaria.
- Queste istruzioni non costituiscono isolamento di sicurezza o un servizio automatico: valgono le capacità e autorizzazioni effettive del runtime.
