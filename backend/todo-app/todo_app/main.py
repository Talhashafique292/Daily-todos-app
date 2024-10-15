from fastapi import FastAPI, Depends, HTTPException,status
from todo_app import setting
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Annotated
from contextlib import asynccontextmanager
from todo_app.db import get_session, create_tables
from todo_app.models import Todo, Token, User, Todo_Create, Todo_Update
from todo_app.router import user
from fastapi.security import OAuth2PasswordRequestForm
from todo_app.auth import authenticate_user, create_access_token, EXPIRE_TIME, current_user, validate_refresh_token, create_refresh_token
from datetime import timedelta


# contextmanager will create tables firstly as app starts
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Create Tables")
    create_tables()
    print("Tables Created")
    yield


app: FastAPI = FastAPI(lifespan=lifespan, title="Daily todos app", version='1.0.0')

#including app router 
app.include_router(router=user.user_router)

@app.get('/')
async def root():
    return {"message": "Welcome to Daily TODOs App"}


# login    
@app.post('/token', response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                session:Annotated[Session, Depends(get_session)]):
    user = authenticate_user(form_data.username,form_data.password,session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    expire_time = timedelta(minutes=EXPIRE_TIME)
    access_token = create_access_token({"sub":form_data.username}, expire_time)  

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)

    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)
    

@app.post('/token/refresh')
def refresh_token(old_refresh_token:str,
                    session:Annotated[Session,Depends(get_session)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate":"Bearer"}
    )    
    user = validate_refresh_token(old_refresh_token,
                                    session)
    if not user:
        raise credential_exception   

    expire_time = timedelta(minutes=EXPIRE_TIME)
    access_token = create_access_token({"sub":user.username}, expire_time)   

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)

    return Token(access_token=access_token, token_type='bearer', refresh_token=refresh_token)


@app.post('/todos/', response_model=Todo)
async def create_todo(current_user:Annotated[User,Depends(current_user)], 
                    todo:Todo_Create,
                    session:Annotated[Session, Depends(get_session)]):
    new_todo = Todo(content=todo.content, user_id=current_user.id)

    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

@app.get('/todos/', response_model= list[Todo])
async def get_all(current_user:Annotated[User,Depends(current_user)],
                    session:Annotated[Session,Depends(get_session)]):
    todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all() 
    if todos:
        return todos
    else:
        raise HTTPException (status_code=404, detail="No task found")


@app.get('/todos/{id}', response_model=Todo)
async def get_single_todo(id:int, 
                            current_user:Annotated[User,Depends(current_user)], 
                            session:Annotated[Session,Depends(get_session)]):

    user_todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    matched_todo = next((todo for todo in user_todos if todo.id == id),None)
    if matched_todo:
        return matched_todo
    else:
        raise HTTPException (status_code=404, detail="No task found")

@app.put('/todos/{id}')
async def update_todo(id:int,
                        todo:Todo_Update, 
                        current_user:Annotated[User,Depends(current_user)],
                        session:Annotated[Session,Depends(get_session)]):

    user_todos = session.exec(select(Todo).where(Todo.user_id==current_user.id)).all()                    
    existing_todo = next((todo for todo in user_todos if todo.id==id),None)
    
    if existing_todo:
        existing_todo.content = todo.content
        existing_todo.is_completed = todo.is_completed 
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException (status_code=404, detail="No task found")  

@app.delete('/todos/{id}')
async def delete_todo(id:int, 
                        current_user:Annotated[User,Depends(current_user)],
                        session:Annotated[Session,Depends(get_session)]):

    user_todos = session.exec(select(Todo).where(Todo.user_id==current_user.id)).all()
    todo = next((todo for todo in user_todos if todo.id==id),None)

    if todo:
        session.delete(todo)
        session.commit()
        # session.refresh(todo)
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="no task deleted") 
       
