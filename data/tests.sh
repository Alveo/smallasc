#!/bin/bash

HOST="localhost:8000"

curl -v --data-binary '@tests/items.json' http://$HOST/data/

