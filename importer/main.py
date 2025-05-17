from fastapi import FastAPI
from api.routes import router
from dotenv import load_dotenv

load_dotenv()
print("RUUUUN importer")
app = FastAPI(title="importer")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)