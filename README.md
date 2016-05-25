Repo for Pycon 2016 Tutorial The Fellowship of The Data

For best results, follow instructions below :)

0. Start docker, note the docker IP as YOUR_DOCKER_IP

1. Get the LAMP stack for hosting tutorial files from Docker:  
	`$ docker run -t -i -p 3306:3306 --net=bridge --name=pycon2016_lamp  gizm00/pycon2016_lamp /bin/bash`  

2. In the pycon2016_lamp container you just created, note the IP address by running:  
	`$ ifconfig | grep 'inet addr'`  
	the first line will give you the IP for the container. This is the LAMP_IP  

3. Execute the startup script in the pycon2016_lamp container to setup the mysql database  
	`$ lamp_startup.sh`  

Your LAMP container should now be ready to serve files for the tutorial  

1. Clone the tutorial repo to your local machine  
	```
	$ git clone https://github.com/gizm00/pycon2016.git
	$ cd pycon2016/notebooks
	```

In the pycon2016/notebooks directory, start the tutorial container  

1. Get the tutorial image from Docker:  
	`$ docker run --rm -it --net=bridge -p 8888:8888 --name=pycon2016_notebooks -v "$(pwd):/home/notebooks" gizm00/pycon2016`  

2. In the pycon2016_notebooks container execute the startup script to install the pymysql driver and start the notebook server:  
	`$ start-notebook.sh`  

3. Navigate to http://YOUR_DOCKER_IP:8888/ to see the notebook tree

At this point youre ready to run the test notebook to verify your setup

1. At http://YOUR_DOCKER_IP:8888/ find the config.py file

2. Update config.py with the values you noted above:
	LAMP_IP = your LAMP_IP
	HOST_IP = YOUR_DOCKER_IP

3. Open the test_notebook in the jupyter tree and run the notebook. The resulting plot should be a map of Oregon, hover over points to see campground name and telephone (where available)

