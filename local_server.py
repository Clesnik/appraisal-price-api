#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import asyncio
import subprocess
import sys
import os
from typing import Dict, Any

app = FastAPI(title="Local Nadlan Appraisal API", description="Local API for testing Nadlan appraisal automation")

class AppraisalRequest(BaseModel):
    wait_time: int = 3000
    screenshot_path: str = "appraisal_fee_test.png"
    headless: bool = False  # FALSE = VISIBLE BROWSER
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
    product: int
    date_appraisal_needed: str

@app.get("/")
async def root():
    return {"message": "Local Nadlan Appraisal API is running"}

@app.post("/run-appraisal")
async def run_appraisal(request: AppraisalRequest):
    """
    Run the Nadlan appraisal script with the provided variables
    """
    try:
        # Convert the request to JSON string
        variables_json = json.dumps(request.dict())
        
        print(f"🔍 Received request: {variables_json}")
        
        # Run the script using subprocess
        result = subprocess.run(
            [sys.executable, "nadlan_playwright_simple_working.py", variables_json],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        print(f"📤 Script stdout: {result.stdout}")
        print(f"📤 Script stderr: {result.stderr}")
        
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
    return {"status": "healthy", "message": "Local Nadlan API is running"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting local FastAPI server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🔍 API docs will be available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
