# Deployment Guide: Render + Netlify

Complete step-by-step guide to deploy your application using:
- **Backend**: Render.com (Free tier available)
- **Frontend**: Netlify (Free tier available)

**Total deployment time: ~15 minutes**

---

## 📋 Prerequisites

- GitHub account with this repository
- Email address for Render and Netlify signup
- Coffee ☕ (optional but recommended)

---

## 🔧 Part 1: Deploy Backend on Render (10 minutes)

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with GitHub (recommended) or email

### Step 2: Create PostgreSQL Database

1. From Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `equipment-db` (or any name you like)
   - **Database**: `equipmentdb`
   - **User**: `equipmentuser`
   - **Region**: Choose closest to you
   - **Plan**: **Free** (select this!)
3. Click **"Create Database"**
4. Wait ~2 minutes for database to provision
5. Once ready, click on the database name
6. **Copy** the **"Internal Database URL"** (starts with `postgresql://...`)
   - Keep this handy - you'll need it in Step 4!

### Step 3: Create Web Service for Backend

1. From Render dashboard, click **"New +"** → **"Web Service"**
2. Click **"Connect a repository"**
3. If first time: Authorize Render to access your GitHub
4. Find and select your repository: `chemical_equipment_parameter_visualizer_fossee`
5. Click **"Connect"**

### Step 4: Configure Web Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `equipment-backend` (or your preferred name)
- **Region**: Same as your database
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn backend.wsgi:application
  ```

**Plan:**
- Select **"Free"** (scroll down to find it)

### Step 5: Add Environment Variables

Click **"Advanced"** → Scroll to **"Environment Variables"**

Add these variables one by one (click **"Add Environment Variable"** for each):

1. **DJANGO_SETTINGS_MODULE**
   ```
   backend.production_settings
   ```

2. **SECRET_KEY** (Generate a new one!)
   - Open your terminal and run:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   - Copy the output and paste as the value

3. **DATABASE_URL**
   - Paste the **Internal Database URL** you copied in Step 2
   - Example: `postgresql://equipmentuser:password@dpg-xxxxx.oregon-postgres.render.com/equipmentdb`

4. **ALLOWED_HOSTS**
   ```
   equipment-backend.onrender.com,*.onrender.com
   ```
   ⚠️ Replace `equipment-backend` with your actual service name if different

5. **PYTHON_VERSION**
   ```
   3.11.0
   ```

6. **CORS_ORIGINS** (We'll update this later)
   ```
   http://localhost:5173
   ```

7. **CSRF_ORIGINS** (We'll update this later)
   ```
   http://localhost:5173
   ```

### Step 6: Deploy Backend

1. Click **"Create Web Service"** at the bottom
2. Render will start building and deploying (takes 5-10 minutes)
3. Watch the logs - you'll see:
   - Installing dependencies
   - Running migrations
   - Starting gunicorn server
4. Once you see **"Your service is live 🎉"**, copy your backend URL:
   - Example: `https://equipment-backend.onrender.com`
   - **Save this URL** - you'll need it for frontend!

### Step 7: Test Backend

1. Open your backend URL in browser: `https://equipment-backend.onrender.com/api/`
2. You should see the Django REST Framework browsable API
3. Test the endpoints:
   - `/api/register/` - Should show registration form
   - `/api/login/` - Should show login form

✅ **Backend deployment complete!**

---

## 🌐 Part 2: Deploy Frontend on Netlify (5 minutes)

### Step 1: Update Frontend Configuration

Before deploying, update the API URL:

1. Open `web-frontend/.env.production`
2. Update with your Render backend URL:
   ```env
   VITE_API_BASE_URL=https://equipment-backend.onrender.com/api
   ```
   ⚠️ Replace `equipment-backend` with your actual Render service name
   ⚠️ Include `/api` at the end!

3. **Commit and push** this change:
   ```bash
   git add web-frontend/.env.production
   git commit -m "Update production API URL"
   git push origin main
   ```

### Step 2: Create Netlify Account

1. Go to [netlify.com](https://netlify.com)
2. Click **"Sign up"**
3. Sign up with GitHub (recommended)

### Step 3: Create New Site

1. From Netlify dashboard, click **"Add new site"** → **"Import an existing project"**
2. Click **"Deploy with GitHub"**
3. If first time: Authorize Netlify to access your GitHub
4. Search for and select: `chemical_equipment_parameter_visualizer_fossee`
5. Click on your repository

### Step 4: Configure Build Settings

**Site settings:**
- **Branch to deploy**: `main`
- **Base directory**: `web-frontend`
- **Build command**: 
  ```bash
  npm install && npm run build
  ```
- **Publish directory**: 
  ```bash
  web-frontend/dist
  ```

### Step 5: Add Environment Variables

Click **"Show advanced"** → **"New variable"**

Add this environment variable:
- **Key**: `VITE_API_BASE_URL`
- **Value**: `https://equipment-backend.onrender.com/api`
  - ⚠️ Use your actual Render backend URL

### Step 6: Deploy Frontend

1. Click **"Deploy [your-repo-name]"**
2. Netlify will start building (takes 2-3 minutes)
3. Watch the deploy logs
4. Once complete, you'll get a URL like: `https://random-name-12345.netlify.app`

### Step 7: Get Your Frontend URL

1. Your site is live! Copy the URL
2. **Optional**: Click **"Site settings"** → **"Change site name"** to customize:
   - Example: `equipment-visualizer.netlify.app`

✅ **Frontend deployment complete!**

---

## 🔗 Part 3: Connect Backend and Frontend (2 minutes)

Now we need to update backend CORS settings with your actual frontend URL.

### Step 1: Update Backend Environment Variables

1. Go back to [Render dashboard](https://dashboard.render.com)
2. Click on your backend service: `equipment-backend`
3. Click **"Environment"** in left sidebar
4. Find and update these variables:

**CORS_ORIGINS:**
- Delete the old value
- Add your Netlify URL: `https://your-site.netlify.app`
- Example: `https://equipment-visualizer.netlify.app`

**CSRF_ORIGINS:**
- Same as CORS_ORIGINS: `https://your-site.netlify.app`

**ALLOWED_HOSTS:**
- Update to: `equipment-backend.onrender.com,your-site.netlify.app`
- Example: `equipment-backend.onrender.com,equipment-visualizer.netlify.app`

### Step 2: Save and Redeploy

1. Click **"Save Changes"**
2. Render will automatically redeploy your backend (takes ~2 minutes)
3. Wait for deployment to complete

---

## ✅ Part 4: Test Your Deployment

### Test Frontend

1. Visit your Netlify URL: `https://your-site.netlify.app`
2. You should see the landing page with rainbow gradients

### Test User Registration

1. Click **"Sign In"** or **"Get Started Free"**
2. Click **"Don't have an account? Register"**
3. Fill in the registration form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `TestPass123!`
4. Click **"Register"**
5. Should automatically log you in

### Test CSV Upload

1. You should now be in the dashboard
2. Click **"Choose File"** and upload a CSV file
3. Sample CSV format:
   ```csv
   Equipment Name,Equipment Type,Flowrate (L/min),Pressure (kPa),Temperature (°C)
   Pump A,Pump,150,500,80
   Heat Exchanger B,Heat Exchanger,200,600,150
   ```
4. Click **"Upload and Analyze"**
5. You should see:
   - Summary statistics
   - Bar charts
   - Doughnut chart
   - Line charts
   - Distribution histograms with threshold lines

### Test PDF Generation

1. After uploading data, click **"Generate PDF Report"**
2. PDF should download automatically

### Test Desktop App Download

1. Go back to landing page (click home icon)
2. Click **"Download Desktop App"**
3. `.exe` file should download

✅ **All tests passed? You're live! 🎉**

---

## 🔧 Troubleshooting

### Frontend shows "Network Error" or "Failed to fetch"

**Cause**: CORS is not configured correctly

**Fix**:
1. Go to Render → Your backend service → Environment
2. Double-check `CORS_ORIGINS` matches your Netlify URL **exactly**
3. Must include `https://` and no trailing slash
4. Save changes and wait for redeploy

### Backend shows "DisallowedHost" error

**Cause**: ALLOWED_HOSTS doesn't include your domain

**Fix**:
1. Go to Render → Environment
2. Update `ALLOWED_HOSTS` to include both:
   ```
   equipment-backend.onrender.com,your-site.netlify.app
   ```
3. Save and redeploy

### Netlify build fails

**Common causes**:
- Wrong base directory: Should be `web-frontend`
- Wrong publish directory: Should be `web-frontend/dist`
- Missing environment variable: Add `VITE_API_BASE_URL`

**Fix**:
1. Go to Netlify → Site settings → Build & deploy
2. Verify settings match Step 4 above
3. Trigger manual redeploy: Deploys → Trigger deploy → Deploy site

### Database connection error on Render

**Cause**: DATABASE_URL is incorrect

**Fix**:
1. Go to Render → Databases → Your database
2. Copy the **Internal Database URL** (not External!)
3. Go to your backend service → Environment
4. Update `DATABASE_URL` with the copied value
5. Save and redeploy

### Free tier limitations

**Render Free Tier:**
- ⚠️ Backend **spins down after 15 minutes** of inactivity
- First request after idle takes ~30-60 seconds to wake up
- Solution: Upgrade to paid plan ($7/month) for always-on service

**Netlify Free Tier:**
- 100GB bandwidth/month
- Unlimited sites
- No spin-down issues

---

## 💰 Cost Breakdown

### Free Tier (Recommended for development/testing)
- **Render Backend**: Free (with spin-down)
- **Render Database**: Free (PostgreSQL)
- **Netlify Frontend**: Free
- **Total**: **$0/month**

### Paid Tier (Recommended for production)
- **Render Backend**: $7/month (always-on, no spin-down)
- **Render Database**: Free or $7/month for bigger DB
- **Netlify Frontend**: Free (or $19/month for advanced features)
- **Total**: **$7-26/month**

---

## 🚀 Next Steps

### Custom Domain (Optional)

**For Netlify (Frontend):**
1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Follow instructions to add DNS records
4. SSL automatically provisioned

**For Render (Backend):**
1. Render automatically provides HTTPS
2. For custom domain: Settings → Custom domains
3. Note: Custom domains on paid plan only

### Enable Automatic Deploys

**Both platforms automatically deploy on git push!**
- Push to `main` branch
- Render and Netlify detect changes
- Both redeploy automatically
- Check deployment status in dashboards

### Monitoring

**Render:**
- Dashboard shows logs, metrics, deploy history
- Set up email alerts: Settings → Notifications

**Netlify:**
- Deploy notifications in dashboard
- Analytics available on Pro plan

---

## 📱 Update Desktop App API URL

If you've deployed backend, update the desktop app to use production API:

1. Open `desktop-app/api_client.py`
2. Update the base URL:
   ```python
   self.base_url = "https://equipment-backend.onrender.com"
   ```
3. Rebuild the executable:
   ```bash
   cd desktop-app
   pyinstaller --onefile --windowed --icon=fossee.ico main.py
   ```
4. Upload new version to GitHub Releases

---

## 🆘 Still Having Issues?

1. **Check Render logs**: Dashboard → Service → Logs
2. **Check Netlify logs**: Dashboard → Deploys → Deploy log
3. **Test backend directly**: Visit `https://your-backend.onrender.com/api/`
4. **Test frontend locally**: 
   ```bash
   cd web-frontend
   VITE_API_BASE_URL=https://your-backend.onrender.com/api npm run dev
   ```

### Common Error Messages

| Error | Location | Fix |
|-------|----------|-----|
| `CORS error` | Browser console | Update `CORS_ORIGINS` in Render |
| `DisallowedHost` | Render logs | Update `ALLOWED_HOSTS` in Render |
| `Module not found` | Render logs | Check `requirements.txt` is complete |
| `Build failed` | Netlify logs | Check build command and directory |
| `502 Bad Gateway` | Render | Service is starting, wait 30-60s |

---

## ✅ Deployment Checklist

- [ ] Backend deployed on Render
- [ ] PostgreSQL database created and connected
- [ ] Frontend deployed on Netlify
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] User registration tested
- [ ] CSV upload tested
- [ ] Charts display correctly
- [ ] PDF generation works
- [ ] Desktop app download works
- [ ] Custom domain configured (optional)
- [ ] Team members notified of URLs

---

## 📚 Resources

- [Render Documentation](https://render.com/docs)
- [Netlify Documentation](https://docs.netlify.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Project GitHub Repository](https://github.com/your-username/chemical_equipment_parameter_visualizer_fossee)

---

**🎉 Congratulations! Your application is now live!**

Share these URLs with your team:
- **Web App**: `https://your-site.netlify.app`
- **API**: `https://your-backend.onrender.com/api/`
- **Admin Panel**: `https://your-backend.onrender.com/admin/`
