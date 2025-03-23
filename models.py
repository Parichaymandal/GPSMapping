import sqlalchemy as alchemy
from sqlalchemy import Column, BigInteger, Sequence, ForeignKey, ARRAY
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from geoalchemy2 import Geometry


import datetime as datetime
import database as db


class Recording(db.Base):
    __tablename__ = "recordings"
    #id=
    recording_id = Column(BigInteger, Sequence('recording_id_seq'), primary_key=True)
    gps_index = Column(BigInteger, nullable=False)
    geometry = Column(Geometry('POINT', srid=4326, spatial_index=True))

class RoadEdge(db.Base):
    __tablename__ = 'road_edges'
    
    edge_id = Column(BigInteger, Sequence('edge_id_seq'), primary_key=True)
    start_node = Column(BigInteger, nullable=False)
    end_node = Column(BigInteger, nullable=False)
    start_geometry = Column(Geometry('POINT', srid=4326))
    end_geometry = Column(Geometry('POINT', srid=4326))
    geometry = Column(Geometry('LINESTRING', srid=4326))

class GPSEdgeMapping(db.Base):
    __tablename__ = 'gps_edge_mapping'
    
    edge_id = Column(BigInteger, nullable=False)
    recording_id = Column(BigInteger, nullable=False)
    gps_index_array = Column(BigInteger, nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('edge_id', 'recording_id'),)

