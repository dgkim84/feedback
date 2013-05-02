#!/bin/sh
. env/bin/activate
gunicorn -w 2 -b 0.0.0.0:3122 run:app
