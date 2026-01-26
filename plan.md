# Project Development Plan

## Objective

To design and implement a hybrid Web + Desktop application that visualizes and analyzes chemical equipment data using a shared backend API.

---

## Phase 1: Project Setup

### Backend Setup

* Create Django project and application
* Configure Django REST Framework
* Setup SQLite database
* Configure media handling for CSV uploads

### Frontend Setup

* Initialize React application
* Setup PyQt5 desktop application structure
* Establish API base configuration for both clients

---

## Phase 2: Backend Development

### Step 1: Database Design

* Create model for dataset uploads
* Fields:

  * filename
  * upload timestamp
  * summary values

### Step 2: CSV Upload API

* Accept CSV files via POST request
* Validate CSV format
* Parse using Pandas

### Step 3: Analytics Engine

* Calculate:

  * Total equipment count
  * Average flowrate
  * Average pressure
  * Average temperature
  * Equipment type distribution

### Step 4: History Management

* Store metadata for each upload
* Automatically keep only the last five entries

### Step 5: Authentication

* Enable Django authentication
* Protect APIs using basic authentication or token-based auth

### Step 6: PDF Report Generation

* Generate reports dynamically
* Include summary tables and charts
* Provide download API

---

## Phase 3: Web Frontend Development (React)

### Features

* Login page
* CSV upload interface
* Dashboard with:

  * Data table
  * Summary cards
  * Charts
* History view

### Implementation Steps

* Build reusable components
* Integrate Chart.js for visualization
* Connect backend APIs using Axios

---

## Phase 4: Desktop Application Development (PyQt5)

### Features

* Login window
* File upload using file dialog
* Table display using QTableWidget
* Charts rendered using Matplotlib
* History selection

### Implementation Steps

* Design UI layout
* Implement API calls using requests library
* Embed Matplotlib charts into PyQt5 widgets

---

## Phase 5: Integration & Testing

* Verify both clients consume same APIs
* Validate CSV uploads from both platforms
* Ensure analytics consistency
* Test authentication flow
* Confirm history limit enforcement

---

## Phase 6: Documentation & Submission

### Documentation

* README with setup instructions
* API documentation
* Project and plan markdown files

### Demo

* Record 2–3 minute walkthrough video
* Demonstrate both Web and Desktop applications

---

## Timeline (Suggested)

| Day | Task                    |
| --- | ----------------------- |
| 1   | Backend setup & models  |
| 2   | CSV upload & analytics  |
| 3   | Web frontend            |
| 4   | Desktop frontend        |
| 5   | PDF + Auth              |
| 6   | Testing & documentation |

---

## Final Notes

This plan prioritizes backend correctness first, followed by frontend consistency. A single well-designed API is the backbone of the project and ensures maintainability and scalability.
