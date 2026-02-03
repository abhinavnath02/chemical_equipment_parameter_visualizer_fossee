# Chemical Equipment Parameter Visualizer

A hybrid **Web + Desktop** application for analyzing and visualizing chemical equipment parameters. Built with Django backend, React web frontend, and PyQt5 desktop application.

## 📊 Features

### Core Functionality
- **CSV Upload & Analysis** - Import equipment data from CSV files
- **Data Visualization** - Bar charts, doughnut charts, and line graphs
- **Summary Statistics** - Equipment counts and parameter averages
- **Smart Insights** - AI-powered pattern detection and anomaly analysis
- **Safety Alerts** - Configurable threshold warnings for critical parameters
- **Upload History** - Track and review past uploads
- **PDF Reports** - Generate downloadable PDF reports
- **Dark Theme** - Consistent dark mode across all platforms

### Authentication
- User registration with email validation
- JWT token-based authentication
- Password strength requirements
- Auto-login after registration

## 🏗️ Architecture

```
┌──────────────────────┐              ┌──────────────────────┐
│    WEB FRONTEND      │              │   DESKTOP FRONTEND   │
│      React +         │              │       PyQt5 +        │
│    TypeScript        │              │      Matplotlib      │
└──────────┬───────────┘              └──────────┬───────────┘
           │         HTTP REST API               │
           └────────────────┬────────────────────┘
                            ▼
           ┌────────────────────────────────────┐
           │          DJANGO BACKEND            │
           │   Django REST Framework + Pandas   │
           │            SQLite DB               │
           └────────────────────────────────────┘
```

### Project Structure

```
chemical_equipment_parameter_visualizer/
├── backend/              # Django REST API
│   ├── backend/          # Project settings
│   └── equipment/        # Main app (views, models, serializers)
├── web-frontend/         # React Web App
│   └── src/
│       ├── components/   # UI components (charts, forms, tables)
│       ├── context/      # Auth context
│       └── types/        # TypeScript types
└── desktop-app/          # PyQt5 Desktop App
    ├── main.py           # Entry point
    ├── auth_window.py    # Authentication window
    ├── dashboard.py      # Main dashboard
    └── api_client.py     # API client
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** (for web frontend)
- **Git**

### 1. Clone Repository

```bash
git clone https://github.com/abhinavnath02/chemical_equipment_parameter_visualizer_fossee.git
cd chemical_equipment_parameter_visualizer_fossee
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000`

### 3. Web Frontend Setup

```bash
cd web-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Web app runs at: `http://localhost:5173`

### 4. Desktop App Setup

```bash
cd desktop-app

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

**Quick Start on Windows:**
```bash
cd desktop-app
start.bat
```

## 📁 CSV Format

Your CSV file should have these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Equipment Name | Unique identifier | Pump-001 |
| Type | Equipment category | Pump, Reactor, Valve, Heat Exchanger |
| Flowrate | Flow rate value | 150.5 |
| Pressure | Pressure value | 10.2 |
| Temperature | Temperature value | 45.3 |

**Example CSV:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,10.2,45.3
Reactor-001,Reactor,200.0,15.5,80.0
Heat Exchanger-001,Heat Exchanger,180.0,12.0,65.5
Valve-001,Valve,120.0,8.5,35.0
```

## 🔧 Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Django 6.0 | Web framework |
| Django REST Framework | API development |
| SimpleJWT | JWT authentication |
| Pandas | Data processing & analytics |
| ReportLab | PDF generation |
| SQLite | Database |

### Web Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI library |
| TypeScript | Type safety |
| Vite | Build tool |
| Tailwind CSS v4 | Styling |
| Chart.js | Data visualization |

### Desktop App
| Technology | Purpose |
|------------|---------|
| PyQt5 | GUI framework |
| Matplotlib | Chart generation |
| Requests | HTTP client |
| Pandas | Data processing |

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET | `/api/auth/user/` | Get user profile |
| POST | `/api/upload/` | Upload CSV file |
| GET | `/api/history/` | Get upload history |
| POST | `/api/generate-pdf/` | Generate PDF report |

## 🌟 Features Comparison

| Feature | Web App | Desktop App |
|---------|:-------:|:-----------:|
| Authentication | ✅ | ✅ |
| CSV Upload | ✅ | ✅ |
| Interactive Charts | ✅ | ✅ |
| Data Table | ✅ | ✅ |
| Smart Insights | ✅ | ✅ |
| Safety Alerts | ✅ | ✅ |
| Upload History | ✅ | ✅ |
| PDF Reports | ✅ | ✅ |
| Responsive Design | ✅ | ❌ |
| Native Performance | ❌ | ✅ |

## 📸 Screenshots

### Web Application
<img width="1919" alt="Web Dashboard" src="https://github.com/user-attachments/assets/620fd227-fac5-4cd1-b5f8-6f71607380b7" />
<img width="1919" alt="Charts View" src="https://github.com/user-attachments/assets/396d8fbd-eab3-42bf-8b7b-055d85bcf360" />
<img width="1919" alt="Data Table" src="https://github.com/user-attachments/assets/9f846c04-2667-40cd-b878-b1799828c074" />
<img width="1919" alt="Smart Insights" src="https://github.com/user-attachments/assets/73f9a13d-233d-4300-bde2-7e806942edce" />
<img width="1919" alt="Safety Alerts" src="https://github.com/user-attachments/assets/b7b67c2c-d6bd-4bf5-b88d-992af99f6339" />

### Desktop Application
<img width="449" alt="Login Window" src="https://github.com/user-attachments/assets/d7ae22fe-b657-4e30-9758-29dd49e01d1b" />
<img width="1401" alt="Desktop Dashboard" src="https://github.com/user-attachments/assets/933b516b-83f0-4ced-8f88-528c3c71c631" />
<img width="1396" alt="Desktop Charts" src="https://github.com/user-attachments/assets/01bc5559-9b0d-454e-84d0-b4b2e212e7c7" />
<img width="1390" alt="Desktop Data View" src="https://github.com/user-attachments/assets/14e9a12f-2221-4488-ae18-1a95e00b4a52" />

## 🐛 Troubleshooting

### Backend Issues

**Migration errors:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Port already in use:**
```bash
python manage.py runserver 8001
```

### Frontend Issues

**Package conflicts:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Desktop App Issues

**Connection refused:**
- Ensure backend is running at `http://127.0.0.1:8000`
- Check firewall settings

**Display scaling issues (Windows):**
```bash
set QT_SCALE_FACTOR=1.0
python main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 👥 Author

Developed by **Abhinav Nath** as part of the Chemical Equipment Parameter Visualizer project for the FOSSEE Fellowship.

## 🙏 Acknowledgments

- FOSSEE
- Django REST Framework
- React and Vite teams
- PyQt5 developers
- Chart.js and Matplotlib communities
