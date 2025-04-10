#!/bin/bash
export FLASK_APP=app,app:app
export FLASK_ENV=development
PYTHONPATH=$(pwd) flask run

