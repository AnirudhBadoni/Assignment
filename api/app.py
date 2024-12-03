from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .utils.terraform_utils import generate_terraform, run_terraform
from .utils.ansible_utils import generate_ansible_inventory, run_ansible

# Initialize FastAPI app
app = FastAPI()

# Request model
class ConfigParams(BaseModel):
    postgres_version: str
    instance_type: str
    num_replicas: int
    max_connections: int
    shared_buffers: str

# Endpoints

@app.post("/generate")
async def generate_configs(params: ConfigParams):
    """
    Generate Terraform configuration for PostgreSQL infrastructure.
    """
    try:
        terraform_config = generate_terraform(params.dict())
        return {"message": "Terraform configuration generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/provision")
async def provision_infrastructure():
    """
    Provision PostgreSQL infrastructure using Terraform.
    """
    try:
        success, output = run_terraform()
        if success:
            return {"message": "Infrastructure provisioned successfully"}
        else:
            raise HTTPException(status_code=500, detail=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/configure")
async def configure_postgresql():
    """
    Configure PostgreSQL on provisioned EC2 instances using Ansible.
    """
    try:
        # Generate Ansible inventory (mock example, replace with actual IPs)
        instances = {
            "primary": "10.0.0.1",
            "replicas": ["10.0.0.2", "10.0.0.3"],
        }
        generate_ansible_inventory(instances)

        # Run Ansible playbook
        success, output = run_ansible()
        if success:
            return {"message": "PostgreSQL configured successfully"}
        else:
            raise HTTPException(status_code=500, detail=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/status")
async def fetch_status():
    # Placeholder for future implementation
    return {"status": "Not implemented yet"}
