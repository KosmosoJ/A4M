from fastapi import FastAPI
from routes.categories import router as categories_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories_router, prefix='/api/categories',tags=['categories'])


@app.get("/d")
async def index():
    return {"message": "Hello"}
