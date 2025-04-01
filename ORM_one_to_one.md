## Пример построения ER-диаграммы на примере связи сущностей 1:1
#### Импорт необходимых библиотек:
```cmd
python3 -m pip install sqlalchemy sqlalchemy_schemadisplay graphviz
```


```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_schemadisplay import create_schema_graph


Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    role_id = Column(Integer, ForeignKey('Roles.id', ondelete='CASCADE'), unique=True) 
    role = relationship("Roles", back_populates="user")

class Roles(Base):
    __tablename__ = 'Roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    role = relationship("Users", uselist=False, back_populates="role")


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

graph.write_png('img/ORM_test_1_1.png')
```

#### Результат:
<img src="ORM_test_1_1.png" height="400">
