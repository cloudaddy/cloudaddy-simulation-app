import jinja2
import os
import requests
from flask import render_template, send_from_directory, request
from locust import HttpLocust, TaskSet, task, web

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
my_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(os.path.join(PROJECT_ROOT, 'templates')),
    web.app.jinja_loader,
])
web.app.jinja_loader = my_loader


# override the locust web routes
@web.app.route('/public/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'public'), path)


numberOfJobsPerUser = 0


@web.app.route("/cloudaddy")
def cloudaddy():
    return render_template("index.html")


@web.app.route("/start-testing", methods=['POST'])
def start_testing():
    numberOfConcurrentUsers = request.form['numberOfConcurrentUsers']
    os.environ['numberOfJobsPerUser'] = request.form['numberOfJobsPerUser']
    os.environ['daysDatesBack'] = request.form['daysDatesBack']

    locust_parameters = {
        "locust_count": numberOfConcurrentUsers,
        "hatch_rate": numberOfConcurrentUsers
    }

    # starting locust by making a http request to the service
    response = requests.post('http://localhost:8089/swarm', data=locust_parameters)
    return "success!"


@web.app.route("/stop-testing", methods=['GET'])
def stop_testing():
    response = requests.get('http://localhost:8089/stop')
    return "success!"


class WebsiteTasks(TaskSet):
    def on_start(self):
        # get random valid usernames and passwords
        with self.client.post("/login", {
            "username": "user",
            "password": "user"
        }, catch_response=True)as response:
            print "Response status code of login page:", response.status_code
            result = response.status_code
            if "<title>Cloudaddy</title>"  in response.content:
                print "Logged in successfully"
            else:
                #print "Invalid credentials"
                response.failure("Invalid credentials")

    @task
    def index(self):
        with self.client.get("/index", catch_response=True) as response:
            # print response.content
            print "Response status code of index page:", response.status_code
            if "<title>generate reports</title>" in response.content:
                print "Entered Index Page"
            else:
               response.failure("valid credentials is required to access the system")

    @task
    def report(self):
        with self.client.post("/report", {
            "prod": "7",
            "count": os.environ['numberOfJobsPerUser'],
            "daysOld": os.environ['daysDatesBack']
        }, catch_response=True) as response:
            if "<title>generate reports</title>" in response.content:
                print "Reported Generated"
            else:
                response.failure("Report was not generated")
    @task
    def home_page(self):
        with self.client.get("/", catch_response=True) as response:
            print "Response status code of root page:", response.status_code
            result = response.status_code

            if result != 200:
                response.failure("Not yet been logged out")

    @task
    def download(self):
        self.client.get("/download?report=108")



class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000
