# AssistenzaGelormini

Client di assistenza remota di **Informatica Gelormini**, ricavato da [RustDesk](https://github.com/rustdesk/rustdesk)
(versione indicata in `.github/workflows/build-windows.yml`, variabile `VERSION`) con:

- nome del programma *AssistenzaGelormini*, icona e logo di Informatica Gelormini (`risorse/`);
- colori del sito (blu #3C6DF0, blu notte #181B31), logo chiaro e scuro, riquadro con slogan, telefono/WhatsApp e sito;
- indirizzo e chiave **pubblica** del server di Informatica Gelormini scritti nel programma;
- controllo degli aggiornamenti verso rustdesk.com tolto e VERIFICATO in compilazione (il programma non viene sostituito dal RustDesk normale);
- rubrica condivisa sul server di Informatica Gelormini, raggiungibile solo dalla sua rete privata (Tailscale);
- collegamenti verso www.informaticagelormini.com.

Nessuna password o segreto e' contenuto in questo repository: la chiave del server qui presente e' quella pubblica,
che ogni client riceve comunque dal server.

## Come si compila

Ogni modifica sul ramo `main` avvia GitHub Actions (`build-windows.yml`, Windows x64, circa 45 minuti). Il workflow
controlla che nel programma ci siano il server e la chiave giusti e che NON ci siano quelli di rustdesk.com, poi
pubblica eseguibile, MSI e `SHA256SUMS.txt` come Release del repository.

## Provenienza e licenze

- RustDesk: Purslane Ltd e collaboratori, licenza **AGPL-3.0** (`LICENSE-RustDesk-AGPL-3.0.txt`). Il sorgente usato
  e' il tag ufficiale di `rustdesk/rustdesk` indicato nel workflow; le modifiche sono quelle applicate dal workflow stesso.
- I workflow in `.github/workflows` e la patch in `.github/patches` derivano da
  [rdgen](https://github.com/bryangerlach/rdgen) (Bryan Gerlach, licenza **GPL-3.0**, `LICENSE-rdgen-GPL-3.0.txt`),
  commit `0e83379858ec4a2ecb8a4f832b0db5de8ab605aa`, adattati per non dipendere da un server rdgen.
- Logo e marchio AG: Antonio Gelormini, non coperti dalle licenze sopra.
