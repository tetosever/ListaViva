---
name: offline-sync
description: Implementare retry idempotenti, conflitti e cursori senza perdere modifiche concorrenti.
---

# offline-sync

## Quando usarla

Implementare retry idempotenti, conflitti e cursori senza perdere modifiche concorrenti.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [data-sync](../../roles/data-sync.md).

## Procedura

1. Salvare comando e modifica ottimistica in una transazione SQLite, con operation ID unico e persistente.
2. Associare l’identità idempotente a household e attore autenticato; un retry deve preservare lo stesso ID e payload.
3. Sul server imporre unicità della chiave e memorizzare hash del payload/risultato: stesso ID con payload diverso è un errore.
4. Verificare membership corrente anche per risultati già registrati; non restituire dati a membri revocati.
5. Applicare mutazione, eventuale acquisto, ricevuta idempotente e changelog nella stessa transazione.
6. Per cursori per nucleo, bloccare la riga contatore del nucleo prima delle mutazioni; incrementare il contatore e scrivere eventi nella stessa transazione mantenendo il lock fino al commit.
7. Non usare timestamp client o sequence auto-incrementale come ordine di commit: una transazione lenta potrebbe comparire dietro un cursore già avanzato.
8. Applicare delta di quantità atomicamente; per valori assoluti richiedere revisione attesa e restituire conflitto con stato canonico autorizzato.
9. Usare pull dal cursore come recupero autorevole; WebSocket è solo un segnale. Gestire pagine, tombstone e cursore scaduto con snapshot coerente e replay dei comandi pendenti.
10. Definire retention e retry massimo del registro: comandi più vecchi della finestra non devono essere riapplicati silenziosamente.
11. Provare due dispositivi, risposta persa dopo commit, crash client, commit concorrenti, revoca, completamento ripetuto e conflitti.
12. Registrare per diagnosi solo metadati necessari e autorizzati; audit e risposte non devono esporre dati di altri nuclei.

## Verifica

- Nessun acquisto duplicato dopo un retry.
- Il cursore non salta eventi committati più tardi.
- Una riconciliazione non scarta silenziosamente un comando pendente.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
