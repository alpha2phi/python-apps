import sys
import logging
from fastapi import FastAPI
import uvicorn

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI(
    title="Grabber App",
    description="""Visit port 8088/docs for the Swagger documentation.""",
    version="0.0.1",
)


@app.get("/")
def home():
    return {"message": "Cartoon Camera"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
