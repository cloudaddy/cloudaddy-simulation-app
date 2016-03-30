from locust import HttpLocust, TaskSet, task

class WebsiteTasks(TaskSet):
    def on_start(self):
        self.client.post("/login", {
            "username": "user",
            "password": "password"
        })

    @task
    def index(self):
        self.client.get("/hello")

    @task
    def about(self):
        self.client.get("/logout")

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000
