# Chemical Equipment Parameter Visualizer

A hybrid **Web + Desktop** application for analyzing and visualizing chemical equipment parameters. Built with Django backend, React web frontend, and PyQt5 desktop application.

## 📊 Features

### Core Functionality
- **CSV Upload & Analysis** - Import equipment data from CSV files
- **Data Visualization** - Bar charts, doughnut charts, and line graphs
- **Summary Statistics** - Equipment counts and parameter averages
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
chemical_equipment_parameter_visualizer/
├── backend/              # Django REST API
│   ├── backend/          # Project settings
│   └── equipment/        # Main app
├── web-frontend/         # React Web App
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── context/      # Auth context
│   │   └── api.ts        # API client
│   └── public/
└── desktop-app/          # PyQt5 Desktop App
    ├── main.py           # Entry point
    ├── auth_window.py    # Authentication
    ├── dashboard.py      # Main window
    └── api_client.py     # API client
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** (for web frontend)
- **Git**

### 1. Clone Repository

```bash
git clone <repository-url>
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

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

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

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,10.2,45.3
Reactor-001,Reactor,200.0,15.5,80.0
Heat Exchanger-001,Heat Exchanger,180.0,12.0,65.5
```

Sample files provided:
- `sample_data.csv` (root directory)
- `desktop-app/sample_data.csv`

## 🎨 Design System

### Color Palette

```
Background:      #000000 (black)
Cards:           #18181b (zinc-900)
Inputs:          #27272a (zinc-800)
Borders:         #3f3f46 (zinc-700)
Primary Text:    #ffffff (white)
Secondary Text:  #a1a1aa (zinc-400)
Error:           #ef4444 (red)
```

### Components
- **Buttons:** White primary, zinc-800 secondary, 8px border radius
- **Cards:** Zinc-900 background, rounded borders, 16px padding
- **Charts:** Dark backgrounds with colored data series
- **Scrollbars:** Custom 8px thin scrollbars matching theme

## 🔧 Technology Stack

### Backend
- **Django 6.0.1** - Web framework
- **Django REST Framework** - API development
- **djangorestframework-simplejwt** - JWT authentication
- **django-cors-headers** - CORS handling
- **Pandas** - Data processing
- **ReportLab** - PDF generation

### Web Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite 7.3.1** - Build tool
- **Tailwind CSS v4** - Styling
- **Chart.js** - Data visualization
- **react-chartjs-2** - React Chart.js wrapper

### Desktop Frontend
- **PyQt5 5.15.9** - GUI framework
- **matplotlib 3.8.0** - Chart generation
- **requests 2.31.0** - HTTP client
- **pandas 2.1.0** - Data processing

## 📖 API Endpoints

```
POST   /api/auth/register/      # Register new user
POST   /api/auth/login/         # Login and get JWT tokens
POST   /api/auth/token/refresh/ # Refresh access token
GET    /api/auth/user/          # Get user profile
POST   /api/upload/             # Upload CSV file
GET    /api/history/            # Get upload history
POST   /api/generate-pdf/       # Generate PDF report
```

## 📚 Documentation

- [Backend Documentation](backend/README.md)
- [Web Frontend Documentation](web-frontend/README.md)
- [Desktop App Documentation](desktop-app/README.md)
- [Implementation Details](desktop-app/IMPLEMENTATION.md)
- [Project Plan](plan.md)

## 🧪 Testing

### Test Backend
```bash
cd backend
python manage.py test
```

### Test Web Frontend
```bash
cd web-frontend
npm test
```

### Test Desktop Dependencies
```bash
cd desktop-app
python test_dependencies.py
```

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

**Build errors:**
```bash
npm run build
```

### Desktop App Issues

**Import errors:**
```bash
pip install --upgrade -r requirements.txt
```

**Connection refused:**
- Ensure backend is running at `http://127.0.0.1:8000`
- Check firewall settings

**Display scaling:**
```bash
set QT_SCALE_FACTOR=1.0
python main.py
```

## 🌟 Features Comparison

| Feature | Web App | Desktop App |
|---------|---------|-------------|
| Authentication | ✅ | ✅ |
| CSV Upload | ✅ | ✅ |
| Charts | ✅ (Chart.js) | ✅ (matplotlib) |
| Data Table | ✅ | ✅ |
| History | ✅ | ✅ |
| PDF Download | ✅ | ✅ |
| Responsive | ✅ | ❌ |
| Offline Mode | ❌ | Partial |
| Native Performance | ❌ | ✅ |

## 📸 Screenshots

### Web Application
<img width="1919" height="906" alt="Screenshot 2026-01-27 150535" src="https://github.com/user-attachments/assets/620fd227-fac5-4cd1-b5f8-6f71607380b7" />
<img width="1919" height="908" alt="Screenshot 2026-01-27 150548" src="https://github.com/user-attachments/assets/396d8fbd-eab3-42bf-8b7b-055d85bcf360" />
<img width="1919" height="894" alt="Screenshot 2026-01-27 150605" src="https://github.com/user-attachments/assets/9f846c04-2667-40cd-b878-b1799828c074" />
<img width="1919" height="911" alt="Screenshot 2026-01-27 150624" src="https://github.com/user-attachments/assets/73f9a13d-233d-4300-bde2-7e806942edce" />
<img width="1919" height="917" alt="Screenshot 2026-01-27 150640" src="https://github.com/user-attachments/assets/b7b67c2c-d6bd-4bf5-b88d-992af99f6339" />
<img width="1919" height="913" alt="Screenshot 2026-01-27 150658" src="https://github.com/user-attachments/assets/b77d6213-fcca-4a91-8ac8-fea33b931705" />


### Desktop Application
<img width="449" height="600" alt="Screenshot 2026-01-27 151022" src="https://github.com/user-attachments/assets/d7ae22fe-b657-4e30-9758-29dd49e01d1b" />
<img width="1401" height="901" alt="Screenshot 2026-01-27 151045" src="https://github.com/user-attachments/assets/933b516b-83f0-4ced-8f88-528c3c71c631" />
<img width="1396" height="894" alt="Screenshot 2026-01-27 151113" src="https://github.com/user-attachments/assets/01bc5559-9b0d-454e-84d0-b4b2e212e7c7" />
<img width="1390" height="897" alt="Screenshot 2026-01-27 151124" src="https://github.com/user-attachments/assets/14e9a12f-2221-4488-ae18-1a95e00b4a52" />


## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is part of the FOSSEE initiative.

## 👥 Authors

Developed as part of the Chemical Equipment Parameter Visualizer project.

## 🔗 Links

- [Project Plan](plan.md)
- [Development Status](WEB_APP_STATUS.md)
- [React Setup Guide](REACT_SETUP.md)

## 🙏 Acknowledgments

- Django REST Framework
- React and Vite teams
- PyQt5 developers
- Chart.js and matplotlib communities
- Tailwind CSS team


**For detailed setup instructions, see individual README files in each directory.**
