import dataclasses
import json
from decimal import Decimal
from typing import Any


def _to_jsonable(o: Any) -> Any:
    # ib_async v3 records are slotted dataclasses with no __dict__.
    if dataclasses.is_dataclass(o) and not isinstance(o, type):
        return {f.name: getattr(o, f.name) for f in dataclasses.fields(o)}
    if isinstance(o, Decimal):
        return str(o)
    return getattr(o, "__dict__", str(o))


def gen_json(obj):
    """
    Gen json from object, or nested-objects.
    """
    return json.loads(json.dumps(obj, default=_to_jsonable))
