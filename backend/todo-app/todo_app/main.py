from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine
from todo_app import setting


# create model
  # data model is for data validation (pydantic)
  # table model for creating tables in db
class Todo(SQLModel, table = True):
    id : int| None = Field(default=None, primary_key=True)
    content: str = Field(index=True, min_length=3, max_length=54)
    is_completed : bool = Field(default=False)

# Connection string for engine
connection_string = ""    

# Engine:connection to db
engine = create_engine(connection_string)


app: FastAPI = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to Daily TODOs App"}


@app.get('/todos/')
async def read_todos():
    return {"content": "dummy todo"}