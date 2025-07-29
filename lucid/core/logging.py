"""
# Lucid Logging

* Description:

    Logging handlers and utilities.
"""


import logging
import logging.handlers
from pathlib import Path

from lucid.core import const


LOG_FILE = Path(const.USER_LOG_DIR, f'{const.USERNAME}.log')


def main() -> int:
    _logger = logging.getLogger('lucid')
    _logger.setLevel(logging.DEBUG)

    if not _logger.hasHandlers():
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=5_000_000, backupCount=3, encoding='utf-8'
        )
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
        )
        handler.setFormatter(formatter)
        _logger.addHandler(handler)

    return 0


if __name__ == '__main__':
    main()
