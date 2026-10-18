# Nino09 Stats: istruzioni

## 1. Chiavi per le notifiche (sul PC, una volta sola)
    pip install pywebpush
    python gen_keys.py
- Chiave PUBBLICA: incollala in `index.html` al posto di INCOLLA_QUI_LA_CHIAVE_PUBBLICA.
- Chiave PRIVATA: tienila per il punto 3.

## 2. Pubblica il sito
1. Crea un repository pubblico su GitHub e carica tutti i file (compresa la cartella `.github`).
2. Settings → Pages → Branch: main, cartella /root. Ti darà un indirizzo https://tuonome.github.io/nome-repo/

## 3. Secrets (Settings → Secrets and variables → Actions)
- `YOUTUBE_API_KEY`: chiave dalla Google Cloud Console (abilita "YouTube Data API v3")
- `VAPID_PRIVATE_KEY`: la chiave privata del punto 1
- `VAPID_EMAIL`: la tua email
- `PUSH_SUBSCRIPTION`: il codice che ti mostra l'app (punto 4)

## 4. Sull'iPhone
1. Apri l'indirizzo in Safari → Condividi → Aggiungi a Home.
2. Apri l'app dalla Home → "Attiva notifiche" → Consenti.
3. Copia il codice, salvalo nel Secret PUSH_SUBSCRIPTION.

## 5. Prova
GitHub → Actions → "Notifica settimanale" → Run workflow. Dopo pochi secondi arriva la notifica.
Poi parte da sola ogni lunedì alle 21:00 (ora italiana, anche con il cambio ora).

Se il tuo handle YouTube non è @Nino09, cambia `YT_HANDLE` in `.github/workflows/weekly.yml`.
