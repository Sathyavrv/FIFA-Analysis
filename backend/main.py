from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from player_similarity_model import PlayerSimilarityModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from the Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the model
model = PlayerSimilarityModel("../data/raw/player_raw_data.csv")
model.load_and_preprocess_data()
model.create_preprocessing_pipeline()
model.fit_transform_data()
model.fit_knn_model(5)

class PlayerRequest(BaseModel):
    playerName: str

@app.post("/api/similar-players")
async def get_similar_players(player_request: PlayerRequest):
    try:
        similar_players = model.find_similar_players(player_request.playerName)
        return similar_players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

