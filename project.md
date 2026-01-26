# Chemical Equipment Parameter Visualizer

## Project Overview

Chemical Equipment Parameter Visualizer is a **hybrid application** that runs as both a **Web Application** and a **Desktop Application**, powered by a **single common backend**. The system allows users to upload CSV files containing chemical equipment parameters, analyze the data, and visualize insights using charts and tables.

The goal of this project is to demonstrate real-world skills in **backend API design**, **data analytics**, and **multi-platform frontend development**.

---

## Core Problem Statement

Chemical plants and labs often collect equipment parameters in CSV format, but lack simple tools to:

* Quickly analyze the data
* Visualize trends
* Generate summaries and reports
* Access the same system across platforms

This project solves that by providing a unified backend with two different client interfaces.

---

## System Architecture

```
React Web App  ─┐
                │
PyQt5 Desktop ──┼──> Django REST API ──> SQLite Database
                │
                └──> Pandas Analytics Engine
```

* One backend
* Two independent frontends
* Shared APIs

---

## Technology Stack

### Backend

**Django**
Used as the core backend framework to manage requests, authentication, and database operations.

**Django REST Framework (DRF)**
Provides RESTful APIs consumed by both Web and Desktop applications.

**Pandas**
Used for CSV parsing, data cleaning, aggregation, and statistical analysis.

**SQLite**
Lightweight database used to store metadata and summaries of the last five uploaded datasets.

---

### Web Frontend

**React.js**
Used to build a modern, responsive web interface.

**Chart.js**
Used for rendering interactive charts such as bar charts and pie charts for data visualization.

**Axios / Fetch API**
Used to communicate with the Django backend APIs.

---

### Desktop Frontend

**PyQt5**
Used to build a native desktop application with forms, tables, and buttons.

**Matplotlib**
Used to render charts similar to the web version for UI consistency.

---

## Key Features

### CSV Upload

* Upload CSV files from both Web and Desktop applications
* Files are processed only by the backend

### Data Analytics

* Total equipment count
* Average flowrate, pressure, and temperature
* Equipment type distribution

### Data Visualization

* Tables for raw data preview
* Charts for summarized analytics

### History Management

* Stores only the **last 5 uploaded datasets**
* Automatically removes older records

### Authentication

* Basic user authentication
* Protects all analytics APIs

### PDF Report Generation

* Generates downloadable PDF reports
* Includes summaries and charts

---

## Expected Outcomes

* Clean API-driven architecture
* Platform-independent data analytics
* Consistent visualization across Web and Desktop
* Demonstration of production-ready development practices

---

## Deliverables

* GitHub repository (backend + both frontends)
* README with setup instructions
* Demo video (2–3 minutes)
* Optional deployed web version

---

## Conclusion

This project demonstrates the ability to design and implement a full-stack, cross-platform analytics system using industry-relevant tools and best practices. It reflects real-world software engineering workflows and architectural thinking.
