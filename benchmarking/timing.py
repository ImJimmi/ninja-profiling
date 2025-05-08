from datetime import datetime, timedelta
from typing import Callable


def record_timedelta(callable: Callable[..., None], *args) -> timedelta:
    start = datetime.now()
    callable(*args)
    return datetime.now() - start
