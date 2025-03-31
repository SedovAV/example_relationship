from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_schemadisplay import create_schema_graph

Base = declarative_base()

user_roles = Table('UserRoles', Base.metadata,
    Column('id',Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('Users.id')),
    Column('role_id', Integer, ForeignKey('Roles.id'))
)

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    roles = relationship("Roles", secondary=user_roles, back_populates="users")

class Roles(Base):
    __tablename__ = 'Roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    users = relationship("Users", secondary=user_roles, back_populates="roles")

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

graph.write_png('ORM_many_to_many.png')
