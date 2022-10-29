from __future__ import annotations

import logging
import sys

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.ERROR)

_LOG_FORMAT = "%(name)-25s %(levelname)-8s %(message)s"

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter(_LOG_FORMAT))
LOG.addHandler(handler)
