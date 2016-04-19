import jinja2
import os
import requests
from flask import render_template, send_from_directory, request
from locust import HttpLocust, TaskSet, task, web
import random


USER_CREDENTIALS = [
    ("user4", "user4"),
    ("user3", "user3"),
    ("user24", "user24"),
    ("user5", "user5"),
    ("user22", "user22"),
    ("user7", "user7"),
    ("user38", "user38"),
    ("user9", "user9"),
    ("user10", "user10"),
    ("user11", "user11"),
    ("user20", "user20"),
    ("user19", "user19"),
    ("user37", "user37"),
    ("user40", "user40"),
    ("user5", "user5"),
    ("user6", "user6"),
    ("user13", "user13"),
    ("user21", "user21"),
]

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

        credentials = random.choice(USER_CREDENTIALS)
        #print(credentials[0],credentials[1])
        response = self.client.post("/login", {
            "username": credentials[0],
            "password": credentials[1]
        }, catch_response=True, verify=False)
            #print "Response status code of login page:", response.status_code

        if "<title>generate reports</title>" in response.content:
            print "Logged in successfully"
        else:
            print response.content
            response.failure("Invalid credentials")

    @task
    def index(self):
        response = self.client.get("/index", catch_response=True, verify=False)
            # print response.content
        print "Response status code of index page:", response.status_code

        if "<title>generate reports</title>" in response.content:
            print "Entered Index Page"
        else:
            response.failure("valid credentials is required to access the system")

    @task
    def report(self):
        response = self.client.post("/report", {
            "prod": "1",
            "count": os.environ['numberOfJobsPerUser'],
            "daysOld": os.environ['daysDatesBack']
        }, catch_response=True, verify=False)
        if "<title>generate reports</title>" in response.content:
            print "Reported Generated"
        else:
            response.failure("Report was not generated")

    @task
    def home_page(self):
        response = self.client.get("/", catch_response=True, verify=False)
        print "Response status code of root page:", response.status_code
        result = response.status_code

        if result != 200:
            response.failure("Not yet been logged out")

    @task
    def download(self):
        self.client.get("/download?report=108", verify=False)


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000
