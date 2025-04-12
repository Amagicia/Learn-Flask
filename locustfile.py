# from locust import HttpUser, task, between


# class WebsiteUser(HttpUser):
#     wait_time = between(1, 3)  # Each user waits 1 to 3 seconds between tasks

#     @task
#     def home(self):
#         self.client.get("/")  # this hits http://localhost:5000/

#     @task(3)
#     def contact(self):
#         self.client.get("/contact")

#     @task(1)
#     def login(self):
#         self.client.post("/login", data={"username": "test", "password": "123"})
