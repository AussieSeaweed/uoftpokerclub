import json
from typing import Any


class InformationSetJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        return str(o)
