# 🍽️ Calorie Tracker - AI-Powered PWA

A Progressive Web App that uses AI to recognize food from photos and track calories with hyper-accurate nutrition data.

## ✨ Features

- **🤖 AI Food Recognition**: Upload photos to automatically identify food items
- **📊 Hyper-Accurate Nutrition**: Multi-tiered accuracy system (Enhanced DB → USDA API → Web Search → Smart Fallbacks)
- **🎯 Customizable Goals**: Set personal calorie, protein, fat, and carb targets
- **📱 Progressive Web App**: Installable on mobile with offline functionality
- **🔧 Debug Analysis**: Detailed AI decision logging for troubleshooting
- **📈 Real-time Stats**: Live dashboard with progress tracking
- **🗄️ Smart Storage**: Automatic image cleanup and archival system

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **AI**: Ollama Cloud API for food recognition
- **Frontend**: Bootstrap 5 with custom JavaScript
- **Image Processing**: Pillow (PIL) for image handling
- **Authentication**: Flask-Login with bcrypt password hashing

## 🚀 Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### Launch the App

```bash
# Clone or navigate to the project directory
cd calorieApp

# Start the application
docker compose up -d

# The app will be available at:
# http://localhost:5151
```

### Stop the App

```bash
docker compose down
```

### View Logs

```bash
docker compose logs -f calorie-tracker
```

### Manual Setup (Alternative)

If you prefer to set up manually:

1. **Create virtual environment**:
   ```bash
   python3 -m venv calorie_env
   source calorie_env/bin/activate  # On Windows: calorie_env\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**:
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## 📱 How to Use

1. **Create an Account**:
   - Click "Register" to create a new account
   - Fill in your username, email, and password

2. **Log Your First Meal**:
   - Click "Log Food" in the navigation
   - Upload a photo of your food
   - Wait for AI analysis
   - Review and edit the results if needed
   - Save the entry

3. **View Your History**:
   - Click "History" to see all logged meals
   - Filter by date or search for specific foods
   - Edit entries by clicking the pencil icon

4. **Track Your Progress**:
   - View daily summaries on the dashboard
   - Monitor your calorie and nutrition intake

## 🔧 Configuration

### Ollama Cloud API

The app uses Ollama Cloud for AI food recognition with the following configuration:

- **Model**: `gpt-oss:120b` (GPT-based model optimized for visual understanding)
- **API Key**: `fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg`

The API key is currently configured in `food_recognition.py`. For production use or if you want to use your own API key:

1. Get your own API key from [Ollama Cloud](https://ollama.com)
2. Set it as an environment variable:
   ```bash
   export OLLAMA_API_KEY="your-api-key-here"
   ```
3. Or modify the API_KEY constant in `food_recognition.py`

### Database Configuration

By default, the app uses SQLite with a local database file `calorie_tracker.db`. For production, you may want to use PostgreSQL or MySQL by updating the database URL in `app.py`.

## 📁 Project Structure

```
calorieApp/
├── app.py                 # Main Flask application
├── food_recognition.py    # AI food recognition module
├── calorie_calculator.py  # Calorie calculation logic
├── requirements.txt       # Python dependencies
├── start.sh              # Startup script
├── database_schema.sql   # Database schema documentation
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── upload.html
│   ├── edit_entry.html
│   ├── history.html
│   └── dashboard.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── uploads/         # Uploaded food images
└── calorie_env/         # Virtual environment (created after setup)
```

## 🔒 Security Notes

- Passwords are hashed using bcrypt
- File uploads are validated for type and size
- SQL injection protection via SQLAlchemy ORM
- XSS protection via Jinja2 template escaping

## 🐛 Troubleshooting

### Common Issues

1. **"python command not found"**:
   - Use `python3` instead of `python`
   - Make sure Python 3.8+ is installed

2. **Import errors**:
   - Make sure you activated the virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Database errors**:
   - Delete `calorie_tracker.db` and restart the app
   - The database will be recreated automatically

4. **Upload issues**:
   - Check that the `static/uploads/` directory exists
   - Verify image file types (JPG, PNG, GIF only)
   - Ensure images are under 16MB

## 🚀 Deployment

For production deployment, consider:

1. **Use a production WSGI server** (like Gunicorn)
2. **Set up a reverse proxy** (like Nginx)
3. **Use environment variables** for sensitive configuration
4. **Use a production database** (PostgreSQL/MySQL)
5. **Set up SSL/HTTPS**
6. **Configure proper logging**

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Ollama Cloud for AI food recognition
- USDA Food Data Central for nutrition information
- Bootstrap team for the UI framework
- Flask community for the excellent web framework

---

**Made with ❤️ and AI by Claude Code**

For questions or support, please create an issue in the repository.