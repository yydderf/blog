#!/bin/bash

cd /Users/ydderf/Workspace/projects/ydderfsblog && {
    rsync -av --delete "/Users/ydderf/Vaults/C/7 - Posts/" "/Users/ydderf/Workspace/projects/ydderfsblog/content/posts/"
    python3 images.py
    hugo build -b 'https://blog.ydderf.dev/'
    git add --all
    git commit
    git push
    git subtree split --prefix public -b deploy
    git push origin deploy:deploy --force
    git branch -D deploy
}
echo "[+] Done"
