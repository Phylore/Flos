#!/bin/bash
export FLASK_APP=app.app:app
export FLASK_DEBUG=1
PYTHONPATH=$(pwd) flask run

