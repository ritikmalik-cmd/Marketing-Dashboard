# TOML Configuration Format for Marketing Dashboard

## 📋 Complete TOML Configuration

Here's your complete configuration in TOML format for use with Streamlit Cloud or any TOML-based configuration system.

### 🔐 Full Configuration (secrets.toml)

```toml
[zoho]
client_id = "1000.JY4N7CSGP5S31JKJFEMJTSBZGJL2EJ"
client_secret = "60ab68b202ff2d73e9113cadeaf6f17218c8e3febb"
refresh_token = "1000.985a431241ab09913d864dfa4e3d66fd.1658f0fc3616853d44d9dcac4ef42104"

[dashboard]
app_title = "Marketing Leads Dashboard"
max_leads = 5000
default_date_range = 7

[team]
target_emails = [
    "aakib.posharkar@xmonks.com",
    "ankita.vinayak@xmonks.com",
    "preeti@erickson.co.in",
    "rejna.balan@xmonks.com",
    "saurav.tiwari@xmonks.com"
]

[sources]
target_sources = [
    "Google Ads 2025",
    "Whatsapp Marketing",
    "Form Submission",
    "Self Created"
]
```

## 📂 File Locations

### Local Development
- **File:** `.streamlit/secrets.toml`
- **Location:** `C:\Users\xMonks\Downloads\New Dashboard\.streamlit\secrets.toml`
- **Usage:** Automatically loaded by Streamlit when running locally

### Streamlit Cloud
- **Method:** Set secrets via app settings dashboard
- **Format:** Copy the TOML sections above into the "Secrets" field
- **Access:** Streamlit reads from `st.secrets`

### Docker/Containers
- **Method:** Mount secrets as environment variables
- **Format:** Convert TOML to environment variables

## 🔄 TOML Configuration Breakdown

### **[zoho] Section**
Zoho CRM API credentials:
```toml
[zoho]
client_id = "1000.JY4N7CSGP5S31JKJFEMJTSBZGJL2EJ"        # Your OAuth Client ID
client_secret = "60ab68b202ff2d73e9113cadeaf6f17218c8e3febb"  # Your OAuth Secret
refresh_token = "1000.985a431241ab09913d864dfa4e3d66fd.1658f0fc3616853d44d9dcac4ef42104"  # Refresh token for long-lived access
```

### **[dashboard] Section**
Dashboard configuration:
```toml
[dashboard]
app_title = "Marketing Leads Dashboard"    # Page title in browser
max_leads = 5000                           # Maximum leads to fetch
default_date_range = 7                     # Default date range in days
```

### **[team] Section**
Team member emails (array format):
```toml
[team]
target_emails = [
    "aakib.posharkar@xmonks.com",
    "ankita.vinayak@xmonks.com",
    "preeti@erickson.co.in",
    "rejna.balan@xmonks.com",
    "saurav.tiwari@xmonks.com"
]
```

### **[sources] Section**
Lead source categories (array format):
```toml
[sources]
target_sources = [
    "Google Ads 2025",
    "Whatsapp Marketing",
    "Form Submission",
    "Self Created"
]
```

## 🚀 Deployment Instructions

### 1. **Local Development**
```bash
# File is automatically used from .streamlit/secrets.toml
streamlit run full_dashboard.py
```

### 2. **Streamlit Cloud**
```
1. Go to app.streamlit.io
2. Deploy your repository
3. In Settings → Secrets
4. Paste your TOML configuration
5. Deploy and restart
```

### 3. **Docker Container**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Set environment variables
ENV STREAMLIT_SECRETS_ZOHO_CLIENT_ID=1000.JY4N7CSGP5S31JKJFEMJTSBZGJL2EJ
ENV STREAMLIT_SECRETS_ZOHO_CLIENT_SECRET=60ab68b202ff2d73e9113cadeaf6f17218c8e3febb
ENV STREAMLIT_SECRETS_ZOHO_REFRESH_TOKEN=1000.985a431241ab09913d864dfa4e3d66fd.1658f0fc3616853d44d9dcac4ef42104

EXPOSE 8501
CMD ["streamlit", "run", "full_dashboard.py"]
```

## 📝 TOML vs Other Formats

### TOML Format (Recommended for Streamlit)
```toml
[zoho]
client_id = "value"
[team]
emails = ["email1@company.com", "email2@company.com"]
```

### JSON Format
```json
{
  "zoho": {
    "client_id": "value"
  },
  "team": {
    "emails": ["email1@company.com", "email2@company.com"]
  }
}
```

### YAML Format
```yaml
zoho:
  client_id: value
team:
  emails:
    - email1@company.com
    - email2@company.com
```

### Environment Variables Format
```
STREAMLIT_SECRETS_ZOHO_CLIENT_ID=value
STREAMLIT_SECRETS_TEAM_EMAILS=email1@company.com,email2@company.com
```

## ✅ Usage in Python Code

### Reading TOML Configuration
```python
import streamlit as st

# Access Zoho credentials
zoho_client_id = st.secrets["zoho"]["client_id"]
zoho_client_secret = st.secrets["zoho"]["client_secret"]
zoho_refresh_token = st.secrets["zoho"]["refresh_token"]

# Access dashboard config
app_title = st.secrets["dashboard"]["app_title"]
max_leads = st.secrets["dashboard"]["max_leads"]

# Access team emails
target_emails = st.secrets["team"]["target_emails"]

# Access sources
target_sources = st.secrets["sources"]["target_sources"]
```

### Error Handling
```python
try:
    client_id = st.secrets["zoho"]["client_id"]
except KeyError as e:
    st.error(f"Missing configuration: {e}")
    st.stop()
```

## 🔐 Security Best Practices

✅ **Do:**
- Store `.streamlit/secrets.toml` in `.gitignore`
- Use environment variables for production
- Rotate credentials regularly
- Use different credentials for dev/prod

❌ **Don't:**
- Commit secrets to Git
- Hardcode credentials in source code
- Share credentials via chat/email
- Use same credentials for all environments

## 📚 Related Files

- `.streamlit/secrets.toml` - Your actual secrets (⚠️ NEVER commit)
- `.streamlit/secrets.example.toml` - Template for team (safe to share)
- `.streamlit/config.toml` - App configuration (can commit)
- `.env` - Alternative format using python-dotenv
- `ENVIRONMENT_SETUP.md` - Detailed setup guide

## 🔄 Converting Between Formats

### TOML to Environment Variables
```bash
# TOML
[zoho]
client_id = "abc123"

# Becomes
export STREAMLIT_SECRETS_ZOHO_CLIENT_ID=abc123
```

### TOML to JSON
```bash
# Use: pip install toml json
python -c "import toml, json; print(json.dumps(toml.load('secrets.toml')))"
```

---

**Format:** TOML (Tom's Obvious, Minimal Language)  
**Status:** ✅ Production Ready  
**Last Updated:** November 10, 2025