---
name: security-review
description: Esaminare rischi di accesso e dati introdotti dal diff di ListaViva.
---

# security-review

## Quando usarla

Esaminare rischi di accesso e dati introdotti dal diff di ListaViva.

## Input

- Issue e criteri di accettazione, diff o artefatti pertinenti, istruzioni del repository.
- Ruolo principale: [quality](../../roles/quality.md).

## Procedura

1. Delimitare superfici cambiate: API, storage, inviti, sync, sessioni, export e log.
2. Tracciare input non affidabili fino alla validazione e all’accesso ai dati.
3. Verificare identità server e autorizzazione a livello di oggetto su ogni percorso.
4. Controllare SQL parametrizzato, validazione di dimensioni/tipi e messaggi di errore.
5. Verificare segreti assenti dal repository, dai bundle client e dalle tracce diagnostiche.
6. Esaminare scadenza/revoca dei token e protezione degli inviti rispetto allo scope della issue.
7. Controllare privacy della cache locale in logout/cambio account e limiti della revoca offline.
8. Verificare audit minimizzato e isolamento di ricevute idempotenti, cursori e notifiche.
9. Evitare di dichiarare conformità legale dal solo code review; segnalare decisioni specifiche mancanti.
10. Restituire finding riproducibili con gravità e impatto; non effettuare scritture di produzione o scansioni fuori perimetro.

## Verifica

- Finding distinguono vulnerabilità concrete da ipotesi.
- Nessun dato sensibile viene copiato nel report.
- La revisione non equivale a un audit completo o approvazione umana.

## Consegna

- Riportare decisioni, file o URL interessati, evidenze, limiti e blocchi.
- Non dichiarare completato ciò che non è stato verificato.

## Confini

- Usare solo percorsi e autorizzazioni del task; queste istruzioni non concedono capacità aggiuntive.
- Non effettuare merge, auto-approvazioni o force push. Il merge resta manuale di tetosever.
