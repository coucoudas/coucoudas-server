from fastapi import FastAPI

app = FastAPI(docs_url='/api/docs', redoc_url='/api/redoc')

@app.get("/")
def hello_world():
    return {"Hello": "World"}