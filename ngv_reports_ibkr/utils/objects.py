import json


def gen_json(obj):
    """
    Gen json from object, or nested-objects.
    """
    return json.loads(json.dumps(obj, default=lambda o: getattr(o, "__dict__", str(o))))
