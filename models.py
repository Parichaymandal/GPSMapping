import sqlalchemy as alchemy
from sqlalchemy import Column, BigInteger, Sequence, ForeignKey, ARRAY, PrimaryKeyConstraint, TIMESTAMP
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry


import datetime as datetime
import database as db


class Recording(db.Base):
    __tablename__ = "recordings"
    id = Column(BigInteger, Sequence('recording_id'), primary_key=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    gps_tracks = relationship("GPSTrack", back_populates="recording")

class GPSTrack(db.Base):
    __tablename__ = "gps_tracks" 
    id = Column(BigInteger,  Sequence('track_id'), primary_key=True)
    recording_id = Column(BigInteger, ForeignKey("recordings.id"), nullable=False)
    gps_index = Column(BigInteger, nullable=False)
    geometry = Column(Geometry("POINT", srid=4326), nullable=False)
    recording = relationship("Recording", back_populates="gps_tracks")


class RoadEdge(db.Base):
    __tablename__ = 'road_edges' 
    id = Column(BigInteger, Sequence('edge_id'), primary_key=True)
    geometry = Column(Geometry('LINESTRING', srid=4326))

class GPSEdgeMapping(db.Base):
    __tablename__ = 'gps_edge_mapping'
    edge_id = Column(BigInteger, ForeignKey('road_edges.id'), nullable=False)
    recording_id = Column(BigInteger, ForeignKey('recordings.id'), nullable=False)
    gps_index_array = Column(ARRAY(BigInteger), nullable=False)
    __table_args__ = (PrimaryKeyConstraint('edge_id', 'recording_id'),)

