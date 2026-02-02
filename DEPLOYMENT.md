# Deployment Guide

This guide covers deploying the Chemical Equipment Parameter Visualizer application with three components:
1. Django Backend (API)
2. React Frontend (Web App)
3. Desktop App (Executable Download)

## 🎯 Deployment Options

### Option 1: Full Deployment (Recommended)
- **Backend**: Railway/Render (Free tier available)
- **Frontend**: Vercel/Netlify (Free tier)
- **Desktop App**: GitHub Releases (Free)

### Option 2: Single Server Deployment
- Deploy everything on a single VPS (DigitalOcean, Linode, AWS)

---

## 📦 Backend Deployment (Railway)

Railway offers a generous free tier and easy Django deployment.

### Step 1: Prepare Backend for Production

Create `backend/backend/production_settings.py`:

```python
import os
from .settings import *

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE'),
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': os.environ.get('PGPORT', 5432),
    }
}

# CORS
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_ORIGINS', '').split(',')

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### Step 2: Add Production Dependencies

Update `backend/requirements.txt`:
```txt
Django==6.0.1
djangorestframework==3.15.2
djangorestframework-simplejwt==5.4.0
pandas==2.2.0
reportlab==4.0.9
matplotlib==3.8.0
numpy==1.26.3
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
django-cors-headers
```

### Step 3: Create Railway Configuration

Create `backend/Procfile`:
```
web: gunicorn backend.wsgi --bind 0.0.0.0:$PORT
release: python manage.py migrate
```

Create `backend/railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn backend.wsgi --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 4: Deploy to Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure environment variables:
   - `SECRET_KEY`: Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `ALLOWED_HOSTS`: Your Railway domain (e.g., `your-app.railway.app`)
   - `CORS_ORIGINS`: Your frontend URL (e.g., `https://your-app.vercel.app`)
   - `CSRF_ORIGINS`: Same as CORS_ORIGINS
   - `DJANGO_SETTINGS_MODULE`: `backend.production_settings`

5. Add PostgreSQL database:
   - In your Railway project, click "New" → "Database" → "PostgreSQL"
   - Railway automatically sets PGDATABASE, PGUSER, PGPASSWORD, PGHOST, PGPORT

6. Deploy! Railway will automatically build and deploy.

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Configure Environment Variables

Create `web-frontend/.env.production`:
```env
VITE_API_BASE_URL=https://your-backend.railway.app/api
```

### Step 2: Update API Base URL

Update `web-frontend/src/App.tsx`:
```typescript
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
```

### Step 3: Build Configuration

Update `web-frontend/vite.config.ts`:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
})
```

### Step 4: Deploy to Vercel

**Option A: Using Vercel CLI**
```bash
cd web-frontend
npm install -g vercel
vercel login
vercel
```

**Option B: Using Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Connect your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: web-frontend
   - **Build Command**: `npm run build`
   - **Output Directory**: dist
   - **Environment Variables**: Add `VITE_API_BASE_URL`

5. Click "Deploy"

---

## 💻 Desktop App Distribution

### Step 1: Build Windows Executable

```bash
cd desktop-app
pyinstaller --onefile --windowed --icon=fossee.ico main.py
```

Executable will be in `desktop-app/dist/main.exe`

### Step 2: Distribute via GitHub Releases

1. **Create Release on GitHub**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Go to GitHub** → Your Repository → Releases → "Create a new release"

3. **Upload the executable**:
   - Click "Choose files"
   - Upload `desktop-app/dist/main.exe`
   - Rename to `ChemicalEquipmentVisualizer-v1.0.0.exe`

4. **Update download link in web frontend**:
   
   In `web-frontend/src/components/LandingPage.tsx`:
   ```tsx
   <a
     href="https://github.com/YOUR_USERNAME/YOUR_REPO/releases/download/v1.0.0/ChemicalEquipmentVisualizer-v1.0.0.exe"
     className="..."
   >
     Download Desktop App
   </a>
   ```

### Alternative: Host on Frontend

Copy executable to `web-frontend/public/` before deployment:
```bash
Copy-Item desktop-app\dist\main.exe web-frontend\public\ChemicalEquipmentVisualizer.exe
```

Then use relative URL: `href="/ChemicalEquipmentVisualizer.exe"`

---

## 🔧 Alternative Deployment Options

### Render.com (Backend + Frontend)

**Backend:**
1. Create new Web Service on [render.com](https://render.com)
2. Connect GitHub repository
3. Configure:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn backend.wsgi:application`
   - Add PostgreSQL database
   - Set environment variables

**Frontend:**
1. Create new Static Site
2. Configure:
   - **Build Command**: `cd web-frontend && npm install && npm run build`
   - **Publish Directory**: `web-frontend/dist`

### Netlify (Frontend Alternative)

```bash
cd web-frontend
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

### Docker Deployment (All Components)

Create `docker-compose.yml` in root:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: equipmentdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    command: gunicorn backend.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/equipmentdb
    depends_on:
      - db

  frontend:
    build: ./web-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## ✅ Post-Deployment Checklist

- [ ] Update CORS settings in backend with frontend URL
- [ ] Update ALLOWED_HOSTS in backend
- [ ] Set DEBUG=False in production
- [ ] Configure proper SECRET_KEY
- [ ] Run database migrations on production
- [ ] Test user registration and login
- [ ] Test CSV upload functionality
- [ ] Test PDF generation
- [ ] Test desktop app download
- [ ] Set up SSL/HTTPS (automatic on Railway/Vercel)
- [ ] Configure custom domain (optional)
- [ ] Set up monitoring and logs
- [ ] Create backup strategy for database

---

## 🔐 Security Recommendations

1. **Environment Variables**: Never commit sensitive data to Git
2. **SECRET_KEY**: Generate a new one for production
3. **Database**: Use managed PostgreSQL with backups
4. **HTTPS**: Ensure all traffic is encrypted (free on most platforms)
5. **CORS**: Restrict to specific domains, not `*`
6. **Rate Limiting**: Add DRF throttling for API endpoints
7. **File Upload**: Add file size and type validation
8. **Dependencies**: Keep packages updated for security patches

---

## 📊 Monitoring & Maintenance

### Backend Logs
```bash
# Railway CLI
railway logs

# Check database
railway run python manage.py dbshell
```

### Frontend Logs
- Vercel: Dashboard → Your Project → Deployments → View Logs
- Netlify: Dashboard → Your Site → Deploys → View Logs

### Database Backups
- Railway: Automatic daily backups
- Render: Manual backups in dashboard
- Self-hosted: Use `pg_dump` with cron jobs

---

## 🚀 Quick Deploy Commands

```bash
# Backend to Railway
cd backend
railway login
railway init
railway up

# Frontend to Vercel
cd web-frontend
vercel --prod

# Desktop app to GitHub Releases
git tag v1.0.0
git push origin v1.0.0
# Upload exe file via GitHub web interface
```

---

## 🆘 Troubleshooting

### Backend Issues
- **500 Error**: Check logs for detailed error messages
- **CORS Error**: Verify CORS_ALLOWED_ORIGINS includes frontend URL
- **Static Files**: Run `python manage.py collectstatic`
- **Database**: Ensure migrations are run: `python manage.py migrate`

### Frontend Issues
- **API Connection Failed**: Check VITE_API_BASE_URL environment variable
- **404 on Refresh**: Add `_redirects` file in public/ with `/* /index.html 200`
- **Build Fails**: Clear node_modules and reinstall

### Desktop App Issues
- **Won't Download**: Check file size limits and MIME types
- **Antivirus Blocking**: Sign the executable or add README with instructions
- **API Connection**: Update API URL in compiled app before distribution

---

## 📝 Cost Estimates

### Free Tier Deployment
- **Railway**: $5 credit/month (sufficient for small apps)
- **Vercel**: Generous free tier (100GB bandwidth)
- **GitHub**: Unlimited releases and downloads
- **Total**: $0-5/month

### Paid Deployment
- **Railway Pro**: $20/month
- **Vercel Pro**: $20/month
- **Domain**: $10-15/year
- **Total**: ~$40-45/month

---

## 🎓 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)
- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [PyInstaller Documentation](https://pyinstaller.org/)

---

**Need Help?** Open an issue on GitHub or consult the documentation for your chosen platform.
