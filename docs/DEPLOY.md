# Deployment Guide — GitHub + Render

## Step 1: Push to GitHub

```bash
cd /Users/shrutisrivastava/Projects/india-payment-fraud-detection

# One-time: log in to GitHub
gh auth login

# Create repo and push
chmod +x scripts/push_github.sh
./scripts/push_github.sh
```

Your repo will be at: `https://github.com/<your-username>/india-payment-fraud-detection`

---

## Step 2: Deploy on Render (free tier)

1. Go to [render.com](https://render.com) and sign up / log in with GitHub
2. Click **New +** → **Blueprint**
3. Connect the `india-payment-fraud-detection` repository
4. Render reads `render.yaml` automatically
5. Click **Apply** — first deploy takes ~5–8 minutes (model training runs in build)

### After deploy

- Live URL: `https://payguard-ai.onrender.com` (or the name Render assigns)
- Update `ALLOWED_HOSTS` in Render dashboard if the URL differs:
  - Environment → `ALLOWED_HOSTS` → `your-app-name.onrender.com`

### Free tier note

Render free services spin down after 15 min idle. First page load may take ~30 seconds.

---

## Step 3: Update paper & README with live URL

After deploy, replace placeholder URLs in:
- `docs/SSRN_PAPER.md` (Abstract + Appendix)
- `README.md`

---

## Step 4: Upload paper to SSRN

1. Open `docs/SSRN_PAPER.md`
2. Fill in: **Affiliation**, **email** at the bottom
3. Convert to PDF:
   - **Option A:** Paste into Google Docs → File → Download → PDF
   - **Option B:** `brew install pandoc && pandoc docs/SSRN_PAPER.md -o docs/SSRN_PAPER.pdf`
4. Go to [ssrn.com](https://www.ssrn.com) → **Submit a Paper**
5. Choose **eLibrary** → **Computer Science eJournal** or **Economics eJournal**
6. Upload PDF, add abstract, keywords, JEL codes from the paper header

### SSRN metadata (copy from paper)

| Field | Value |
|-------|-------|
| Title | Artificial Intelligence for Fraud Detection in Digital Payments: Opportunities, Challenges and Policy Implications for India |
| Keywords | Artificial Intelligence, Fraud Detection, UPI, Digital Payments, India, Machine Learning, RBI, NPCI |
| JEL | G23, G28, O33, K24 |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build timeout on Render | Upgrade build timeout in dashboard or pre-commit trained model |
| 400 Bad Request | Add your Render URL to `ALLOWED_HOSTS` |
| Static files missing | `collectstatic` runs in `build.sh` |
| Model not found | `build.sh` runs `train_model` automatically |
