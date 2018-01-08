#!/bin/bash
echo "# ps-addon" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:inosboxes/ps-addon.git
git push -u origin master

