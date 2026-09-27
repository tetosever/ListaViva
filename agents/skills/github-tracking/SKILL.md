---
name: github-tracking
description: Collegare milestone, issue, branch e PR preservando la revisione di tetosever.
---

# github-tracking

## Quando usarla

Collegare milestone, issue, branch e PR preservando la revisione di tetosever.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [pm](../../roles/pm.md).

## Procedura

1. Leggere convenzioni del repository e issue/PR esistenti prima di creare risorse.
2. Per milestone e backlog usare `agents/scripts/pm_sync.py` dalla radice: dry run, revisione, poi `--apply`.
3. Mantenere gli ID stabili per consentire sincronizzazioni idempotenti; in caso di match ambiguo fermare la voce.
4. Associare a ogni issue implementativa un branch `feat/<numero>-<slug>`, `fix/…` o `chore/…`.
5. Usare un worktree per issue parallela, senza checkout o reset in directory condivise.
6. Aprire una PR sulla base prevista con motivazione, scope, test effettivi e limiti; aggiungere `Closes #N` solo per completamenti reali.
7. Passare da Draft a pronta alla revisione dopo i controlli richiesti, indicando il commit verificato.
8. Ricevere i commenti dalla PR e correggere lo stesso branch; verificare nuovamente quanto interessato.
9. Lasciare approvazione finale e merge manuale a tetosever; mai auto-approvare, fare merge o force push.
10. Aggiornare lo stato sulla base di fatti; una issue di codice è Done solo con PR merged e criteri soddisfatti.

## Verifica

- Branch e PR puntano alla issue corretta e alla base prevista.
- Nessuna credenziale o dato privato nel corpo o nei log.
- Chiusure automatiche non sostituiscono la verifica del completamento.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
