# Streamlit Student Management App - Deployment Guide

## 📋 Overview

This Streamlit app provides a beautiful web interface to interact with your Django Student API. It supports all CRUD operations with a modern, user-friendly design.

## 🚀 Features

- ✅ View all students in a data table
- ✅ Add new students with profile images
- ✅ Update student information
- ✅ Delete students with confirmation
- ✅ View detailed student information
- ✅ Statistics dashboard (total students, average age, etc.)
- ✅ CSV export functionality
- ✅ Responsive design
- ✅ Real-time API integration

---

## 🏠 Local Development

### Prerequisites

1. **Django API Running**
   ```bash
   # Make sure your Django API is running on http://localhost:8000
   cd student_project
   python manage.py runserver
   ```

2. **Install Streamlit Dependencies**
   ```bash
   pip install -r streamlit_requirements.txt
   ```

### Run Locally

```bash
# Run the Streamlit app
streamlit run streamlit_app.py

# Open in browser (usually auto-opens)
# http://localhost:8501
```

---

## ☁️ Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

**Step 1: Prepare Your Repository**

```bash
# Create a GitHub repository
git init
git add .
git commit -m "Initial commit - Student Management App"
git branch -M main
git remote add origin https://github.com/yourusername/student-management-app.git
git push -u origin main
```

**Step 2: Deploy to Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `streamlit_app.py`
6. Click "Deploy"

**Step 3: Configure Secrets**

In Streamlit Cloud dashboard:
1. Go to App Settings → Secrets
2. Add your API URL:
```toml
API_URL = "https://your-django-api-url.com/api/students/"
```

**Important:** Your Django API must be publicly accessible for Streamlit Cloud to connect to it.

---

### Option 2: Heroku Deployment

**Step 1: Install Heroku CLI**
```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login
```

**Step 2: Create Heroku App**
```bash
# Create new Heroku app
heroku create your-student-app-name

# Add buildpack
heroku buildpacks:set heroku/python
```

**Step 3: Configure Environment**
```bash
# Set API URL as config var
heroku config:set API_URL="https://your-django-api.herokuapp.com/api/students/"
```

**Step 4: Deploy**
```bash
# Deploy to Heroku
git push heroku main

# Open the app
heroku open
```

---

### Option 3: Railway Deployment

**Step 1: Install Railway CLI**
```bash
npm install -g @railway/cli

# Login to Railway
railway login
```

**Step 2: Initialize Project**
```bash
# Initialize Railway project
railway init

# Link to new project
railway link
```

**Step 3: Add Environment Variables**
```bash
# Set API URL
railway variables set API_URL="https://your-django-api.railway.app/api/students/"
```

**Step 4: Deploy**
```bash
# Deploy to Railway
railway up
```

---

### Option 4: Render Deployment

**Step 1: Create render.yaml**

Create `render.yaml` in your project root:

```yaml
services:
  - type: web
    name: student-management-streamlit
    env: python
    buildCommand: pip install -r streamlit_requirements.txt
    startCommand: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: API_URL
        value: https://your-django-api.onrender.com/api/students/
```

**Step 2: Deploy**
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new "Web Service"
4. Render will auto-detect the render.yaml
5. Deploy

---

## 🔧 Configuration

### API URL Configuration

The app uses Streamlit secrets to manage the API URL. Configure it based on your deployment:

**For Streamlit Cloud:**
```toml
# In Streamlit Cloud dashboard → Settings → Secrets
API_URL = "https://your-deployed-django-api.com/api/students/"
```

**For Local Development:**
```toml
# In .streamlit/secrets.toml
API_URL = "http://localhost:8000/api/students/"
```

**For Heroku/Railway/Render:**
```bash
# Set as environment variable
API_URL="https://your-api-url.com/api/students/"
```

---

## 📁 Required Files

Make sure these files are in your repository:

```
project/
├── streamlit_app.py              # Main Streamlit application
├── streamlit_requirements.txt    # Python dependencies
├── Procfile                      # For Heroku deployment
├── setup.sh                      # Setup script
├── .streamlit/
│   ├── config.toml              # Streamlit configuration
│   └── secrets.toml             # API URL (local only)
└── README_STREAMLIT.md          # This file
```

---

## 🌐 Django API Requirements

Your Django API must be:

1. **Publicly Accessible**
   - Deployed on Heroku, Railway, Render, or similar
   - Has a public URL (HTTPS recommended)

2. **CORS Enabled**
   ```python
   # In Django settings.py
   INSTALLED_APPS = [
       ...
       'corsheaders',
   ]
   
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       ...
   ]
   
   # Allow Streamlit Cloud domains
   CORS_ALLOWED_ORIGINS = [
       "https://your-app.streamlit.app",
       "http://localhost:8501",  # For local testing
   ]
   
   # Or allow all (not recommended for production)
   CORS_ALLOW_ALL_ORIGINS = True
   ```

3. **Install django-cors-headers**
   ```bash
   pip install django-cors-headers
   ```

---

## 🐛 Troubleshooting

### Connection Error

**Problem:** "Connection error: ..."

**Solution:**
1. Check if Django API is running and accessible
2. Verify API_URL in secrets/environment variables
3. Check CORS configuration in Django
4. Ensure API endpoint ends with `/`

### 404 Not Found

**Problem:** "Student with id X not found"

**Solution:**
1. Check if student ID exists in database
2. Refresh the student list
3. Verify API endpoint URL

### Image Upload Issues

**Problem:** Images not uploading

**Solution:**
1. Check Django MEDIA_URL and MEDIA_ROOT settings
2. Ensure Pillow is installed: `pip install Pillow`
3. Verify Django file upload limits

### Deployment Errors

**Problem:** App crashes after deployment

**Solution:**
1. Check deployment logs
2. Verify all dependencies in streamlit_requirements.txt
3. Ensure API_URL is set correctly
4. Check Python version compatibility (3.8+)

---

## 📊 App Features Guide

### 1. View All Students
- Displays all students in a sortable table
- Shows statistics (total, average age, images count)
- Export to CSV functionality

### 2. Add New Student
- Form with name and age fields
- Optional profile image upload
- Real-time validation
- Success/error notifications

### 3. Update Student
- Select student from dropdown
- Edit name and age
- Shows current information
- Confirmation messages

### 4. Delete Student
- Select student to delete
- Confirmation required
- Safety warning before deletion

### 5. Student Details
- Full student information
- Profile image display
- Quick action buttons
- Formatted timestamps

---

## 🔒 Security Best Practices

1. **Never commit secrets.toml to Git**
   ```bash
   # Add to .gitignore
   echo ".streamlit/secrets.toml" >> .gitignore
   ```

2. **Use HTTPS for API**
   - Deploy Django API with SSL certificate
   - Use https:// URLs only in production

3. **Environment Variables**
   - Store API credentials securely
   - Use platform-specific secret management

4. **API Authentication** (Optional Enhancement)
   - Add token-based authentication
   - Implement API keys
   - Use Django REST Framework authentication

---

## 📱 Mobile Responsiveness

The app is fully responsive and works on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktop computers
- 🖥️ Large displays

---

## 🎨 Customization

### Change Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"        # Your brand color
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Modify Layout

Edit `streamlit_app.py`:

```python
# Change page configuration
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="🎯",
    layout="wide"  # or "centered"
)
```

---

## 📈 Performance Tips

1. **Caching API Calls**
   ```python
   @st.cache_data(ttl=60)  # Cache for 60 seconds
   def get_all_students():
       # Your API call
   ```

2. **Minimize Reruns**
   - Use session state effectively
   - Implement proper form handling

3. **Optimize Images**
   - Compress images before upload
   - Use appropriate image formats (JPEG for photos)

---

## 🚀 Next Steps

After deployment:

1. ✅ Test all CRUD operations
2. ✅ Verify image uploads work
3. ✅ Check mobile responsiveness
4. ✅ Share app URL with users
5. ✅ Monitor usage and errors

---

## 📞 Support

For issues or questions:
- Check Streamlit documentation: https://docs.streamlit.io
- Django REST Framework docs: https://www.django-rest-framework.org
- Review deployment platform docs

---

## 🎉 Quick Deploy Checklist

- [ ] Django API deployed and accessible
- [ ] CORS configured in Django
- [ ] Streamlit app repository on GitHub
- [ ] secrets.toml or environment variables configured
- [ ] All files committed to repository
- [ ] Deployment platform selected
- [ ] App deployed successfully
- [ ] API_URL configured correctly
- [ ] All features tested
- [ ] Mobile tested

---

## Example Deployment URLs

After deployment, your app will be accessible at:

- **Streamlit Cloud:** `https://your-app-name.streamlit.app`
- **Heroku:** `https://your-app-name.herokuapp.com`
- **Railway:** `https://your-app-name.railway.app`
- **Render:** `https://your-app-name.onrender.com`

Make sure to update your API_URL with your actual Django backend URL!
