Repo for Object Oriented Web Data Pipelines in Python


## Setup Using Docker  

If you don't have Docker installed start by heading to https://www.docker.com/products/docker. Docker is available for Windows, MacOS, and Linux 

0. Start docker, note the docker IP as YOUR_DOCKER_IP

1. Get the LAMP stack for hosting tutorial files from Docker:  
	`$ docker run -t -i -p 3306:3306 --net=bridge --name=pycon2016_lamp  gizm00/pycon2016_lamp /bin/bash`  

2. In the pycon2016_lamp container you just created, note the IP address by running:  
	`$ ifconfig | grep 'inet addr'`  
	the first line will give you the IP for the container. This is the LAMP_IP  

3. Execute the startup script in the pycon2016_lamp container to setup the mysql database  
	`$ lamp_startup.sh`  

Your LAMP container should now be ready to serve files for the tutorial. 

In a new window clone the tutorial files from Github  
	`git clone https://github.com/gizm00/pycon2016.git`  
	`cd pycon2016/notebooks`  

In the pycon2016/notebooks directory, start the tutorial container  

1. Get the tutorial image from Docker. This will take some time to download, good time for second breakfast:  
	`$ docker run --rm -it --net=bridge -p 8888:8888 --name=pycon2016_notebooks -v "$(pwd):/home/notebooks" gizm00/pycon2016`  

2. In the pycon2016_notebooks container execute the startup script to install the pymysql driver and start the notebook server:  
	`$ start-notebook.sh`  

3. Navigate to http://YOUR_DOCKER_IP:8888/ to see the notebook tree

At this point youre ready to run the test notebook to verify your setup

1. At http://YOUR_DOCKER_IP:8888/ find the config.py file

2. Update config.py with the values you noted above:
	LAMP_IP = your LAMP_IP  
	DB_HOST = YOUR_DOCKER_IP  

3. Save the updated config.py  

4. Open the test_notebook in the Jupyter tree and run the notebook. The resulting plot should be a map titled "Oregon Counties." Hover over the blue points to see campground name and telephone (where available). You can check the notebook outputs against notebooks/test_notebook_output.pdf

### To get the eventbrite registration discount code
Hover over any of the blue dots on the Oregon Counties map. The registration code is the Secret field.


## Setup locally

I strongly suggest using the Docker containers for the tutorial, but here are some notes if you want to run the materials locally. 

1. For a list of required pip packages see 'pycon2016/docker/requirements.txt'  

2. In addition to the above packages you will need  

	firefox (we will be using the firefox driver for Selenium)  
	python 3.4.3  
	jupyter 4.2.0
	mysql-connector-python  

3. To forgo using the pycon2016_lamp container you will need to have a local LAMP stack  

	Refer to the pycon2016_lamp repo: `https://github.com/gizm00/pycon2016_lamp`  

	mysql: setup users and database using the mysql_setup.sql 

	apache: copy the contents of webfiles/ to your apache directory  

4. Get the course materials : `git clone https://github.com/gizm00/pycon2016.git` and run the test_notebook as above
Please get the latest version of the tutorial files from the repo for tomorrow:  
	`$ git clone https://github.com/gizm00/pycon2016.git`  
	`$ cd pycon2016/notebooks`  
	


### Some errors you might see and how to troubleshoot:

##### `URLError: <urlopen error [Errno 111] Connection refused>`  

Usually this means the apache server needs to be restarted. To do so, execute the following in the LAMP container shell:  
		`$ /etc/init.d/apache2 restart`

##### `(pymysql.err.OperationalError) (2013, 'Lost connection to MySQL server during query')`  

Usually this means the mysql server needs to be restarted (and often occurs after you have encountered the above error and restarted apache).  To fix, restart mysql in the LAMP container shell:  
		`$ /etc/init.d/mysql restart`  




	
