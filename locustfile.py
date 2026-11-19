from locust import HttpUser, task, between

class GramSetuUserBehavior(HttpUser):
    wait_time = between(1, 3)

    @task(4)
    def view_homepage(self):
        self.client.get("/")

    @task(3)
    def view_projects(self):
        self.client.get("/development/")

    @task(2)
    def view_schemes(self):
        self.client.get("/schemes/")

    @task(2)
    def view_services(self):
        self.client.get("/services/")

    @task(2)
    def view_map(self):
        self.client.get("/map/")

    @task(2)
    def view_budget(self):
        self.client.get("/budget/")

    @task(1)
    def api_projects_list(self):
        self.client.get("/api/projects/")

    @task(1)
    def api_infrastructure_markers(self):
        self.client.get("/api/infrastructure/")

    @task(1)
    def health_check(self):
        self.client.get("/health/")
