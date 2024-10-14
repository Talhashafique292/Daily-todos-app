from sqlmodel import SQLModel,create_engine, Session
from todo_app import setting




# Connection string for engine
connection_string : str = str(setting.DATABASE_URL).replace("postgresql","postgresql+psycopg") 

# Engine:connection to db and is one for whole application
engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

# create tables
def create_tables():
    SQLModel.metadata.create_all(engine)

# session function 
def get_session():
    with Session(engine) as session:
        yield session    