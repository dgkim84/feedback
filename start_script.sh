#!/bin/sh
. env/bin/activate
gunicorn -w 2 -b unix:/tmp/feedback.sock run:app
