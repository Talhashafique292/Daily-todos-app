from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from todo_app import setting
from typing import Annotated
from contextlib import asynccontextmanager

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
def create_tables():
    SQLModel.metadata.create_all(engine)

# todo1 : Todo = Todo(content="first task")
# todo2 : Todo = Todo(content="second task")

# session: seperate session for each transaction/functionality through engine
session = Session(engine)

# # create todos in db
# session.add(todo1)
# session.add(todo2)
# print(f'Before commit {todo1}')
# session.commit()
# session.refresh(todo1)
# print(f'After commit {todo1}')
# session.close()

# a better way is to make function of session
def get_session():
    with Session(engine) as session:
        yield session

# contextmanager will create tables firstly as app starts
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Create Tables")
    create_tables()
    print("Tables Created")
    yield


app: FastAPI = FastAPI(lifespan=lifespan, title="Daily todos app", version='1.0.0')

@app.get('/')
async def root():
    return {"message": "Welcome to Daily TODOs App"}


@app.post('/todos/', response_model=Todo)
async def create_todo(todo:Todo, session:Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get('/todos/', response_model= list[Todo])
async def get_all(session:Annotated[Session,Depends(get_session)]):
    statement = select(Todo)
    todos = session.exec(statement).all() 
    return todos

@app.get('/todos/{id}', response_model=Todo)
async def get_single_todo(id:int, todo:Todo, session:Annotated[Session,Depends(get_session)]):
    todos = session.exec(select(Todo).where(Todo.id == id)).first()
    return todos

@app.put('/todos/{id}')
async def update_todo(id:int,todo:Todo, session:Annotated[Session,Depends(get_session)]):
    existing_todo = session.exec(select(Todo).where(Todo.id==id)).first()
    if existing_todo:
        existing_todo.content = Todo.content
        existing_todo.is_completed = Todo.is_completed 
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException (status_code=404, detail="No task found")  

@app.delete('/todos/{id}')
async def delete_todo(id:int, session:Annotated[Session,Depends(get_session)]):
    todo = session.exec(select(Todo).where(Todo.id==id)).first()
    session.delete(todo)
    session.commit()
    session.refresh(todo)
    return todo