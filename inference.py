import os
import json
import requests
from openai import OpenAI

# Hackathon required environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")
API_KEY = os.getenv("HF_TOKEN", "dummy-key-for-local-testing")

# URL where your Docker container is running
ENV_URL = "http://localhost:7860"

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward} done={done} error={error}", flush=True)

def log_end(success, steps, score, rewards):
    print(f"[END] success={success} steps={steps} score={score} rewards={rewards}", flush=True)

def main():
    # Initialize the LLM Client
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    
    # We will test Level 1 (The Deadlock)
    task_level = 1
    max_steps = 3
    
    log_start(task=f"level-{task_level}", env="CloudOps-Triage", model=MODEL_NAME)
    
    # 1. Reset Environment to start the game
    reset_resp = requests.post(f"{ENV_URL}/reset?task_level={task_level}")
    obs = reset_resp.json()
    
    history = []
    rewards = []
    steps_taken = 0
    success = False
    
    for step in range(1, max_steps + 1):
        steps_taken = step
        
        # 2. Ask the LLM what to do based on the server logs
        prompt = f"""
        You are an AI CloudOps Engineer. Your job is to fix the server.
        Current Server State: {json.dumps(obs)}
        
        Based on the logs, you must choose exactly ONE of these commands: "RESTART", "SCALE_UP", "ROLLBACK", "WAIT".
        Reply ONLY with the command string. Nothing else.
        """
        
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            # Clean up the AI's answer
            action_cmd = response.choices[0].message.content.strip().replace('"', '')
        except Exception as e:
            action_cmd = "WAIT"
            error_msg = str(e)
            
        # 3. Take the Step in the Environment
        step_resp = requests.post(f"{ENV_URL}/step", json={"command": action_cmd})
        step_data = step_resp.json()
        
        obs = step_data["observation"]
        reward = step_data["reward"]
        done = step_data["done"]
        
        rewards.append(reward)
        history.append(f"Step {step}: Commanded {action_cmd} -> Reward: {reward}")
        
        log_step(step=step, action=action_cmd, reward=reward, done=done, error=None)
        
        if done:
            break
            
    score = sum(rewards)
    success = score > 0
    log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    main()