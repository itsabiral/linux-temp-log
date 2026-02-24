Executable permission 

```
chmod +x /home/jhilke-pi/scripts/linux-temp-logger/log_temp.sh

```
Add to crontab (crontab -e), log every 8 minutes.

```

*/8 * * * * /home/jhilke-pi/scripts/linux-temp-logger/log_temp.sh >> /home/jhilke-pi/temp_cron.log 2>&1
@reboot nohup python3 /home/jhilke-pi/scripts/linux-temp-logger/server/log_temp.py > log_temp_server.log 2>&1 &
```

POST or GET to /temperature.
