# urban-planner-ai-tool
ML backend for an urban planning tool using Vizag geospatial data.
# Urban Planner AI Tool

## Overview
This project is a Minimum Viable Product (MVP) built to explore how AI and data
can be used in urban planning. The idea is to simulate the impact of infrastructure
changes (such as road construction) on different urban metrics **before** actual
planning or construction takes place.

The system uses real-world geospatial and demographic data from Visakhapatnam
(Vizag), mapped at the ward level, and provides predictive insights through a
backend API.

---

## Problem Statement
Urban planning decisions often require analyzing multiple factors such as
population, traffic, environmental conditions, and land usage. This project
attempts to simulate such decisions by allowing users to analyze potential
changes at the **ward level**, helping to understand trends before implementation.

---

## Data Collection and Processing
- Collected Vizag ward-level data from third-party public sources
- Used additional open datasets (including NASA free data sources)
- Data includes:
  - Ward boundaries and names
  - Population (male/female distribution)
  - Traffic data based on vehicle type and weight
  - Air Quality Index (AQI)
  - Urban vegetation percentage
  - Heat index and environmental metrics

### Geospatial Mapping
- Original data was available in CSV format
- Converted a PDF-based ward map into a GeoJSON file
- Linked CSV data with GeoJSON boundaries for all **96 wards**
- Used the final GeoJSON file as input for model training

---

## Model and Prediction Logic
- Trained an ML model using the processed GeoJSON-based dataset
- The model predicts **relative changes** in urban metrics when a specific type
  of infrastructure (e.g., a road) is introduced in a ward
- Example predictions include:
  - Change in traffic flow
  - Impact on population growth trends
  - Environmental changes at the ward level

> This is a simulation-based learning project and not intended for real-world
policy decisions.

---

## Backend Architecture
- Built using **FastAPI**
- Exposes APIs for simulation and prediction
- Handles data preprocessing, model inference, and response formatting

### Tech Stack
- Python
- FastAPI
- Uvicorn
- Pandas, GeoPandas
- PyTorch
- Scikit-learn
- Joblib
- Shapely
- Pydantic
- python-dotenv
- Groq API (LLM support)

---

## Deployment
- Backend deployed using **Hugging Face Spaces**
- Used Docker for environment consistency and deployment
- Hugging Face was chosen due to ease of use and free deployment support

---

## Frontend
- Simple web-based frontend hosted on GitHub
- Sends user input to the backend API
- Displays predicted outputs from the model

---

## Limitations
- Predictions operate at the **ward level**, not at a fine-grained geographic level
- Simulation accuracy is limited and intended for exploratory purposes only
- Model predictions are approximate and may not reflect real-world outcomes
- Uses third-party APIs (Groq, LLaMA-based models) with free-tier constraints

---

## Learning Outcomes
- Learned how to work with real-world geospatial datasets (GeoJSON)
- Gained experience in data preprocessing and ML model training
- Built and deployed an ML backend using FastAPI and Docker
- Understood backend–frontend integration for end-to-end systems
- Explored AI-assisted simulations for urban planning use cases

