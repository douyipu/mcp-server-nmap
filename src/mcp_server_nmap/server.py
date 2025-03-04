import subprocess
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("NmapServer")

@mcp.tool()
def run_nmap(target: str, options: str = "-sV") -> str:
    """
    Run Nmap to scan the target host.

    Parameters:
        target (str): The target to scan, such as "192.168.1.1" or "example.com".
        options (str): Nmap options, default is "-sV" (service version detection).

    Returns:
        str: The result of the Nmap scan.
    """
    try:
        # Execute the Nmap command
        command = f"nmap {options} {target}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return "Error: Nmap execution timed out"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")