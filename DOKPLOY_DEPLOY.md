# 🐳 Dokploy Deployment Guide

Deploy FinanceBot to your VPS using Dokploy in 5 minutes!

## 📋 Prerequisites

1. VPS with Docker installed
2. Dokploy installed on your VPS
3. Domain name (optional, for HTTPS)

---

## 🚀 Quick Deploy Steps

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Ready for Dokploy deployment"
git push origin main
```

---

### 2. Setup in Dokploy

1. **Login to Dokploy Dashboard**
   - Access your Dokploy instance (usually `http://your-vps-ip:3000`)

2. **Create New Application**
   - Click "New Application"
   - Select "Docker Compose"
   - Name: `financebot`

3. **Connect GitHub Repository**
   - Select your repository
   - Branch: `main`

4. **Configure Build**
   - **Docker Compose File Path:** `docker-compose.yml`
   - **Environment File:** `.env` (or set variables in Dokploy)

5. **Add Environment Variables**

   Go to **Environment Variables** section and add:

   ```env
   PIXPOC_API_BASE_URL=https://app.pixpoc.ai
   PIXPOC_API_KEY=your_actual_api_key
   PIXPOC_AGENT_ID=your_actual_agent_id
   PIXPOC_COACHING_AGENT_ID=your_coaching_agent_id
   PIXPOC_FROM_NUMBER_ID=your_from_number_id
   BACKEND_URL=http://backend:8000
   ```

6. **Deploy!**
   - Click "Deploy"
   - Wait for build to complete (~5-10 minutes first time)

---

## 🌐 Configure Domains (Optional)

### Setup Reverse Proxy

1. **In Dokploy:**
   - Go to your application
   - Navigate to "Domains" section
   - Add your domain: `app.yourdomain.com`
   - Dokploy will auto-configure nginx/Caddy

2. **For API (Backend):**
   - Add subdomain: `api.yourdomain.com`
   - Point to backend service on port 8000

3. **SSL Certificates:**
   - Dokploy handles Let's Encrypt automatically
   - Or add your own certificates

---

## ⚙️ Environment Variables Reference

### Required:
- `PIXPOC_API_KEY` - Your Pixpoc API key
- `PIXPOC_AGENT_ID` - Your Pixpoc agent ID

### Optional:
- `PIXPOC_API_BASE_URL` - Default: `https://app.pixpoc.ai`
- `PIXPOC_FROM_NUMBER_ID` - Specific from number
- `BACKEND_URL` - Backend URL for frontend (default: `http://backend:8000`)
- `OLLAMA_BASE_URL` - If using external Ollama instance
- `OLLAMA_MODEL` - Model name (default: `mistral-nemo`)

---

## 🔧 Manual Docker Compose Deploy

If you prefer to deploy manually without Dokploy:

```bash
# Clone repository
git clone <your-repo>
cd hackathone_finetech

# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📊 Access Your Application

After deployment:

- **Frontend:** `http://your-vps-ip:3000` or `https://app.yourdomain.com`
- **Backend API:** `http://your-vps-ip:8000` or `https://api.yourdomain.com`
- **API Docs:** `https://api.yourdomain.com/docs`

---

## 🔄 Update Pixpoc Webhook

1. Go to Pixpoc Dashboard
2. Settings → Webhooks
3. Add webhook URL: `https://api.yourdomain.com/webhook/pixpoc`
   (Or `http://your-vps-ip:8000/webhook/pixpoc` if no domain)

---

## 🐛 Troubleshooting

### Build Fails
- Check Docker logs in Dokploy dashboard
- Ensure all environment variables are set
- Verify `docker-compose.yml` syntax

### Services Not Starting
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart
```

### Database/Reports Not Persisting
- Volumes are mounted in `docker-compose.yml`
- Check volume permissions on VPS
- Ensure `./database` and `./reports` directories exist

### Frontend Can't Connect to Backend
- Verify `BACKEND_URL` environment variable
- Check network connectivity between containers
- Ensure backend health check passes

---

## 🔒 Security Tips

1. **Use HTTPS:**
   - Configure domains with SSL in Dokploy
   - Never expose API keys in frontend code

2. **Firewall:**
   - Only expose ports 80, 443
   - Keep 3000, 8000 behind reverse proxy

3. **Environment Variables:**
   - Never commit `.env` file
   - Use Dokploy's secure environment variable storage

---

## 📈 Monitoring

Dokploy provides:
- Container health checks
- Log viewing
- Resource usage metrics
- Auto-restart on failure

Check these in your Dokploy dashboard!

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Dokploy application created
- [ ] Environment variables configured
- [ ] Build successful
- [ ] Services running (check logs)
- [ ] Frontend accessible
- [ ] Backend API responding
- [ ] Pixpoc webhook configured
- [ ] Test login working
- [ ] SSL certificates configured (if using domain)

---

**That's it! Your app is live on your VPS! 🚀**

