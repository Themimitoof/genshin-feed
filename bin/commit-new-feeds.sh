#!/bin/env bash

if [ "$GERALDO_BOULARDO_TOKEN" == "" ]; then
    echo "Sorry you're not in a GitHub Actions context, you can't use this script."
    exit 1
fi

echo "Setup Git initial config"
git config user.name "geraldo.boulardo"
git config user.email "geraldo.boulardo@themimitoof.fr"
git remote add githubActions https://git:$GERALDO_BOULARDO_TOKEN@github.com/themimitoof/genshin-feed.git

echo "Commit all new feeds"
git add feed/*
git commit -m "Update all feeds"

echo "PUSH DA STUFF!"
git push -u githubActions master
