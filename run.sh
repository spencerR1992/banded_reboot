#!/bin/bash
sudo apt-get install libcairo2-dev
gunicorn banded.wsgi --workers 3