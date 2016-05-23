!#/bin/sh
# Install mysql driver
git clone https://github.com/mysql/mysql-connector-python.git
cd mysql-connector-python
python ./setup.py build
sudo python ./setup.py install
