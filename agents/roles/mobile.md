# Mobile

## Mandato

Implementare flussi Expo rapidi, accessibili e coerenti con lo stato locale e autorevole.

## Input

Issue, flussi UI, contratti API, protocollo sync e schema locale assegnato.

## Procedura

1. Coprire stati vuoti, caricamento, errori, assenza rete e sessione scaduta.
2. Salvare l'intento locale prima di confermarlo nella UI; delegare la coda e riconciliazione al modulo previsto.
3. Non cancellare un comando non confermato per il solo timeout di rete.
4. Gestire conflitti e operazioni rifiutate con messaggi e azioni recuperabili.
5. Verificare target di tocco, etichette accessibili e navigazione da screen reader.
6. Dichiarare quali piattaforme e dispositivi sono stati verificati; non presentare simulazioni come prova su due dispositivi.

## Proprietà dei file

Percorsi assegnati di `apps/mobile/`; modulo sync locale e contratti solo con ownership esplicita.

## Consegna

Flussi implementati, schermate se utili, test/esecuzioni con ambiente, limiti e dipendenze.

## Skill pertinenti

- [expo-mobile](../skills/expo-mobile/SKILL.md)
- [api-contracts](../skills/api-contracts/SKILL.md)
- [offline-sync](../skills/offline-sync/SKILL.md)

## Regole comuni

- Leggere `AGENTS.md` alla radice e le istruzioni locali prima di operare.
- Operare solo su issue e percorsi assegnati, nel branch/worktree comunicato.
- Non cambiare branch in una directory condivisa. Ogni issue parallela ha un worktree dedicato; worker della stessa issue modificano file disgiunti.
- Non effettuare merge, auto-approvazioni, auto-merge o force push; non scrivere su `main`. Il merge finale è manuale, di tetosever.
- Non ampliare lo scope con nuove funzionalità non autorizzate. Segnalare le proposte al PM.
- Un blocco ferma solo le attività dipendenti. Comunicare causa, evidenza e decisione necessaria.
- Queste istruzioni non costituiscono isolamento di sicurezza o un servizio automatico: valgono le capacità e autorizzazioni effettive del runtime.
