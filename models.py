from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any


# This defines the structure of the data coming from your GeoJSON file.
class WardProperties(BaseModel):
    wardcode: Optional[str] = Field(None, alias="wardcode")
    totaldata_Ward_Name: Optional[str] = Field(None, alias="totaldata_Ward Name")
    totaldata_Population_Age_1_12: Optional[int] = Field(None, alias="totaldata_#Population (Age 1-12)")
    totaldata_Population_Age_13_17: Optional[int] = Field(None, alias="totaldata_#Population (Age 13-17)")
    totaldata_Population_Age_18_24: Optional[int] = Field(None, alias="totaldata_#Population (Age 18-24)")
    totaldata_Population_Age_25_34: Optional[int] = Field(None, alias="totaldata_#Population (Age 25-34)")
    totaldata_Population_Age_35_44: Optional[int] = Field(None, alias="totaldata_Population (Age 35-44)")
    totaldata_Population_Age_45_59: Optional[int] = Field(None, alias="totaldata_#Population (Age 45-59)")
    totaldata_Population_Age_60_plus: Optional[int] = Field(None, alias="totaldata_#Population (Age 60+)")
    totaldata_Air_Quality_Index_AQI: Optional[int] = Field(None, alias="totaldata_Air Quality Index (AQI)")
    totaldata_Traffic_Density_percent: Optional[str] = Field(None, alias="totaldata_% Traffic Density")
    totaldata_Green_Space_percent: Optional[str] = Field(None, alias="totaldata_% Green Space")
    totaldata_Infrastructure_percent: Optional[str] = Field(None, alias="totaldata_% Infrastructure")
    totaldata_Heatmap_Index_Relative: Optional[str] = Field(None, alias="totaldata_Heatmap Index (Relative)")
    totaldata_Estimated_Ward_GDP_Crore: Optional[float] = Field(None, alias="totaldata_Estimated Ward GDP (₹ Crore)")
    totaldata_Light_Weight_Vehicles_2wheelers_autos: Optional[float] = Field(None, alias="totaldata_Light Weight Vehicles (2-wheelers, autos)")
    totaldata_Medium_Weight_Vehicles_cars_pickups: Optional[int] = Field(None, alias="totaldata_Medium Weight Vehicles (cars, pickups)")
    totaldata_Heavy_Weight_Vehicles_buses_trucks: Optional[int] = Field(None, alias="totaldata_Heavy Weight Vehicles (buses, trucks)")
    totaldata_Total_Ward_Population: Optional[int] = Field(None, alias="totaldata_Total Ward Population")
    totaldata_Estimated_Male_Population: Optional[int] = Field(None, alias="totaldata_Estimated Male Population")
    totaldata_Estimated_Female_Population: Optional[int] = Field(None, alias="totaldata_Estimated Female Population")

class Geometry(BaseModel):
    type: str
    coordinates: list

class WardFeature(BaseModel):
    type: str = "Feature"
    properties: WardProperties
    geometry: Geometry

class WardCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[WardFeature]

#  Pydantic Models for API Requests 
class SimulationRequest(BaseModel):
    infrastructure_type: str
    geometry: Dict[str, Any]

class SuggestionResponse(BaseModel):
    ward_name: str
    reason: str
    latitude: float
    longitude: float


class EnvironmentalImpactReport(BaseModel):
    predicted_aqi_change: Optional[float] = None
    predicted_heat_index_change: Optional[float] = None
    predicted_urban_vegetation_change_percent: Optional[float] = None
    narrative: str 
# Nested model for detailed traffic predictions
class TrafficImpactReport(BaseModel):
    predicted_traffic_density_change_percent: Optional[float] = None
    predicted_light_vehicle_change_percent: Optional[float] = None
    predicted_medium_vehicle_change_percent: Optional[float] = None
    predicted_heavy_vehicle_change_percent: Optional[float] = None
    narrative: str 
    
# Nested model for detailed population predictions
class PopulationImpactReport(BaseModel):
    predicted_total_population_change: Optional[int] = None
    predicted_age_group_most_affected: Optional[str] = None
    narrative: str 

# Nested model for detailed economic predictions
class EconomicImpactReport(BaseModel):
    predicted_gdp_change_crore: Optional[float] = None
    narrative: str 


class SimulationReport(BaseModel):
    status: str = "success"
    infrastructure_type: str
    summary_narrative: str
    environmental_impact: Optional[EnvironmentalImpactReport] = None
    traffic_impact: Optional[TrafficImpactReport] = None
    population_impact: Optional[PopulationImpactReport] = None
    economic_impact: Optional[EconomicImpactReport] = None


SimulationResponse = Union[SimulationReport, dict]

