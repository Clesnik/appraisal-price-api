from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import asyncio
import subprocess
import sys
import os
from typing import Dict, Any

app = FastAPI(title="Fixed Nadlan Appraisal API", description="API for running Nadlan appraisal automation")

class AppraisalRequest(BaseModel):
    wait_time: int = 3000
    screenshot_path: str = "appraisal_fee_test.png"
    headless: bool = True
    username: str
    password: str
    transaction_type: str
    loan_type: str
    loan_number: str
    borrower: str
    property_type: str
    property_address: str
    property_city: str
    property_state: str
    property_zip: str
    occupancy_type: str
    contact_person: str
    other_access_instructions: str
    agent_name: str
    product: int  # INTEGER - NOT STRING
    date_appraisal_needed: str

@app.get("/")
async def root():
    return {"message": "Fixed Nadlan Appraisal API is running - ACCEPTS INTEGER PRODUCT"}

@app.post("/run-appraisal")
async def run_appraisal(request: AppraisalRequest):
    """
    Run the Nadlan appraisal script with the provided variables
    """
    try:
        print(f"🔍 Received request with product: {request.product} (type: {type(request.product)})")
        
        # Convert the request to JSON string using model_dump (Pydantic v2)
        variables_json = json.dumps(request.model_dump())
        
        print(f"📤 Sending to script: {variables_json}")
        
        # Run the script using subprocess
        result = subprocess.run(
            [sys.executable, "nadlan_playwright_simple.py", variables_json],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        print(f"📥 Script stdout: {result.stdout}")
        print(f"📥 Script stderr: {result.stderr}")
        
        # Parse the JSON output from the script
        try:
            # Find the JSON output in the stdout
            output_lines = result.stdout.strip().split('\n')
            json_output = None
            
            for line in output_lines:
                if line.startswith('{') and line.endswith('}'):
                    try:
                        json_output = json.loads(line)
                        break
                    except json.JSONDecodeError:
                        continue
            
            if json_output:
                return json_output
            else:
                return {
                    "status": "partial_success",
                    "message": "Script ran but no JSON output found",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "return_code": result.returncode
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to parse script output: {str(e)}",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Script execution timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute script: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Fixed Nadlan API is running - ACCEPTS INTEGER PRODUCT"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
