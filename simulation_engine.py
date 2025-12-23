import logging
import geopandas as gpd
import json
from typing import Union, Dict
import os
from groq import Groq
from dotenv import load_dotenv
import pandas as pd

# We now import the single, unified report model from our final models.py file
from models import SimulationReport

logger = logging.getLogger("urban-planning-api")
load_dotenv()

# --- The Main "Director" Function (Simple & Synchronous) ---
def run_advanced_simulation(intersecting_wards_data: gpd.GeoDataFrame, infra_type: str) -> dict:
    """
    This is the main director function. It runs synchronously and orchestrates 
    the entire hybrid AI workflow from start to finish.
    """
    infra_type_lower = infra_type.lower()
    if intersecting_wards_data.empty:
        return {"status": "no_impact", "message": "The new infrastructure is outside of any known ward."}

    # 1. Run the Numeric Engine (PyTorch placeholder) to get hard numbers
    numeric_predictions = run_pytorch_predictions(intersecting_wards_data, infra_type_lower)
    
    # 2. Prepare the rich context for the Narrative Engine (LLM)
    context = _prepare_llm_context(intersecting_wards_data, numeric_predictions, infra_type_lower)
    
    # 3. Craft the powerful prompt for the LLM
    prompt = _create_generative_prompt(context, infra_type_lower)
    
    # 4. Get the final, generative report from the live LLM
    llm_response = _query_llm_api(prompt)
    
    # Add the specific infrastructure_type to the final report for the frontend
    if "status" in llm_response and llm_response["status"] == "success":
        llm_response["infrastructure_type"] = infra_type.replace("_", " ").title()

    return llm_response


# --- FINAL, CORRECTED "AI SUGGESTION" FUNCTION ---
def get_ai_suggestion(all_wards_gdf: gpd.GeoDataFrame, infra_type: str) -> Dict:
    """
    Uses proxy data to find the most suitable ward for a new infrastructure project.
    This version includes robust data cleaning to prevent errors.
    """
    logger.info(f"Generating AI suggestion for: {infra_type}")
    
    gdf = all_wards_gdf.copy()
    
    try:
        # --- NEW: Bulletproof Data Cleaning ---
        # We ensure all columns we need are clean and numeric before using them.
        gdf['totaldata_Total Ward Population'] = pd.to_numeric(gdf['totaldata_Total Ward Population'], errors='coerce').fillna(0)
        gdf['totaldata_Estimated Ward GDP (₹ Crore)'] = pd.to_numeric(gdf['totaldata_Estimated Ward GDP (₹ Crore)'], errors='coerce').fillna(0)
        gdf['green_space_numeric'] = pd.to_numeric(gdf['totaldata_% Green Space'].str.rstrip('%'), errors='coerce').fillna(100) # Fill missing green space with high value
        
        # --- The Core Proxy Logic (Now safe to run) ---
        if infra_type in ["school", "hospital"]:
            target_ward = gdf.loc[gdf['totaldata_Total Ward Population'].idxmax()]
            reason = f"This ward has the highest population density ({int(target_ward['totaldata_Total Ward Population']):,}), indicating a strong need for public services."
            
        elif infra_type == "park":
            target_ward = gdf.loc[gdf['green_space_numeric'].idxmin()]
            reason = f"This ward has the lowest percentage of green space ({target_ward['totaldata_% Green Space']}), making it an ideal candidate for a new park."
            
        elif infra_type == "mall":
            target_ward = gdf.loc[gdf['totaldata_Estimated Ward GDP (₹ Crore)'].idxmax()]
            reason = f"This ward has the highest estimated economy (₹{target_ward['totaldata_Estimated Ward GDP (₹ Crore)']} Crore), making it a prime location for a new commercial center."
            
        else: 
            return {"ward_name": "N/A", "reason": "AI suggestions are not available for this infrastructure type.", "latitude": 17.6868, "longitude": 83.2185}

        centroid = target_ward.geometry.centroid
        
        return {
            "ward_name": target_ward['totaldata_Ward Name'],
            "reason": reason,
            "latitude": centroid.y,
            "longitude": centroid.x
        }
    except Exception as e:
        logger.error(f"Error during suggestion generation: {e}")
        return {"ward_name": "Error", "reason": f"An error occurred while generating the suggestion: {e}", "latitude": 17.6868, "longitude": 83.2185}


# --- Helper Functions (The Two AI Engines) ---

def run_pytorch_predictions(wards_data: gpd.GeoDataFrame, infrastructure_type: str) -> Dict[str, Union[float, str]]:
    """
    *** SUPER OP PYTORCH MODEL PLACEHOLDER ***
    This function now returns a comprehensive dictionary of placeholder predictions
    for every single infrastructure type.
    """
    logger.info(f"Executing Numeric Engine for: {infrastructure_type}")
    
    base_predictions = {
        "predicted_aqi_change": 0.0, "predicted_heat_index_change": 0.0,
        "predicted_urban_vegetation_change_percent": 0.0, "predicted_traffic_density_change_percent": 0.0,
        "predicted_light_vehicle_change_percent": 0.0, "predicted_medium_vehicle_change_percent": 0.0,
        "predicted_heavy_vehicle_change_percent": 0.0, "predicted_total_population_change": 0,
        "predicted_gdp_change_crore": 0.0,
    }

    if infrastructure_type == "road_ground":
        base_predictions.update({"predicted_aqi_change": 15.2, "predicted_traffic_density_change_percent": 55.0, "predicted_medium_vehicle_change_percent": 40.0, "predicted_heavy_vehicle_change_percent": 15.0, "predicted_urban_vegetation_change_percent": -18.0, "predicted_heat_index_change": 1.8})
    elif infrastructure_type in ["road_flyover", "road_tunnel"]:
        base_predictions.update({"predicted_aqi_change": 8.5, "predicted_traffic_density_change_percent": 30.0, "predicted_medium_vehicle_change_percent": 25.0, "predicted_urban_vegetation_change_percent": -5.0, "predicted_heat_index_change": 0.5})
    elif infrastructure_type == "mall":
        base_predictions.update({"predicted_aqi_change": 5.7, "predicted_traffic_density_change_percent": 42.5, "predicted_medium_vehicle_change_percent": 50.0, "predicted_gdp_change_crore": 12.50, "predicted_heat_index_change": 2.5, "predicted_urban_vegetation_change_percent": -5.0})
    elif infrastructure_type == "school":
        base_predictions.update({"predicted_aqi_change": 1.5, "predicted_traffic_density_change_percent": 18.0, "predicted_medium_vehicle_change_percent": 20.0, "predicted_heat_index_change": 0.5, "predicted_total_population_change": 500, "predicted_urban_vegetation_change_percent": -2.0})
    elif infrastructure_type == "hospital":
         base_predictions.update({"predicted_aqi_change": 2.1, "predicted_traffic_density_change_percent": 15.0, "predicted_medium_vehicle_change_percent": 15.0, "predicted_heavy_vehicle_change_percent": 5.0, "predicted_heat_index_change": 0.8, "predicted_urban_vegetation_change_percent": -3.0})
    elif infrastructure_type == "park":
        base_predictions.update({"predicted_aqi_change": -12.0, "predicted_traffic_density_change_percent": -8.0, "predicted_heat_index_change": -2.5, "predicted_urban_vegetation_change_percent": 25.0, "predicted_total_population_change": 50})
    
    return base_predictions


def _prepare_llm_context(wards_data: gpd.GeoDataFrame, numeric_predictions: dict, infra_type: str) -> str:
    """This function prepares the comprehensive data briefing for the LLM."""
    total_pop = int(wards_data['totaldata_Total Ward Population'].sum())
    avg_gdp = wards_data['totaldata_Estimated Ward GDP (₹ Crore)'].mean()
    
    context = f"""
    CONTEXT OF THE AFFECTED URBAN AREA:
    - Geographic Area: Consists of {len(wards_data)} ward(s).
    - Total Population: Approximately {total_pop:,} people.
    - Average Ward Economy: Estimated GDP of ₹{avg_gdp:.2f} Crore per ward.
    """
    if numeric_predictions:
        context += "\n\n    PRELIMINARY AI ANALYSIS (NUMERIC PREDICTION MODEL):"
        for key, value in numeric_predictions.items():
            if value != 0:
                title = key.replace("_", " ").replace("percent", "%").title()
                context += f"\n    - {title}: {value}"
            
    if infra_type == "road_flyover":
        context += "\n\n    ANALYTICAL NOTE: This is a flyover, designed to bypass local traffic."
    elif infra_type == "road_tunnel":
        context += "\n\n    ANALYTICAL NOTE: This is a tunnel, with minimal surface impact."
        
    return context.strip()

def _create_generative_prompt(context: str, infrastructure_type: str) -> str:
    """This function now uses the single, unified SimulationReport schema for all prompts."""
    output_schema = json.dumps(SimulationReport.model_json_schema(), indent=2)
    
    prompt = f"""
    ROLE: You are a world-class urban planning AI assistant named 'UrbanInsight'. Your analysis is sharp, data-driven, and generative.

    CONTEXT: I am analyzing a specific urban area with the following characteristics:
    {context}

    USER ACTION: A new '{infrastructure_type.upper()}' is being proposed for this area.

    YOUR TASK: Based on all the provided context, including the preliminary AI analysis, perform a detailed generative analysis. Your response must be a valid JSON object that strictly adheres to the following JSON schema. For every single 'narrative' field in the schema, you MUST provide a detailed, data-driven analysis in a sentence or two, explaining the reasoning behind the predicted changes. Do not include any text, explanations, or markdown formatting outside of the JSON object itself.

    JSON SCHEMA:
    {output_schema}
    """
    return prompt.strip()


def _query_llm_api(prompt: str) -> dict:
    """This function calls the live Groq LLM API. It is unchanged."""
    API_KEY = os.getenv("GROQ_API_KEY")
    if not API_KEY:
        logger.error("FATAL: GROQ_API_KEY environment variable not found.")
        return {"status": "error", "message": "API key is not configured on the server."}
    try:
        client = Groq(api_key=API_KEY)
        logger.info("--- SENDING REAL QUERY TO GROQ API ---")
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.7
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        logger.error(f"An unexpected error occurred while querying the Groq API: {e}")
        return {"status": "error", "message": f"An error occurred with the Groq API: {e}"}