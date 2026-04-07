from pydantic import BaseModel
from typing import List, Literal

# 1. What the AI sees (The Dashboard)
class Observation(BaseModel):
    service_health: float       # 0.0 (dead) to 1.0 (perfect)
    cpu_usage: float            # Percentage, e.g., 95.5
    recent_logs: List[str]      # Last few server logs
    status: str                 # "HEALTHY", "DEGRADED", or "CRITICAL"

# 2. What the AI can do (The Controls)
class Action(BaseModel):
    # The AI is only allowed to pick one of these specific commands
    command: Literal["RESTART", "SCALE_UP", "ROLLBACK", "WAIT"]
    
# 3. How the AI is scored (The Feedback)
class Reward(BaseModel):
    score: float                # Points awarded for the action
    is_done: bool               # True if the task is completely finished
    message: str                # Explanation of why they got those points