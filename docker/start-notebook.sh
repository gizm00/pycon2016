#!/bin/bash
# Install mysql driver
git clone https://github.com/mysql/mysql-connector-python.git /tmp/mysql-connector-python
cd /tmp/mysql-connector-python
python ./setup.py build
sudo python ./setup.py install
cd /notebooks
jupyter notebook &> /dev/null &



