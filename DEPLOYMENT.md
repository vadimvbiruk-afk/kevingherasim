# Deploying kevin gerasim to a custom domain

## Production environment variables

On your host (Render, Heroku, PythonAnywhere, etc.), set:

- `FLASK_ENV=production` or `PRODUCTION=1` — turns off debug and enables Flask-Talisman (HTTPS + secure headers).
- `SECRET_KEY` — a long random string (never use the default).
- `DATABASE_URL` — your production database URL (e.g. PostgreSQL on Render/Heroku).

---

## Domain registrar checklist (Namecheap, GoDaddy, etc.)

Use this at your **domain registrar** (where you bought the domain) to point the domain to a host like **Render** or **PythonAnywhere**.

### 1. Get your host’s DNS details

- **Render:** In the dashboard, open your web service → **Settings** → **Custom Domain**. Add your domain (e.g. `kevingerasim.com`) and note the **CNAME target** (e.g. `your-app.onrender.com`) or **A record** instructions.
- **Heroku:** In the app → **Settings** → **Domains** → add domain; Heroku gives you a DNS target (e.g. `your-app.herokuapp.com` for CNAME).
- **PythonAnywhere:** **Web** tab → **Static files / URL configuration**; add your domain and follow their “Custom domain” instructions (CNAME to `username.pythonanywhere.com` or their stated target).

Write down:

- **CNAME target** (e.g. `yourapp.onrender.com`) **or**
- **A record IP** (if the host gives an IP instead of a hostname).

### 2. Log in to your domain registrar

- Namecheap: [namecheap.com](https://www.namecheap.com) → **Domain List** → **Manage** for your domain.
- GoDaddy: [godaddy.com](https://www.godaddy.com) → **My Products** → **DNS** for your domain.
- (Other registrars: find “DNS”, “Nameservers”, or “Advanced DNS”.)

### 3. Open DNS / Advanced DNS

- Find the section named **DNS Records**, **Advanced DNS**, **Manage DNS**, or similar.
- You will add or edit records below.

### 4. Point the root domain (e.g. `kevingerasim.com`)

**If your host gives a CNAME target (e.g. Render, Heroku):**

- **Option A — Root domain (apex):**  
  Many hosts (e.g. Render) support **ALIAS** or **ANAME** for the root. If your registrar has **ALIAS** or **ANAME**:
  - Type: **ALIAS** (or ANAME)
  - Host: `@` (or leave blank for “root”)
  - Value/Target: the host’s CNAME target (e.g. `yourapp.onrender.com`)
- **Option B — Root not supported:**  
  If the host only gives a CNAME and your registrar doesn’t support ALIAS/ANAME for root, use their “redirect” or “forwarding” to send `example.com` → `www.example.com`, then point `www` with CNAME (see step 5).

**If your host gives an A record IP:**

- Type: **A**
- Host: `@` (root)
- Value: the IP they provided
- TTL: 300–3600 (or default).

### 5. Point the www subdomain (e.g. `www.kevingerasim.com`)

- Type: **CNAME**
- Host: `www`
- Value/Target: the host’s CNAME target (e.g. `yourapp.onrender.com` or `yourapp.herokuapp.com`)
- TTL: 300–3600 (or default).

(If you only use `www`, you can skip root and only add this CNAME.)

### 6. Remove conflicting records

- If you have an old **A** or **CNAME** for `@` or `www` pointing somewhere else, delete or update it so it points to your new host.

### 7. Save and wait for DNS

- Save all DNS changes at the registrar.
- Propagation can take from a few minutes up to 24–48 hours.
- You can check with [whatsmydns.net](https://www.whatsmydns.net) or `dig www.yourdomain.com`.

### 8. Add the domain on the host

- In **Render** / **Heroku** / **PythonAnywhere**, add your custom domain (e.g. `www.kevingerasim.com` and optionally `kevingerasim.com`).
- If the host offers **SSL/TLS**, enable it (Let’s Encrypt) so the site is served over HTTPS.

### 9. Test

- Visit `https://www.yourdomain.com` (and `https://yourdomain.com` if configured).
- Confirm the site loads and that Flask-Talisman doesn’t report mixed-content or HTTPS issues.

---

## Quick checklist

- [ ] Get CNAME target or A record IP from your host (Render / Heroku / PythonAnywhere).
- [ ] At registrar: open DNS / Advanced DNS for your domain.
- [ ] Add **CNAME** for `www` → host’s target (and **ALIAS/ANAME** or **A** for root if needed).
- [ ] Remove or update any old A/CNAME for `@` and `www`.
- [ ] Save DNS; wait for propagation (up to 24–48 hours).
- [ ] Add the custom domain in the host’s dashboard and enable HTTPS.
- [ ] Set production env vars: `FLASK_ENV=production` (or `PRODUCTION=1`), `SECRET_KEY`, `DATABASE_URL`.
- [ ] Test in the browser over HTTPS.
