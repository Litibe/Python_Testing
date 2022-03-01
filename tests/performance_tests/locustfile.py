from locust import HttpUser, task


class ServerPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")
