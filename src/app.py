from fastapi import FastAPI, Depends
import uvicorn
# from config.databaseConnect import get_database 
from controller import ChatController, rawDataController
app = FastAPI()

app.include_router(ChatController.router)
app.include_router(rawDataController.router)
@app.get("/")
async def root():
    return {"message": "Hello"}

if __name__ == "__main__":
    # get_database
    # uvicorn app:app --reload

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)