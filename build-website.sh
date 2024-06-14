#!/bin/env sh

echo "Generate all feeds"
poetry run python generate_feed.py

sh bin/prepare-hugo-build.sh

echo "Building Hugo website"
cd site
hugo

echo "Done!"
