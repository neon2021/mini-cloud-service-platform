from pydantic import BaseModel
from typing import Optional

class LimaInstanceParams(BaseModel):
    name: str
    image_url: str
    cpu: int
    memory: int  # GiB
    disk: int  # GiB

class InstanceCreate(BaseModel):
    name: str
    image_url: Optional[str] = None
    cpu: Optional[int] = None
    memory: Optional[int] = None
    disk: Optional[int] = None

class InstanceStatus(BaseModel):
    name: str
    status: str
    cpu: int
    memory: str
    disk: str
    ssh_port: int

class InstanceAction(BaseModel):
    action: str  # start, stop, restart 