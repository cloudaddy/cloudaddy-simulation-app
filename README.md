cloudaddy-simulation-app
========================

How to run
----------

1.	Make sure you have ***Python 2.7*** installed
2.	Change directory to the root of this project in your terminal/cmd
3.	Use ***pip install -r requirements.txt*** to install locust
4.	Use ***locust -f locustfile.py --host http://localhost:8080*** to boot locust, change the --host param accordingly if the website is located in other url
5.	Go to your browser and visit ***http://localhost:8089***
6.	Start torturing the web server~
