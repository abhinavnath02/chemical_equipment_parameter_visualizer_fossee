# Quick Deployment Summary

This guide provides the fastest path to deploy your application.

## 🚀 Recommended: Railway + Vercel (Free Tier)

### 1️⃣ Deploy Backend (Railway) - 5 minutes

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select this repository
4. Click **"Add variables"** and set:
   ```
   DJANGO_SETTINGS_MODULE=backend.production_settings
   SECRET_KEY=<generate-new-secret-key>
   ALLOWED_HOSTS=*.railway.app
   CORS_ORIGINS=https://your-app.vercel.app
   CSRF_ORIGINS=https://your-app.vercel.app
   ```
5. Click **"New"** → **"Database"** → **"PostgreSQL"** (Railway auto-connects it)
6. Wait for deployment to complete
7. Copy your Railway URL: `https://your-app.railway.app`

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2️⃣ Deploy Frontend (Vercel) - 3 minutes

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"Add New"** → **"Project"**
3. Import this repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `web-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add environment variable:
   ```
   VITE_API_BASE_URL=https://your-app.railway.app/api
   ```
6. Click **"Deploy"**
7. Copy your Vercel URL: `https://your-app.vercel.app`

### 3️⃣ Update CORS Settings

Go back to Railway and update these variables with your actual Vercel URL:
```
CORS_ORIGINS=https://your-app.vercel.app
CSRF_ORIGINS=https://your-app.vercel.app
```

### 4️⃣ Deploy Desktop App (GitHub Releases)

1. Create a new release:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. Go to GitHub → Your Repository → **Releases** → **"Create a new release"**

3. Upload `desktop-app/dist/main.exe` and rename to `ChemicalEquipmentVisualizer-v1.0.0.exe`

4. Update download link in [web-frontend/src/components/LandingPage.tsx](web-frontend/src/components/LandingPage.tsx):
   ```tsx
   href="https://github.com/YOUR_USERNAME/YOUR_REPO/releases/download/v1.0.0/ChemicalEquipmentVisualizer-v1.0.0.exe"
   ```

---

## ✅ Verify Deployment

Visit your Vercel URL and test:
- [ ] Landing page loads
- [ ] Sign up works
- [ ] Login works
- [ ] CSV upload works
- [ ] Charts display correctly
- [ ] PDF generation works
- [ ] Desktop app download works

---

## 🔧 Troubleshooting

**CORS Error?**
- Make sure CORS_ORIGINS in Railway matches your Vercel URL exactly
- Include `https://` in the URL

**Database Error?**
- Railway automatically connects PostgreSQL - check if database is running
- View logs in Railway dashboard

**API Connection Failed?**
- Verify VITE_API_BASE_URL is correct in Vercel
- Check Railway deployment logs for errors

**Build Failed?**
- Check build logs in Railway/Vercel dashboard
- Ensure all dependencies are in requirements.txt / package.json

---

## 💰 Cost

- **Railway**: $5 credit/month (free tier)
- **Vercel**: Unlimited (free tier)
- **GitHub**: Unlimited (free)
- **Total: $0/month** (within free tiers)

---

## 📚 Full Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment options including:
- Alternative platforms (Render, Netlify, Heroku)
- Docker deployment
- VPS deployment
- Security best practices
- Monitoring and maintenance

---

## 🆘 Need Help?

Open an issue on GitHub with:
- Deployment platform (Railway/Vercel/etc.)
- Error messages from logs
- Steps you've already tried
