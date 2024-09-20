from fastapi import FastAPI

app: FastAPI = FastAPI()

@app.get('/')
async def root():
    return {"message": "Welcome to Daily TODOs App"}


@app.get('/todos/')
async def read_todos():
    return {"content": "dummy todo"}