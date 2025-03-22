import sqlalchemy as alchemy
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DB_URL = 'postgresql://user:password@localhost:5432/roadnet_db'
engine = alchemy.create_engine(DB_URL, connect_args={"check_same_thread":False})

session = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()