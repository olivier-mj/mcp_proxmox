from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from src.client import ProxmoxClient
import os

app = FastAPI(
    title="Proxmox MCP API",
    description="REST API to control Proxmox VE, compatible with LobeChat Plugins.",
    version="1.0.0",
)

# Initialize Proxmox Client
try:
    proxmox = ProxmoxClient()
except Exception as e:
    print(f"Warning: Proxmox Client initialization failed: {e}")
    proxmox = None

# --- Pydantic Models ---

class MachineActionRequest(BaseModel):
    node: str
    vmid: int
    type: str  # 'qemu' or 'lxc'

class StopMachineRequest(MachineActionRequest):
    force: bool = False

class SnapshotRequest(MachineActionRequest):
    snapname: str
    description: Optional[str] = None

class RollbackRequest(MachineActionRequest):
    snapname: str

class CloneRequest(MachineActionRequest):
    newid: int
    name: str
    target_node: Optional[str] = None

class ResizeRequest(MachineActionRequest):
    cores: Optional[int] = None
    memory_mb: Optional[int] = None

class CreateBackupRequest(BaseModel):
    node: str
    vmid: int
    storage: str
    mode: str = "snapshot"

class FirewallRuleRequest(MachineActionRequest):
    action: str
    direction: str # 'in' or 'out'
    proto: Optional[str] = None
    port: Optional[str] = None

# --- Endpoints ---

@app.get("/infrastructure", summary="List Infrastructure Nodes")
def list_infrastructure():
    """Lists all nodes in the Proxmox cluster with their CPU and RAM usage."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    
    nodes = proxmox.get_nodes()
    results = []
    for node in nodes:
        # Fetch detailed resources for each node
        try:
            res = proxmox.get_node_resources(node['node'])
            results.append({
                "node": node['node'],
                "status": node.get('status', 'unknown'),
                "cpu_usage": f"{res.get('cpu', 0) * 100:.1f}%",
                "ram_usage": f"{res.get('memory', {}).get('used', 0) / 1024**3:.1f} GB / {res.get('memory', {}).get('total', 0) / 1024**3:.1f} GB"
            })
        except:
             results.append({"node": node['node'], "status": "unreachable"})
    return results

@app.get("/machines", summary="List all Machines")
def list_machines(
    name_filter: Optional[str] = None,
    status_filter: Optional[str] = Query(None, enum=["running", "stopped"]),
    type_filter: Optional[str] = Query(None, enum=["qemu", "lxc"])
):
    """Lists all VMs and Containers (LXC) with optional filtering."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    
    machines = proxmox.get_all_machines()
    filtered = []
    for m in machines:
        if name_filter and name_filter.lower() not in m.get('name', '').lower(): continue
        if status_filter and m.get('status') != status_filter: continue
        if type_filter and m.get('type') != type_filter: continue
        
        filtered.append({
            "vmid": m.get('vmid'),
            "name": m.get('name'),
            "node": m.get('node'),
            "type": m.get('type'),
            "status": m.get('status'),
            "uptime": m.get('uptime')
        })
    return filtered

@app.get("/storage", summary="List Storage")
def list_storage(content_filter: Optional[str] = None):
    """Displays the storage status for all nodes."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    
    nodes = proxmox.get_nodes()
    results = []
    for node in nodes:
        try:
            storages = proxmox.get_storage_status(node['node'])
            for s in storages:
                 if content_filter and content_filter not in s.get('content', ''): continue
                 results.append({
                     "node": node['node'],
                     "storage": s.get('storage'),
                     "content": s.get('content'),
                     "used_fraction": f"{s.get('used_fraction', 0) * 100:.1f}%",
                     "total": f"{s.get('total', 0) / 1024**3:.1f} GB"
                 })
        except:
            pass
    return results

@app.post("/machines/start", summary="Start a Machine")
def start_machine(req: MachineActionRequest):
    """Starts a specific machine."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return {"task_id": proxmox.set_machine_state(req.node, req.vmid, req.type, "start")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/machines/stop", summary="Stop a Machine")
def stop_machine(req: StopMachineRequest):
    """Stops a specific machine (shutdown or force stop)."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    action = "stop" if req.force else "shutdown"
    try:
        return {"task_id": proxmox.set_machine_state(req.node, req.vmid, req.type, action)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/machines/reboot", summary="Reboot a Machine")
def reboot_machine(req: MachineActionRequest):
    """Reboots a specific machine."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return {"task_id": proxmox.set_machine_state(req.node, req.vmid, req.type, "reboot")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/machines/{node}/{vmid}/config", summary="Get Machine Configuration")
def get_machine_config(node: str, vmid: int, type: str = Query(..., enum=["qemu", "lxc"])):
    """Retrieves the detailed configuration of a machine."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return proxmox.get_machine_config(node, vmid, type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/machines/clone", summary="Clone a Machine")
def clone_machine(req: CloneRequest):
    """Clones a machine."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return {"task_id": proxmox.clone_machine(req.node, req.vmid, req.newid, req.name, req.type, req.target_node)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/snapshots", summary="Create Snapshot")
def create_snapshot(req: SnapshotRequest):
    """Creates a snapshot."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return {"task_id": proxmox.create_snapshot(req.node, req.vmid, req.type, req.snapname, req.description)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/snapshots/rollback", summary="Rollback Snapshot")
def rollback_snapshot(req: RollbackRequest):
    """Rolls back to a snapshot."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return {"task_id": proxmox.rollback_snapshot(req.node, req.vmid, req.type, req.snapname)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/snapshots", summary="List Snapshots")
def list_snapshots(node: str, vmid: int, type: str = Query(..., enum=["qemu", "lxc"])):
    """Lists snapshots."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return proxmox.list_snapshots(node, vmid, type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/backups", summary="Create Backup")
def create_backup(req: CreateBackupRequest):
    """Creates a backup."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return {"task_id": proxmox.create_backup(req.node, req.vmid, req.storage, req.mode)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/backups", summary="List Backups")
def list_backups(node: str, storage: str):
    """Lists backups."""
    if not proxmox: raise HTTPException(status_code=503, detail="Proxmox client not initialized")
    try:
        return proxmox.list_backups(node, storage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

