from json import JSONEncoder


class DefaultToStrJSONEncoder(JSONEncoder):
    def default(self, o):
        return str(o)
