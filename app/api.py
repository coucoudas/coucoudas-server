from fastapi import FastAPI

app = FastAPI(docs_url='/api/docs', redoc_url='/api/redoc')

# root page
@app.get("/")
def hello_world():
    return { "status": 200, "message": "hello" }