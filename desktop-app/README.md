# Chemical Equipment Parameter Visualizer - Desktop Application

PyQt5 desktop application for analyzing and visualizing chemical equipment parameters.

## Features

- 🔐 **Authentication** - Login/Register with password validation
- 📊 **Data Visualization** - Bar, doughnut, and line charts using matplotlib
- 📁 **CSV Upload** - Import equipment data from CSV files
- 📈 **Statistics** - Summary stats for flowrate, pressure, temperature
- 📜 **History** - View recent uploads in sidebar
- 📄 **PDF Reports** - Generate and download PDF reports
- 🎨 **Dark Theme** - Consistent design matching web app

## Installation

### Prerequisites

- Python 3.8 or higher
- Backend server running (see backend folder)

### Setup

1. **Navigate to the desktop-app directory:**
   ```bash
   cd desktop-app
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Start the Backend Server

Before running the desktop app, ensure the Django backend is running:

```bash
cd backend
python manage.py runserver
```

The backend should be accessible at `http://127.0.0.1:8000`

### Run the Desktop Application

```bash
python main.py
```

### Using the Application

1. **Login/Register:**
   - Create a new account or login with existing credentials
   - Password must be at least 8 characters with uppercase, lowercase, and number

2. **Upload CSV:**
   - Click "Choose File" to select a CSV file
   - CSV should have columns: `Equipment Name`, `Type`, `Flowrate`, `Pressure`, `Temperature`
   - Click "Upload and Analyze" to process the data

3. **View Results:**
   - Summary statistics displayed in cards
   - Three charts show parameter averages, equipment distribution, and trends
   - Data table shows all equipment details

4. **Generate PDF:**
   - Click "Download PDF" to generate a report
   - Select save location for the PDF file

5. **View History:**
   - Right sidebar shows recent uploads
   - Click refresh button to update the list

## CSV Format

Your CSV file should follow this format:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,10.2,45.3
Reactor-001,Reactor,200.0,15.5,80.0
Heat Exchanger-001,Heat Exchanger,180.0,12.0,65.5
```

## Configuration

To change the backend URL, edit `api_client.py`:

```python
class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        # Change base_url here
```

## Dependencies

- **PyQt5** (5.15.9+) - GUI framework
- **matplotlib** (3.8.0+) - Chart generation
- **requests** (2.31.0+) - HTTP client
- **pandas** (2.1.0+) - Data processing

## Troubleshooting

### Connection Error

If you see "Connection refused" error:
- Ensure the backend server is running
- Check the backend URL in `api_client.py`

### Import Errors

If you encounter import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Display Issues

If the UI looks blurry on high-DPI displays:
- The app should automatically enable high-DPI scaling
- If issues persist, try setting environment variable:
  ```bash
  set QT_SCALE_FACTOR=1.5
  ```

## Architecture

```
desktop-app/
├── main.py             # Application entry point
├── auth_window.py      # Login/Register dialog
├── dashboard.py        # Main dashboard window
├── api_client.py       # Backend API communication
├── styles.py           # Dark theme stylesheet
└── requirements.txt    # Python dependencies
```

## Color Scheme

Matches the web application:
- **Background:** #000000 (black)
- **Cards:** #18181b (zinc-900)
- **Inputs:** #27272a (zinc-800)
- **Borders:** #3f3f46 (zinc-700)
- **Text:** #ffffff (white)
- **Secondary Text:** #a1a1aa (zinc-400)

## License

See the main project README for license information.
