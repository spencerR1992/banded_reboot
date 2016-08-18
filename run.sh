#!/bin/bash
gunicorn banded.wsgi --workers 3