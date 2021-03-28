from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}


@app.get("/items/{item_id}")
async def items(item_id: int):
    return {"parameter_passed": item_id}
