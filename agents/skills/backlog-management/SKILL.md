---
name: backlog-management
description: Scomporre le milestone di ListaViva in backlog verificabile e dipendenze eseguibili.
---

# backlog-management

## Quando usarla

Scomporre le milestone di ListaViva in backlog verificabile e dipendenze eseguibili.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [pm](../../roles/pm.md).

## Procedura

1. Leggere PRD, roadmap e decisioni successive prima di proporre lo scope.
2. Associare ogni issue a una milestone nativa e a un ID stabile del catalogo.
3. Coprire flussi utente, prerequisiti tecnici, casi di errore e validazioni della milestone.
4. Suddividere task troppo grandi quando la PR perderebbe uno scope revisionabile; usare 1–3 giorni come riferimento, non promessa.
5. Esplicitare dipendenze con ID risolvibili; verificare riferimenti mancanti e cicli.
6. Marcare Ready solo quando scope, criteri, dipendenze e decisioni necessarie sono definiti.
7. Annotare separatamente scope aggiunto/rimosso: non alterare silenziosamente il denominatore del progresso.
8. Usare evidenze di branch, PR e merge per lo stato tecnico; per OKR usare campione e periodo osservati.
9. Non trasformare metriche di retention o feedback in successi dedotti dai test.
10. Raffinare le milestone future prima della loro esecuzione e mantenere visibili i gate di prodotto.

## Verifica

- Nessuna issue orfana, duplicata o dipendenza ciclica.
- Ogni gate di prodotto ha un task di raccolta/verifica dati esplicito.
- Report separa codice integrato, revisione pendente e validazione utenti.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
