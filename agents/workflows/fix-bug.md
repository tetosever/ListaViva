# Correggere un bug

Il PM crea o riusa una issue con riproduzione minima, atteso/osservato, ambiente e impatto. L'orchestratore assegna un branch `fix/<numero>-<slug>` e individua il proprietario del percorso coinvolto. Prima di modificare la logica, riprodurre il difetto o dichiarare perché non è riproducibile.

Correggere la causa nello scope della issue, aggiungere una verifica di regressione quando il difetto è significativo e verificare i casi vicini che possono essere compromessi. Non mescolare refactoring estesi. Applicare poi Quality e revisione umana del workflow `issue-to-pr.md`.
