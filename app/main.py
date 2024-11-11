from fastapi import FastAPI
from routes.categories import router as categories_router
from routes.anime import router as anime_router
from routes.tokens import router as tokens_router
from routes.parse import router as parser_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = ["http://localhost:3000", '*']


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories_router, prefix='/api/categories',tags=['categories'])
app.include_router(anime_router, prefix='/api/anime', tags=['animes'])
app.include_router(tokens_router, prefix='/api/tokens', tags=['tokens'])
app.include_router(parser_router, prefix='/api/parser', tags=['parser'])

async def lifespan(app:FastAPI):
    ...


@app.get("/d")
async def index():
    return {"message": "Hello"}
