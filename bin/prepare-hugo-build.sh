#!/bin/env bash

echo "Copying last-updates.json file to data folder."
cp feed/last-updates.json site/data/

echo "Copying all feeds files to static/feed folder."
mkdir -p site/static/feed/
cp feed/*.xml site/static/feed/

echo "Done and ready for building the website."
