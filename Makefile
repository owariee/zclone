.PHONY: run clean install_python db install

install_python:
	sudo apt-get install -y build-essential gdb lcov pkg-config \
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev
	asdf install

run: venv
	. venv/bin/activate && flask --app src run --debug && deactivate

venv:
	python -m venv venv
	. venv/bin/activate && python -m pip install -r requirements.txt && deactivate

clean:
	rm -rf venv

db:
	. venv/bin/activate && flask --app src:make_db run --debug && deactivate

install: clean install_python run