from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from HolidayAgent.agents.planner import HolidayPlannerAgent
from HolidayAgent.agents.researcher import HolidayResearcherAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from typing_extensions import Literal
from pydantic import Field


app = FastAPI(title="Holiday Trip Planner")

class TripRequest(BaseModel):
    destination: str
    days: int
    source: str
    people: int
    budget: int
    

@app.get("/", response_class=HTMLResponse)
async def home():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Holiday Trip Planner</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        h1 { color: #667eea; text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #333; font-weight: bold; }
        input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
        input:focus { outline: none; border-color: #667eea; }
        button { width: 100%; padding: 15px; background: #667eea; color: white; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; font-weight: bold; }
        button:hover { background: #5568d3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; display: none; line-height: 1.8; white-space: pre-wrap; }
        .loading { text-align: center; color: #667eea; font-size: 18px; display: none; }
        .error { color: #dc3545; background: #f8d7da; padding: 15px; border-radius: 8px; margin-top: 20px; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Holiday Trip Planner</h1>
        <form id="tripForm">
            <div class="form-group">
                <label>Destination</label>
                <input type="text" id="destination" placeholder="e.g., Goa, Paris, Bali" required>
            </div>
            <div class="form-group">
                <label>Number of Days</label>
                <input type="number" id="days" min="1" max="30" placeholder="e.g., 3" required>
            </div>
            <div class="form-group">
                <label>Source</label>
                <input type="text" id="source" placeholder="e.g., Chennai, Bangalore" required>
            </div>
            <div class="form-group">
                <label>Number of People</label>
                <input type="number" id="people" min="1" placeholder="e.g., 2" required>
            </div>
            <div class="form-group">
                <label>Budget (INR)</label>
                <input type="number" id="budget" min="1000" placeholder="e.g., 50000" required>
            </div>
            <button type="submit">Plan My Trip</button>
        </form>
        <div class="loading" id="loading">Planning your trip... This may take a minute</div>
        <div class="error" id="error"></div>
        <div class="result" id="result"></div>
    </div>

    <script>
        document.getElementById('tripForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const destination = document.getElementById('destination').value;
            const days = parseInt(document.getElementById('days').value);
            const source = document.getElementById('source').value;
            const people = parseInt(document.getElementById('people').value);
            const budget = parseInt(document.getElementById('budget').value);
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            const button = document.querySelector('button');
            
            loading.style.display = 'block';
            result.style.display = 'none';
            error.style.display = 'none';
            button.disabled = true;
            
            try {
                const response = await fetch('/plan-trip', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ destination, days, budget, source, people })
                });
                
                const data = await response.json();
                console.log('Received data:', data);
                
                if (response.ok) {
                    const planText = typeof data.plan === 'string' 
                    ? data.plan 
                    : JSON.stringify(data.plan, null, 2);

                    result.textContent = planText;
                    result.style.display = 'block';
                }               else {
                    error.textContent = data.detail || 'Error planning trip';
                    error.style.display = 'block';
                }
            } catch (err) {
                error.textContent = 'Network error. Please try again.';
                error.style.display = 'block';
            } finally {
                loading.style.display = 'none';
                button.disabled = false;
            }
        });
    </script>
</body>
</html>"""
    return HTMLResponse(content=html)

@app.post("/plan-trip")
async def plan_trip(request: TripRequest):
    try:
        planner = HolidayPlannerAgent()
        researcher = HolidayResearcherAgent()
        
        termination = TextMentionTermination("APPROVE")
        team = RoundRobinGroupChat(
            [planner.plan_trip(), researcher.research_destinations()], 
            termination_condition=termination,
        )
        
        task = f"I want a {request.days} day trip to {request.destination} with a budget of Rs.{request.budget} from {request.source} for {request.people} people. Can you help me plan it?"
        response = await team.run(task=task)
        
        if hasattr(response, 'messages') and response.messages:
            final_message = response.messages[-2] if len(response.messages) > 1 else response.messages[-1]
            if hasattr(final_message, 'content'):
                return {"plan": final_message.content}
            
        
        return {"plan":response}
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return {"detail": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
