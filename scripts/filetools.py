import json
import os
from pathlib import Path


def workspace_path(*paths):
    """Get workspace path."""
    return Path(__file__).parent.parent / Path(*paths).resolve()
