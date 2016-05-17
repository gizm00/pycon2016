FROM jupyter/notebook
RUN pip install --upgrade pip
RUN apt-get install libxml2-dev libxslt1-dev
# install other packages required for tutorial
ADD requirements.txt /
RUN pip install -r /requirements.txt && rm -rf /root/.cache/pip/*
