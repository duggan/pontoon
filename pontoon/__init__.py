# -*- coding: utf-8 -*-

import os
from .cache import cache
from .log import debug

from .exceptions import *

MOCK = True if os.environ.get("MOCK") else False
