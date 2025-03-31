from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_schemadisplay import create_schema_graph


Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    role_id = Column(Integer, ForeignKey('Roles.id')) 

class Roles(Base):
    __tablename__ = 'Roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

graph = create_schema_graph(
    metadata=Base.metadata,  
    show_datatypes=True,   
    show_indexes=False,
    rankdir='LR',
    concentrate=True,
    font="Comic Sans MS",
    show_column_keys=True,
    engine=engine
)

graph.write_png('ORM_one_to_many.png')
