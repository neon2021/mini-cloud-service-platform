from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import json
import asyncio
import logging
from pathlib import Path
from . import config
from .runtime import LambdaRuntime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Local Lambda Service")

@app.post("/functions/{function_name}")
async def deploy_function(function_name: str, code: UploadFile = File(...)):
    try:
        function_dir = config.FUNCTIONS_DIR / function_name
        function_dir.mkdir(parents=True, exist_ok=True)
        
        function_path = function_dir / "lambda_function.py"
        with open(function_path, "wb") as f:
            shutil.copyfileobj(code.file, f)
        
        logger.info(f"Successfully deployed function {function_name}")
        return {"message": f"Function {function_name} deployed successfully"}
    except Exception as e:
        logger.error(f"Failed to deploy function {function_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/2015-03-31/functions/{function_name}/invocations")
async def invoke_function(function_name: str, event: dict):
    try:
        function_path = config.FUNCTIONS_DIR / function_name / "lambda_function.py"
        
        if not function_path.exists():
            raise HTTPException(status_code=404, detail=f"Function {function_name} not found")
        
        result = await LambdaRuntime.invoke(function_path, event)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Failed to invoke function {function_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 