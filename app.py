from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from services import extract_and_save_road_network, get_gps_track_section, save_geojson_to_gps_recording, save_map_matched_data
from shapely.geometry import Point
from logging_config import logger
import database as db

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

@app.post("/upload-geojson/")
async def upload_geojson(background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    try:
        recording_id = await save_geojson_to_gps_recording(file)
        logger.info("Road network extraction and GPS-track matching is running on background..")
        background_tasks.add_task(extract_and_save_road_network)
        background_tasks.add_task(save_map_matched_data, recording_id)
        logger.info("GPS track matched succesfully.")
        return "GPS track saved and matching completed."
    except Exception as e:
         logger.info("Error " + str(e))
         return "Error " + str(e)
   
@app.get("/gps-track-sections/")
async def get_gps_track_sections():
    return get_gps_track_section()
