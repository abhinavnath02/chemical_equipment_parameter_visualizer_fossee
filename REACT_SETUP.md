# Chemical Equipment Parameter Visualizer - React Frontend

## Setup Complete! ✅

### What's Running:

1. **Backend (Django)**: `http://127.0.0.1:8000/`
2. **Frontend (React)**: `http://localhost:5173/`

### Features Implemented:

- **CSV File Upload**: Upload chemical equipment data in CSV format
- **Real-time Analysis**: View statistics including:
  - Total equipment count
  - Average flowrate
  - Average pressure
  - Average temperature
- **Upload History**: Track the last 5 uploaded files
- **Responsive Design**: Built with Tailwind CSS v4

### Tech Stack:

- **React 18** with TypeScript
- **Vite** for fast development
- **Tailwind CSS v4** (using Vite plugin, no PostCSS)
- **Django REST API** backend

### How to Use:

1. Make sure both servers are running:
   - Backend: `cd backend && python manage.py runserver`
   - Frontend: `cd web-frontend && npm run dev`

2. Open `http://localhost:5173/` in your browser

3. Upload a CSV file with this format:
   ```csv
   Equipment Name,Type,Flowrate,Pressure,Temperature
   Pump A,Pump,100,10,80
   Reactor B,Reactor,150,20,120
   ```

4. View the analysis results and upload history

### Sample Data:

A sample CSV file is available at the root: `sample_data.csv`

### Development Commands:

```powershell
# Start frontend dev server
cd web-frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### API Endpoints:

- **POST** `/api/upload/` - Upload CSV file
- **GET** `/api/history/` - Get upload history

### Next Steps (Optional):

- Add data visualization charts (Chart.js, Recharts)
- Add filtering and sorting for history
- Add export functionality
- Add user authentication
- Improve error handling and validation
