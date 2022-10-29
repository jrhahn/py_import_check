from __future__ import annotations

import json

from package_2.code2 import hello2


def run():
    hello2()
    json.loads("{'hello': 'world'}")


if __name__ == "__main__":
    run()
