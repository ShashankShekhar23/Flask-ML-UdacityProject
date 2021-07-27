from locust import HttpUser, TaskSet, task

class MyTaskSet(TaskSet):
	@task
	def get_user_list(self):
		self.client.get("/api/users")

	@task
	def post_user_list(self):
		self.client.post("/api/users/2")

class MyLocust(HttpUser):
	task_set = MyTaskSet
	min_wait = 5000
	max_wait = 10000
	host = "https://flaskmludacityproject.azurewebsites.net"
