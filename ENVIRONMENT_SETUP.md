# Environment Variables Setup Guide

## 🔐 Security Best Practices

Your Zoho CRM credentials are now stored in environment variables and protected from being committed to Git.

## 📋 Files Created

### 1. `.env` File
Located at: `C:\Users\xMonks\Downloads\New Dashboard\.env`

**Contents:**
```
ZOHO_CLIENT_ID=1000.JY4N7CSGP5S31JKJFEMJTSBZGJL2EJ
ZOHO_CLIENT_SECRET=60ab68b202ff2d73e9113cadeaf6f17218c8e3febb
ZOHO_REFRESH_TOKEN=1000.985a431241ab09913d864dfa4e3d66fd.1658f0fc3616853d44d9dcac4ef42104
```

### 2. `.env.example` File
Located at: `C:\Users\xMonks\Downloads\New Dashboard\.env.example`

**Purpose:** Template file to share with team without sensitive data

**Contents:**
```
ZOHO_CLIENT_ID=your_client_id_here
ZOHO_CLIENT_SECRET=your_client_secret_here
ZOHO_REFRESH_TOKEN=your_refresh_token_here
```

### 3. Updated `.gitignore`
- `.env` - Prevents local environment file from being committed
- `.env.local` - Prevents local variations from being committed
- `.env.*.local` - Prevents environment-specific files from being committed

## 🚀 How It Works

### Loading Environment Variables

Your `full_dashboard.py` now:

1. **Imports dotenv:**
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   ```

2. **Reads from .env file:**
   ```python
   ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
   ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
   ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
   ```

3. **Validates credentials:**
   ```python
   if not all([ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN]):
       st.error("❌ Missing Zoho CRM credentials!")
       st.stop()
   ```

## 🎯 Usage Instructions

### Local Development

1. **Run the dashboard:**
   ```bash
   streamlit run full_dashboard.py
   ```

2. The app will automatically load credentials from `.env`

### Deployment Options

#### Option 1: Streamlit Cloud
1. Go to app settings in Streamlit Cloud
2. Add secrets in the "Secrets" section:
   ```toml
   ZOHO_CLIENT_ID = "your_client_id"
   ZOHO_CLIENT_SECRET = "your_client_secret"
   ZOHO_REFRESH_TOKEN = "your_refresh_token"
   ```

#### Option 2: Docker/Container
Set environment variables:
```bash
docker run -e ZOHO_CLIENT_ID="value" -e ZOHO_CLIENT_SECRET="value" -e ZOHO_REFRESH_TOKEN="value" your_image
```

#### Option 3: Traditional Server
Set system environment variables:

**Windows (PowerShell):**
```powershell
$env:ZOHO_CLIENT_ID = "your_client_id"
$env:ZOHO_CLIENT_SECRET = "your_client_secret"
$env:ZOHO_REFRESH_TOKEN = "your_refresh_token"
```

**Linux/Mac (Bash):**
```bash
export ZOHO_CLIENT_ID="your_client_id"
export ZOHO_CLIENT_SECRET="your_client_secret"
export ZOHO_REFRESH_TOKEN="your_refresh_token"
```

## ✅ Security Checklist

- [x] Credentials removed from source code
- [x] `.env` file added to `.gitignore`
- [x] `.env.example` created for team reference
- [x] Environment variable validation in code
- [x] Error messages if credentials missing
- [x] Python-dotenv package installed
- [x] All team members can use `.env.example` template

## 📦 Installing python-dotenv

The package has been automatically installed in your virtual environment:

```bash
pip install python-dotenv
```

If you need to reinstall:
```bash
.venv\Scripts\pip install python-dotenv
```

## 🔄 Sharing with Team

1. **DO share:** `.env.example` (template file)
2. **DO NOT share:** `.env` (contains real credentials)
3. **Team setup:** Each team member should:
   - Copy `.env.example` to `.env`
   - Fill in their own or shared credentials
   - Never commit `.env` to Git

## 🚨 If Credentials Are Exposed

If you accidentally commit `.env` or credentials to Git:

1. **Revoke credentials immediately** in Zoho CRM
2. **Generate new credentials**
3. **Update `.env` with new values**
4. **Remove from Git history** (if already pushed)

## ❓ Troubleshooting

### Error: "Missing Zoho CRM credentials"
- Ensure `.env` file exists in project root
- Verify environment variables are spelled correctly
- Check that values don't have quotes in `.env`

### Credentials not loading
```python
# Debug: Print loaded values (remove before production)
import os
print(f"Client ID: {os.getenv('ZOHO_CLIENT_ID')}")
```

### Module not found: dotenv
```bash
pip install python-dotenv
```

## 📚 Related Files

- `full_dashboard.py` - Updated to use environment variables
- `full_dashboard_secure.py` - Alternative using Streamlit secrets
- `.streamlit/secrets.toml` - For Streamlit Cloud deployment
- `.env.example` - Template for team members

---

**Last Updated:** November 10, 2025
**Security Status:** ✅ Production Ready