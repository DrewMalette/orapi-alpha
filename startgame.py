#!/usr/bin/env python3

import sys
sys.path.append("./")

import importlib

entrypoint = importlib.import_module("scripts.entrypoint")

entrypoint.init()

