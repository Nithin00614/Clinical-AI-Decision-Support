import json
import os


def load_drift_metrics_safe():
    """
    Safe loader for drift metrics.
    Returns empty dict if file missing.
    """

    BASE = os.path.dirname(__file__)
    path = os.path.join(BASE, "artifacts", "drift_metrics.json")

    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)

    except Exception:
        pass

    return {}