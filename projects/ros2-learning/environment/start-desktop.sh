#!/usr/bin/env bash
set -euo pipefail

mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1

Xvfb :1 -screen 0 1280x800x24 -ac +extension GLX +render -noreset > /tmp/amr-xvfb.log 2>&1 &
sleep 2
openbox > /tmp/amr-openbox.log 2>&1 &
x11vnc -display :1 -forever -shared -nopw -rfbport 5900 > /tmp/amr-x11vnc.log 2>&1 &
websockify --web=/usr/share/novnc 6080 localhost:5900 > /tmp/amr-novnc.log 2>&1 &

echo "AMR desktop ready at http://localhost:6080/vnc.html"
wait
