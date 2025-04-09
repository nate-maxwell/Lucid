from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImportTask(object):
    """Import Task options for importing files into engine."""
    source_path: Path
    destination_package_path: Path
    import_name: str = ''
    reimport: bool = True
