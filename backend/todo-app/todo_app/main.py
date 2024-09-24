from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from todo_app import setting


# create model
  # data model is for data validation (pydantic)
  # table model for creating tables in db
class Todo(SQLModel, table = True):
    id : int| None = Field(default=None, primary_key=True)
    content: str = Field(index=True, min_length=3, max_length=54)
    is_completed : bool = Field(default=False)

# Connection string for engine
connection_string : str = str(setting.DATABASE_URL).replace("postgresql","postgresql+psycopg") 

# Engine:connection to db and is one for whole application

engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

# create tables
SQLModel.metadata.create_all(engine)

todo1 : Todo = Todo(content="first task")
todo2 : Todo = Todo(content="second task")

# session: seperate session for each transaction/functionality through engine
session = Session(engine)

# create todos in db
session.add(todo1)
session.add(todo2)
print(f'Before commit {todo1}')
session.commit()
session.refresh(todo1)
print(f'After commit {todo1}')
session.close()

app: FastAPI = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to Daily TODOs App"}


@app.post('/todos/')
async def create_todo():
    ...

@app.get('/todos/')
async def get_all():
    ...

@app.get('/todos/{id}')
async def get_single_todo():
    ...

@app.put('/todos/{id}')
async def update_todo():
    ...

@app.delete('/todos/{id}')
async def delete_todo():
    ...        

