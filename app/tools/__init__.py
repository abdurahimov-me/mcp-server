from tools import greet
from utils.tools import ToolMount, Tools


__tools__ = Tools(servers=(ToolMount(server=greet.mcp, namespace="greeting"),))
