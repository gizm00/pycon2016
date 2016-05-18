FROM jupyter/notebook
RUN apt-get update && apt-get install -y \ 
	libxml2-dev \ 
	libxslt1-dev \
	firefox \
 	xvfb
RUN pip install --upgrade pip
ADD requirements.txt /
RUN pip install -r /requirements.txt && rm -rf /root/.cache/pip/*
