from fastapi import FastAPI, HTTPException
import logging
from . import models
from .lima_vm import LimaVMClient

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mini EC2 Service")

try:
    vm_client = LimaVMClient()
    logger.info("Successfully initialized Lima VM client")
except Exception as e:
    logger.error(f"Failed to initialize Lima VM client: {str(e)}")
    raise

@app.post("/instances", response_model=dict)
async def create_instance(params: models.InstanceCreate):
    try:
        result = vm_client.create_instance(params)
        return {"name": result["name"], "status": result["status"]}
    except Exception as e:
        logger.error(f"Failed to create instance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/instances/{instance_name}", response_model=models.InstanceStatus)
async def get_instance(instance_name: str):
    try:
        return vm_client.get_instance(instance_name)
    except Exception as e:
        logger.error(f"Failed to get instance {instance_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Instance {instance_name} not found")

@app.post("/instances/{instance_name}/actions")
async def instance_action(instance_name: str, action: models.InstanceAction):
    try:
        if action.action == "start":
            vm_client.start_instance(instance_name)
        elif action.action == "stop":
            vm_client.stop_instance(instance_name)
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        return {"message": f"Action {action.action} performed successfully"}
    except Exception as e:
        logger.error(f"Failed to perform action {action.action} on instance {instance_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/instances/{instance_name}")
async def delete_instance(instance_name: str):
    try:
        vm_client.delete_instance(instance_name)
        return {"message": f"Instance {instance_name} deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete instance {instance_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 