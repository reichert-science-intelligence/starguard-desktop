#!/usr/bin/env sh
# StarGuard AI Mobile — deploy/run script (Git Bash / WSL / Mac/Linux)
set -e
cd "$(dirname "$0")"

echo ""
echo " StarGuard AI Mobile - Deploy / Run"
echo " ================================="
echo ""
echo " 1 = Local only       (http://127.0.0.1:8000)"
echo " 2 = Network (mobile) (http://YOUR-IP:8000)"
echo " 3 = Port 8502        (http://127.0.0.1:8502)"
echo " 4 = Help (shinyapps.io, firewall)"
echo ""
printf " Choice (1-4): "
read -r choice

case "$choice" in
  1)
    echo ""
    echo " Starting local. Open http://127.0.0.1:8000"
    exec shiny run app.py
    ;;
  2)
    echo ""
    echo " Starting with network access. On phone (same WiFi): http://YOUR-IP:8000"
    echo " Find IP: ifconfig or ip addr"
    exec shiny run app.py --host 0.0.0.0
    ;;
  3)
    echo ""
    echo " Starting on port 8502. Open http://127.0.0.1:8502"
    exec shiny run app.py --port 8502
    ;;
  4)
    echo ""
    echo " shinyapps.io: pip install rsconnect-python"
    echo " rsconnect add --account YOUR_ACCOUNT --name shinyapps"
    echo " rsconnect deploy shiny . --name starguard-mobile"
    echo ""
    echo " Firewall: allow Python or inbound TCP 8000."
    ;;
  *)
    echo " Invalid. Running local (option 1)."
    exec shiny run app.py
    ;;
esac
