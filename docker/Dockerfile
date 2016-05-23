# Dockerfile for pycon2016 The Fellowship of The Data tutorial
# Dockerfile copied from jupyter/notebook with some changes based on
# the notebook-minimal docker stack and required libs for the tutorial


# Installs Jupyter Notebook and IPython kernel from the current branch
# Another Docker container should inherit with `FROM jupyter/notebook`
# to run actual services.
#
# For opinionated stacks of ready-to-run Jupyter applications in Docker, 
# check out docker-stacks <https://github.com/jupyter/docker-stacks>

FROM jupyter/ubuntu_14_04_locale_fix

#MAINTAINER Project Jupyter <jupyter@googlegroups.com>

# Not essential, but wise to set the lang
# Note: Users with other languages should set this in their derivative image
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV PYTHONIOENCODING UTF-8

# Remove preinstalled copy of python that blocks our ability to install development python.
RUN DEBIAN_FRONTEND=noninteractive apt-get remove -yq \
        python3-minimal \
        python3.4 \
        python3.4-minimal \
        libpython3-stdlib \
        libpython3.4-stdlib \
        libpython3.4-minimal

# Python binary and source dependencies
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
	wget \
        language-pack-en \
        libcurl4-openssl-dev \
        libffi-dev \
        libsqlite3-dev \
        libzmq3-dev \
        pandoc \
        python \
        python3 \
        python-dev \
        python3-dev \
        sqlite3 \
        texlive-fonts-recommended \
        texlive-latex-base \
        texlive-latex-extra \
        zlib1g-dev \
	libxml2-dev \
        libxslt1-dev \
        firefox \
        xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install mysql driver
RUN git clone https://github.com/mysql/mysql-connector-python.git /tmp/mysql-connector-python
RUN cd /tmp/mysql-connector-python
RUN pwd
RUN python /tmp/mysql-connector-python/setup.py build
RUN sudo python /tmp/mysql-connector-python/setup.py install

#ADD install_mysql.sh /
#RUN source /install_mysql.sh

# Install Tini
RUN curl -L https://github.com/krallin/tini/releases/download/v0.6.0/tini > tini && \
    echo "d5ed732199c36a1189320e6c4859f0169e950692f451c03e7854243b95f4234b *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Install the recent pip release
RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python2 get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py && \
    pip2 --no-cache-dir install requests[security] && \
    pip3 --no-cache-dir install requests[security] && \
    rm -rf /root/.cache

# Install some dependencies.
RUN pip2 --no-cache-dir install ipykernel && \
    pip3 --no-cache-dir install ipykernel && \
    \
    python2 -m ipykernel.kernelspec && \
    python3 -m ipykernel.kernelspec && \
    rm -rf /root/.cache


# Move notebook contents into place.
ADD . /usr/src/jupyter-notebook

# Install dependencies and run tests.
#RUN BUILD_DEPS="nodejs-legacy npm" && \
#    apt-get update -qq && \
#    DEBIAN_FRONTEND=noninteractive apt-get install -yq $BUILD_DEPS && \
#    \
#    pip3 install --no-cache-dir /usr/src/jupyter-notebook && \
#    pip2 install --no-cache-dir widgetsnbextension && \
#    pip3 install --no-cache-dir widgetsnbextension && \
#    \
#    npm cache clean && \
#    apt-get clean && \
#    rm -rf /root/.npm && \
#    rm -rf /root/.cache && \
#    rm -rf /root/.config && \
 #   rm -rf /root/.local && \
 #   rm -rf /root/tmp && \
 #   rm -rf /var/lib/apt/lists/* && \
 #   apt-get purge -y --auto-remove \
 #       -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false $BUILD_DEPS

RUN pip install notebook

# Run tests.
# hanging on completion, comment out for now
#RUN pip3 install --no-cache-dir notebook[test] && nosetests -v notebook

# Add class content
ADD requirements.txt /
RUN pip install -r /requirements.txt && rm -rf /root/.cache/pip/*

# Setup bokeh sample data
ADD bokeh_download.py /
RUN python /bokeh_download.py

# Add a notebook profile.
RUN mkdir -p -m 700 /root/.jupyter/ && \
    echo "c.NotebookApp.ip = '*'" >> /root/.jupyter/jupyter_notebook_config.py

# add startup script for notebook
COPY start-notebook.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-notebook.sh

VOLUME /notebooks
WORKDIR /notebooks

EXPOSE 8888

#ENTRYPOINT ["tini", "--"]
#CMD ["jupyter", "notebook", "--no-browser"]
#CMD ["start-notebook.sh"]
