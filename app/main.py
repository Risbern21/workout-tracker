from fastapi import FastAPI

from app.api.v1 import auth, excercises, users, workouts

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.include_router(excercises.router, prefix="/api/v1")
app.include_router(workouts.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "root endpoint works"}
