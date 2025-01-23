from fastapi import FastAPI, Depends
import uvicorn
from controller import ChatController
app = FastAPI()

app.include_router(ChatController.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
    
if __name__ == "__main__":
    # get_database
    # uvicorn app:app --reload

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)