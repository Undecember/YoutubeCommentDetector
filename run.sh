mkdir -p logs
chown --reference=main.py logs
python -u main.py YCalarm > logs/latest.log 2> logs/latest.error.log
