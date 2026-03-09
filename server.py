import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from mcp.server.fastmcp import FastMCP
import tools.health as health
import tools.common as common
import tools.server_apis as server_apis
import tools.query_apis as query_apis
import tools.cla_apis as cla_apis
import tools.project_apis as project_apis

mcp = FastMCP("om-metrics")

health.register(mcp)
common.register(mcp)
server_apis.register(mcp)
query_apis.register(mcp)
cla_apis.register(mcp)
project_apis.register(mcp)

def main():
    """命令行入口函数"""
    mcp.run()

if __name__ == "__main__":
    main()
