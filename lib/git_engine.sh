#!/data/data/com.termux/files/usr/bin/bash

ROOT="${2:-.}"

cd "$ROOT" || exit 1

COMMAND="${1:-status}"

case "$COMMAND" in

status)
echo "========== GIT STATUS =========="
git status
;;

branch)
echo "========== BRANCH =========="
git branch -vv
;;

log)
echo "========== LAST 20 COMMITS =========="
git log --graph --decorate --oneline -20
;;

diff)
echo "========== DIFF =========="
git diff
;;

remote)
echo "========== REMOTES =========="
git remote -v
;;

fetch)
echo "========== FETCH =========="
git fetch --all --prune
;;

pull)
echo "========== PULL =========="
git pull
;;

push)
echo "========== PUSH =========="
git push
;;

*)
echo "Available commands:"
echo
echo "status"
echo "branch"
echo "log"
echo "diff"
echo "remote"
echo "fetch"
echo "pull"
echo "push"
;;

esac
