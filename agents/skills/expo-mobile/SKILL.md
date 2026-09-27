---
name: expo-mobile
description: Implementare interfaccia Expo accessibile con persistenza e stato offline esplicito.
---

# expo-mobile

## Quando usarla

Implementare interfaccia Expo accessibile con persistenza e stato offline esplicito.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [mobile](../../roles/mobile.md).

## Procedura

1. Leggere contratti e protocolli locali prima di creare schermate.
2. Progettare stati vuoti, caricamento, errore, assenza rete e riconciliazione.
3. Usare SecureStore per i token previsti e SQLite per dati/coda; evitare segreti in storage o log generici.
4. Aggiornare vista locale e accodare comando nella stessa transazione ove previsto.
5. Mostrare feedback ottimistico distinguendo conferma locale e sync pendente.
6. Mantenere operation ID stabile attraverso timeout, retry e riavvio.
7. Usare etichette accessibili, target di tocco adeguati, contrasto e supporto al testo ingrandito.
8. Gestire quantità e conflitti con azioni comprensibili senza perdere silenziosamente l’intento.
9. Verificare logout, cambio account e revoca per evitare esposizione della cache precedente.
10. Provare i flussi pertinenti su iOS/Android disponibili e dichiarare esplicitamente quanto non verificato.

## Verifica

- La rete lenta non blocca inutilmente il flusso di spesa.
- Un riavvio non perde comandi salvati e non duplica quelli confermati.
- Il report identifica dispositivi o simulatori realmente usati.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
