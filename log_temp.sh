#!/bin/bash

server_ip="192.168.0.197:8000"  # local server ip and port where temp logger server is hosted

current_local_server=$(hostname -I | awk '{print $1}')
current_date_time=$(date +%Y-%m-%d_%H-%M-%S)
current_temperature=$(cat /sys/class/thermal/thermal_zone0/temp | awk '{printf "%.1f°C", $1/1000}')

curl -X POST -H "Content-Type: application/json" \
  -d "{\"server\": \"$current_local_server\", \"updated_at\": \"$current_date_time\", \"temperature\": \"$current_temperature\"}" \
  "http://$server_ip/temperature"
