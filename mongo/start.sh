#!/bin/bash
PATH_CONF="$(realpath mongodb.conf)"

PATH_DATA="$(realpath data)"
PATH_LOG_DIR="$(realpath log)"
PATH_LOG="$(realpath "$PATH_LOG_DIR/mongod.log")"

mkdir -p "$PATH_DATA"
mkdir -p "$PATH_LOG_DIR"

if [ ! -f "pid.txt" ]; then
  nohup 2>&1 mongod --config "$PATH_CONF" --dbpath "$PATH_DATA" --logpath "$PATH_LOG" &
  echo $! > pid.txt
  echo "Launched process"
else
  echo "[!] Did not launch process: pid file already exists"
fi