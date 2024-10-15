from fastapi import FastAPI
from routes.categories import router as categories_router

app = FastAPI()

app.include_router(categories_router)


@app.get("/d")
async def index():
    return {"message": "Hello"}
