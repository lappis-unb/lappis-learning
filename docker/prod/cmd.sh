#!/bin/bash

salicml --train all
python -m gunicorn.app.wsgiapp --bind=0.0.0.0:5000 --workers=4 salicml.api.main:app
