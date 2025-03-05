import asyncio
import json
from typing import Optional
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
import subprocess

# Define Nmap scan task parameters model
class NmapScanParams(BaseModel):
    target: str = Field(..., description="Target host for scanning")
    ports: Optional[str] = Field(None, description="Port range, e.g., '22-80' or '80,443'")
    scanType: str = Field("quick", description="Scan type, available options: quick, full, version")
    timing: int = Field(3, ge=0, le=5, description="Nmap scan timing template (T0-T5)")
    additionalFlags: Optional[str] = Field(None, description="Additional Nmap parameters")

# Initialize MCP server
mcp = FastMCP("nmap-server", version="0.1.0")

# Define Nmap scanning tool
@mcp.tool()
async def run_nmap_scan(params: NmapScanParams, ctx: Context) -> str:
    """Execute Nmap scan"""
    command = ["nmap", f"-T{params.timing}"]

    # Set scan type
    if params.scanType == "quick":
        command.append("-F")
    elif params.scanType == "full":
        command.append("-p-")
    elif params.scanType == "version":
        command.append("-sV")

    # Port parameter
    if params.ports:
        command.append(f"-p{params.ports}")

    # Additional parameters
    if params.additionalFlags:
        command.extend(params.additionalFlags.split())

    # Target
    command.append(params.target)

    await ctx.info(f"Executing command: {' '.join(command)}")

    try:
        # Execute command
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stderr:
            return f"Nmap stderr: {stderr.decode()}"

        return stdout.decode()
    except Exception as e:
        return f"Failed to execute Nmap: {str(e)}"

# Run MCP server
if __name__ == "__main__":
    mcp.run()
