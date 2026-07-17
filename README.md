# qrcode-web

A QR code generator with two parts:

1. **API service** (`app/`) — FastAPI service that returns QR codes as SVG or PNG. Deployed on Render.
2. **Static web app** (`web/`) — A single-page app that takes a URL/text input and renders the QR as inline SVG. Hosted on GitHub Pages.

## API

Base URL: `https://qrcode-web.onrender.com` (replace with your Render URL)

- `GET /` — service info
- `GET /health` — health check
- `GET /qr?data=<text>&format=svg|png&size=10&border=4` — generate QR

Example:

```bash
curl "https://qrcode-web.onrender.com/qr?data=https://example.com&format=svg" -o qr.svg
```

## Local development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://localhost:8000/docs
```

To run the web app locally, serve the `web/` folder:

```bash
python -m http.server 8080 --directory web
```

> The web app calls the Render API by default. For local testing, change `API` in `web/index.html` to `http://localhost:8000/qr`.

## Deploy API to Render

1. Push this repo to GitHub.
2. In Render, create a new **Web Service** from the repo.
3. Render auto-detects `render.yaml`. Free plan is fine.
4. Note your service URL and update `API` in `web/index.html`.

## Deploy web app to GitHub Pages

1. In repo **Settings → Pages**, set source to `main` branch, folder `/web`.
2. Push. The site will be at `https://<user>.github.io/qrcode-web/`.
3. Make sure `API` in `web/index.html` points to your Render URL.
