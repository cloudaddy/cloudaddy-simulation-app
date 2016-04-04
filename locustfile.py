import jinja2
import os
import requests
from flask import render_template, request
from locust import HttpLocust, TaskSet, task, web

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
my_loader = jinja2.ChoiceLoader([
    jinja2.FileSystemLoader(os.path.join(PROJECT_ROOT, 'templates')),
    web.app.jinja_loader,
])
web.app.jinja_loader = my_loader

# override the locust web routes
@web.app.route("/cloudaddy")
def cloudaddy():
    return render_template("index.html")

@web.app.route("/start-testing", methods=['POST'])
def start_testing():
    numberOfConcurrentUsers = request.form['numberOfConcurrentUsers']
    numberOfJobsPerUser = request.form['numberOfJobsPerUser']

    # TODO: set the custom parameters via environment variables
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
        self.client.post("/login", {
            "username": "user",
            "password": "password"
        })

    @task
    def index(self):
        with self.client.get("/hello", catch_response=True) as response:

            result = response.content.find("Hello Page")

            if result == -1:
                response.failure("No access!!!!")

    @task
    def about(self):
        self.client.get("/logout")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000
