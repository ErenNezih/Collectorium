import os
from . import DEFAULT_FEATURE_FLAGS


def feature_flags(request):
    flags = {}
    for key, default in DEFAULT_FEATURE_FLAGS.items():
        raw = os.environ.get(key)
        if raw is None:
            flags[key] = default
        else:
            flags[key] = raw.lower() in ("1", "true", "yes")
    return {"ff": flags}



