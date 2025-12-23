import logging
import geopandas as gpd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shapely.geometry import shape
import json
from typing import Dict, Any

# We import all the necessary models and the two main simulation functions
from models import WardCollection, SimulationRequest, SimulationResponse, SuggestionResponse
from simulation_engine import run_advanced_simulation, get_ai_suggestion

# --- Configuration & App Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("urban-planning-api")

GEOJSON_FILE_PATH = "complete_vizag_data.geojson"

app = FastAPI(
    title="Urban Planning AI Simulator API",
    version="FINAL"
)

# --- THIS IS THE FINAL, CRUCIAL FIX ---
# VIP list for CORS (allow frontend to communicate safely)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # universal pass
    allow_credentials=True,
    allow_methods=["*"],    # allow POST requests
    allow_headers=["*"],    # allow 'Content-Type' header
)

app.state.geodata_gdf = None

# --- Data Loading ---
@app.on_event("startup")
def startup_event():
    """Loads the GeoJSON data into a GeoDataFrame when the server starts."""
    try:
        app.state.geodata_gdf = gpd.read_file(GEOJSON_FILE_PATH)
        app.state.geodata_gdf.set_crs("EPSG:4326", inplace=True)
        logger.info(f"Loaded {len(app.state.geodata_gdf)} wards from GeoJSON.")
    except Exception as e:
        logger.error(f"FATAL: Failed to load GeoJSON on startup: {e}")

# --- API Endpoints ---
@app.get("/api/wards", response_model=WardCollection, tags=["Geospatial Data"])
def get_wards_geojson():
    """Serves the main geospatial data for the map."""
    if app.state.geodata_gdf is None:
        raise HTTPException(status_code=503, detail="GeoJSON data is not available or failed to load.")
    return json.loads(app.state.geodata_gdf.to_json())

@app.post("/api/simulate", response_model=SimulationResponse, tags=["Simulation"])
def simulate_infrastructure_impact(request: SimulationRequest):
    """
    Receives a user's drawing, finds intersecting wards,
    runs the full AI simulation, and returns the final generative report.
    """
    if app.state.geodata_gdf is None:
        raise HTTPException(status_code=503, detail="Map data is not available.")

    try:
        new_infra_shape = shape(request.geometry)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid geometry provided: {e}")

    intersecting_wards = app.state.geodata_gdf[app.state.geodata_gdf.geometry.intersects(new_infra_shape)]
    logger.info(f"Found {len(intersecting_wards)} intersecting wards for simulation.")

    simulation_result = run_advanced_simulation(intersecting_wards, request.infrastructure_type)
    return simulation_result

@app.get("/api/suggest-placement/{infra_type}", response_model=SuggestionResponse, tags=["AI Suggestions"])
def suggest_placement(infra_type: str):
    """
    Scans all ward data to suggest an optimal placement for a new piece of infrastructure
    based on proxy metrics.
    """
    if app.state.geodata_gdf is None:
        raise HTTPException(status_code=503, detail="Map data is not available.")

    suggestion = get_ai_suggestion(app.state.geodata_gdf, infra_type)
    if suggestion.get("ward_name") == "N/A" or suggestion.get("ward_name") == "Error":
        raise HTTPException(status_code=404, detail=suggestion["reason"])

    return suggestion

@app.get("/", tags=["Health Check"])
def health_check():
    """A simple endpoint to check if the server is running."""
    return {"status": "ok"}

