from mcp.server.fastmcp import FastMCP

from lib.tool_generator import generate_all_tools
from lib.apidocs_loader import load_apidocs_templates

import tools.health as health
import tools.common as common
import tools.server_apis as server_apis
import tools.query_apis as query_apis
import tools.project_apis as project_apis
import tools.general_apis as general_apis

mcp = FastMCP("om-metrics")

health.register(mcp)
common.register(mcp)
server_apis.register(mcp)
query_apis.register(mcp)
project_apis.register(mcp)
templates = load_apidocs_templates()
generate_all_tools(mcp, templates)
general_apis.register(mcp)

def main():
    """命令行入口函数"""
    mcp.run()

if __name__ == "__main__":
    main()
