import geopandas as gpd
import osmnx as ox
from models import GPSEdgeMapping, GPSTrack, Recording, RoadEdge
import database as db
import io
from geoalchemy2.functions import ST_DWithin, ST_Distance, ST_Extent
from geoalchemy2.shape import to_shape
from logging_config import logger

session = db.session()

async def save_geojson_to_gps_recording(geojson_file):
    session = db.session()
    logger.info("Reading GeoJSON file...")
    contents = geojson_file.file.read()  
    geojson_io = io.BytesIO(contents)
    gdf = gpd.read_file(geojson_io)    
    gdf = gdf.set_crs('EPSG:4326', allow_override=True)  
    new_recording = Recording(timestamp="NOW()")
    session.add(new_recording)
    session.flush() 
    recording_id = new_recording.id
    for index, row in gdf.iterrows():
        gps_record = GPSTrack(
            recording_id = recording_id,
            gps_index=row['gps_index'],
            geometry=row['geometry'].wkt
        )
        session.add(gps_record)
    session.commit()
    logger.info("GeoJSON data successfully uploaded.")
    return recording_id

def extract_and_save_road_network():
    session = db.session()
    try:
        #engine = create_engine(db_url)   
        bbox = session.query(ST_Extent(GPSTrack.geometry)).scalar()
        if not bbox or not bbox[0]:
            raise ValueError("No bounding box found for GPS data.")

        bbox = bbox.replace("BOX(", "").replace(")", "").split(",")
        minx, miny = map(float, bbox[0].split())
        maxx, maxy = map(float, bbox[1].split())
        G = ox.graph_from_bbox(bbox=( minx,miny, maxx, maxy), network_type='all') #(left, bottom, right, top)
        gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges =  True, fill_edge_geometry=True)#.to_crs(crs = 23030)
        for _, row in gdf_edges.iterrows():
            edge = RoadEdge(geometry=row["geometry"].wkt)
            session.add(edge)
        session.commit()

        logger.info("Road network successfully saved to database.")
        return "Road network successfully saved to database."

    except Exception as e:
         logger.info("Error " + str(e))
         return "Error " + str(e)


def map_match_gps_to_edge(recording_id, gps_index):
    gps_point = session.query(GPSTrack.geometry).filter_by(
        recording_id=recording_id, gps_index=gps_index
    ).scalar()
    if gps_point is None:
        return None
    closest_edge = session.query(RoadEdge.id).filter(
        ST_DWithin(RoadEdge.geometry, gps_point, 50)
    ).order_by(ST_Distance(RoadEdge.geometry, gps_point)).first()
    return closest_edge.id if closest_edge else None

def save_map_matched_data(recording_id):
    session = db.session()
    gps_indices = session.query(GPSTrack.gps_index, GPSTrack.geometry).filter_by(
        recording_id=recording_id
    ).all()
    edge_dict = {}
    for gps_index, gps_geometry in gps_indices:
        edge_id = map_match_gps_to_edge(recording_id, gps_index)
        if edge_id is None:
            continue
        if edge_id not in edge_dict:
            edge_dict[edge_id] = []
        edge_dict[edge_id].append(gps_index)
    for edge_id, gps_indices in edge_dict.items():
        gps_edge_mapping = GPSEdgeMapping(
            edge_id=edge_id,
            recording_id=recording_id,
            gps_index_array=gps_indices
        )
        session.add(gps_edge_mapping)
    session.commit()
    return None

def get_gps_track_section():
    session = db.session()
    sections = session.query(GPSEdgeMapping).all()  
    features = []
    for section in sections:
        gps_points = session.query(GPSTrack).filter(
            GPSTrack.recording_id == section.recording_id,
            GPSTrack.gps_index.in_(section.gps_index_array)
        ).order_by(GPSTrack.gps_index).all()    
        if len(gps_points) < 2:
            continue
        coordinates = [to_shape(track.geometry).coords[0] for track in gps_points]
        feature = {
            "type": "Feature",
            "properties": {"edge_id": section.edge_id, "recording_id": section.recording_id},
            "geometry": {"type": "LineString", "coordinates": coordinates}
        }
        features.append(feature)    
    return {"type": "FeatureCollection", "features": features}


