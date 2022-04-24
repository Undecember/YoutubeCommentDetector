WD := $(shell pwd)

venv:
	python3.9 -m venv .venv
	. .venv/bin/activate && pip install -r requirements

service:
	sudo cp *.service /etc/systemd/system/
	sudo sed -i 's#BIN_PATH#$(WD)#' /etc/systemd/system/YCalarm.service
	sudo systemctl enable YCalarm
	sudo systemctl daemon-reload
