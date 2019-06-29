#!/bin/bash
env $(cat dev-env | xargs) python -m flask run
