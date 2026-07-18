from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Any
from src.agent.orchestrator import PurpleOrchestrator
from src.agent.tools import PurpleTeamTools

app = FastAPI(
    title="Purple Team AI API",
    description="API to orchestrate security simulations and detection validation on Linux",
    version="1.0.0",
)

# Initialize the orchestrator and tools
orchestrator = PurpleOrchestrator()
tools = PurpleTeamTools()


class SimulationRequest(BaseModel):
    ttp_id: str


class ValidationResponse(BaseModel):
    ttp_id: str
    status: str
    detected: bool
    remediation: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Purple Team AI API is online", "status": "healthy"}


@app.post("/simulate", response_model=Dict[str, str])
async def simulate(request: SimulationRequest):
    """
    Triggers a specific attack simulation.
    """
    try:
        result = tools.simulate_attack(request.ttp_id)
        return {"ttp_id": request.ttp_id, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/check/{ttp_id}", response_model=Dict[str, Any])
async def check(ttp_id: str):
    """
    Checks if the simulated attack was detected by the SIEM.
    """
    try:
        result = tools.check_detection(ttp_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate-all", response_model=Dict[str, str])
async def validate_all(auto_fix: bool = False):
    """
    Runs the full validation cycle. If auto_fix=True, it performs Closed-Loop remediation.
    """
    try:
        results = orchestrator.run_validation_cycle(auto_fix=auto_fix)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reasoning")
async def get_reasoning():
    """
    Returns the agent's thought process from the last run.
    """
    return {"logs": orchestrator.reasoning_log}


@app.post("/test-noise", response_model=Dict[str, str])
async def test_noise():
    """
    Performs noise analysis to identify false positives.
    """
    try:
        results = orchestrator.validate_noise()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/coverage")
async def get_coverage():
    """
    Returns the current security coverage map.
    """
    return orchestrator.results
