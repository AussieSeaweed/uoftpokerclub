from json import JSONEncoder
from typing import Any


class InformationSetJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        return str(o)
