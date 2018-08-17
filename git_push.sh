#!/bin/bash

git pull

git add ./data/md

ls_date=`date +%Y-%m-%d`
git commit -m "$ls_date commit md file"

git push
