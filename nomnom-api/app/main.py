from fastapi import FastAPI

from app.routers import auth, dish, image, user_dish_interaction

app = FastAPI(title="Nomnom API", version="0.1.0")

app.include_router(auth.router)
app.include_router(dish.router)
app.include_router(image.router)
app.include_router(user_dish_interaction.router)

@app.get("/health")
async def health():
    return {"status": "ok"}