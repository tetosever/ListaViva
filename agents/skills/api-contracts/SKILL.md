---
name: api-contracts
description: Definire contratti API e confini NestJS condivisi tra mobile e backend.
---

# api-contracts

## Quando usarla

Definire contratti API e confini NestJS condivisi tra mobile e backend.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [backend](../../roles/backend.md).

## Procedura

1. Leggere i contratti esistenti prima di creare tipi o endpoint.
2. Assegnare un unico proprietario alle modifiche di `packages/contracts/`.
3. Definire input, output, validazione, errori, identità delle risorse e revisioni.
4. Usare DTO pubblici: non esporre direttamente modelli del database al mobile.
5. Documentare comandi idempotenti, operation ID e comportamento dei retry.
6. Concordare paginazione e cursori con Data/Sync prima di implementare letture incrementali.
7. Organizzare NestJS in controller sottili, servizi applicativi e accesso ai dati; mantenere i controlli di membership lato server.
8. Gestire errori previsti con codici stabili senza stack o dettagli di altri nuclei.
9. Valutare compatibilità con client già distribuiti prima di cambiare un campo.
10. Confermare tramite test del contratto che client e server concordino su successo, errore e conflitto.

## Verifica

- Mobile non importa entità interne del database.
- I contratti non accettano household ID come prova di autorizzazione.
- Ogni cambiamento incompatibile ha una strategia esplicita.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
