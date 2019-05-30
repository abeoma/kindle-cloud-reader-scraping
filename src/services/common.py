from pathlib import Path

CACHE_ROOT: Path = Path("../data/cache")
if not CACHE_ROOT.exists():
    CACHE_ROOT.mkdir()
