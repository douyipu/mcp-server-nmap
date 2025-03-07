import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Nmap")

#, ports: str, scanType: str, timing: str, additionalFlags: str
@mcp.tool()
def run_nmap_scan(target: str) -> str:
    print("Running nmap scan...")
    result = subprocess.run(["nmap", target], capture_output=True, text=True)
    if(result.stderr):
        return result.stderr
    return result.stdout

# 运行 MCP 服务器
if __name__ == "__main__":
    print("Starting Nmap server...")
    mcp.run()
    print("Nmap server stopped.")
