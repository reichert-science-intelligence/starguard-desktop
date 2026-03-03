# ngrok Setup for StarGuard AI

Expose your StarGuard Shiny app to the internet for demos, mobile testing, and sharing.

---

## STEP 1: Add Your Authtoken (one-time)

```powershell
ngrok config add-authtoken YOUR_AUTHTOKEN
```

Replace `YOUR_AUTHTOKEN` with your token from [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken).

**Expected output:**
```
Authtoken saved to configuration file: C:\Users\YourName\.ngrok2\ngrok.yml
```

---

## STEP 2: Start StarGuard Shiny App

Open a terminal and run:

```powershell
# Navigate to project
cd "c:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\starguard-shiny"

# Activate venv (if you have one)
# venv\Scripts\activate

# Start Shiny on port 8000
shiny run app.py --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Leave this running in its own window.

---

## STEP 3: Start ngrok in a Second Terminal

Open a **new** terminal (keep Shiny running):

```powershell
ngrok http 8000
```

**Expected output:**
```
Forwarding    https://xxxx-xxx-xxxx.ngrok-free.app -> http://localhost:8000
```

---

## STEP 4: Use Your Public URL

1. Copy the **Forwarding** HTTPS URL (e.g. `https://abcd-1234-5678.ngrok-free.app`)
2. Share it or open it on any device (phone, tablet, etc.)
3. ngrok web interface: [http://127.0.0.1:4040](http://127.0.0.1:4040) — inspect requests in real time

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `shiny run app.py --port 8000` | Run StarGuard locally on port 8000 |
| `ngrok http 8000` | Expose port 8000 to the internet |
| `ngrok config add-authtoken <token>` | One-time auth setup |

---

## Troubleshooting

- **Port in use:** Use `--port 8502` (or another free port) and point ngrok to that port.
- **ngrok not found:** Install from [ngrok.com/download](https://ngrok.com/download) or `winget install ngrok.ngrok`.
- **Connection refused:** Ensure the Shiny app is running and listening on the port before starting ngrok.
