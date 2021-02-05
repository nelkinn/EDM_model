from locust import HttpUser, HttpLocust, TaskSet, task, between


class MyUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        response = self.client.get('/admin/login/')
        csrftoken = response.cookies['csrftoken']
        self.client.post("/admin/login/", {'username': 'username', 'password': 'password'},
                         headers={'X-CSRFToken': csrftoken})

    @task
    def about(self):
        self.client.get("/documents/")
        self.client.get("/documents/2/")

