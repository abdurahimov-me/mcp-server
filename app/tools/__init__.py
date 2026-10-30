from app.tools import greet
from app.utils.tools import Tools


__tools__ = Tools(registrars=(greet.register_tools,))
