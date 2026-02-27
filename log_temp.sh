#!/bin/bash

server_ip="192.168.0.197:8000"  # local server ip and port where temp logger server is hosted

current_local_server=$(hostname -I | awk '{print $1}')
current_date_time=$(date +%Y-%m-%d_%H-%M-%S)
current_sensors=$(
paste <(cat /sys/class/thermal/thermal_zone*/type) \
      <(cat /sys/class/thermal/thermal_zone*/temp) 2>/dev/null | \
awk '
BEGIN {
    print "["
}
{
    if (NR > 1) printf ",\n"
    printf "  {\"sensor\":\"%s\",\"temperature\":\"%.1f °C\"}", $1, $2/1000
}
END {
    if (NR > 0) printf "\n"
    print "]"
}'
)

curl -X POST -H "Content-Type: application/json" \  -d "{\"server\": \"$current_local_server\", \"sensors\": $current_sensors, \"updated_at\": \"$current_date_time\"}" \
  "http://$server_ip/temperature"
