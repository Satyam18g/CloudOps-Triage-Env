# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .models import Observation, Action, Reward
from .env import CloudOpsEnv

app = FastAPI(title="CloudOps Triage Environment")
game_env = CloudOpsEnv()

# --- NEW REDIRECT ROUTE ---
@app.get("/", include_in_schema=False)
async def home():
    """Automatically redirect human visitors to the documentation page."""
    return RedirectResponse(url="/docs")
# --------------------------

@app.post("/reset", response_model=Observation)
async def reset_env(task_level: int = 1):
    return game_env.reset(task_level=task_level)

@app.post("/step", response_model=dict)
async def take_step(action: Action):
    new_state, reward = game_env.step(action)
    return {
        "observation": new_state.model_dump(),
        "reward": reward.score,
        "done": reward.is_done,
        "info": {"message": reward.message}
    }

@app.get("/state", response_model=Observation)
async def get_state():
    return game_env.state()

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == '__main__':
    main() 