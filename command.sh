# INSTALL
pip3 install matplotlib

# CRON
echo "*/1 9-17 * * 1-5 python3 gappi/main.py > log/main.log && python3 gappi/poster.py > log/poster.log" > cron

crontab cron