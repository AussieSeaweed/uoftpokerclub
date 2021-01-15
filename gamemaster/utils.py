from json import JSONEncoder


class InformationSetJSONEncoder(JSONEncoder):
    def default(self, o):
        return str(o)
