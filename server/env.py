# app/env.py
from .models import Observation, Action, Reward

class CloudOpsEnv:
    def __init__(self):
        self.current_state = self._generate_healthy_state()
        self.task_level = 1 
        self.steps_taken = 0

    def _generate_healthy_state(self) -> Observation:
        """Helper to create a normal, working server state."""
        return Observation(
            service_health=1.0,
            cpu_usage=45.0,
            recent_logs=["INFO: Server running smoothly", "INFO: Traffic normal"],
            status="HEALTHY"
        )

    def reset(self, task_level: int = 1) -> Observation:
        """OpenEnv Spec: Resets the environment to start a new episode."""
        self.task_level = task_level
        self.steps_taken = 0

        # Level 1 (Easy): Deadlock -> Needs RESTART
        if task_level == 1:
            self.current_state = Observation(
                service_health=0.0,
                cpu_usage=0.1,
                recent_logs=["FATAL ERROR: Deadlock detected", "CRITICAL: Service completely unresponsive"],
                status="CRITICAL"
            )
        # Level 2 (Medium): High Traffic -> Needs SCALE_UP
        elif task_level == 2:
            self.current_state = Observation(
                service_health=0.4,
                cpu_usage=99.9,
                recent_logs=["WARN: CPU usage critical", "ERROR: Request timeout, instances overloaded"],
                status="DEGRADED"
            )
        # Level 3 (Hard): Bad Code -> Needs ROLLBACK
        elif task_level == 3:
            self.current_state = Observation(
                service_health=0.2,
                cpu_usage=60.0,
                recent_logs=["ERROR: Failed to connect to DB after v2.1 deployment", "FATAL: Crash loop backoff"],
                status="CRITICAL"
            )
        
        return self.current_state

    def step(self, action: Action) -> tuple[Observation, Reward]:
        """OpenEnv Spec: The AI takes an action, we return the new state and a score."""
        self.steps_taken += 1
        reward_score = 0.0
        is_done = False
        msg = ""

        if self.task_level == 1:
            if action.command == "RESTART":
                self.current_state = self._generate_healthy_state()
                reward_score = 1.0
                is_done = True
                msg = "Success! Service restarted and is healthy."
            else:
                reward_score = -0.5
                msg = f"Wrong action '{action.command}'. The service is deadlocked and needs a restart."

        elif self.task_level == 2:
            if action.command == "SCALE_UP":
                self.current_state = self._generate_healthy_state()
                reward_score = 1.0
                is_done = True
                msg = "Success! Instances scaled up to handle load."
            else:
                reward_score = -0.5
                msg = f"Wrong action '{action.command}'. CPU is at 99%, you need to scale up."

        elif self.task_level == 3:
            if action.command == "ROLLBACK":
                self.current_state = self._generate_healthy_state()
                reward_score = 1.0
                is_done = True
                msg = "Success! Bad deployment rolled back."
            else:
                reward_score = -0.5
                msg = f"Wrong action '{action.command}'. The recent deployment is crashing, you must rollback."

        return self.current_state, Reward(score=reward_score, is_done=is_done, message=msg)

    def state(self) -> Observation:
        """OpenEnv Spec: Returns current state without changing anything."""
        return self.current_state