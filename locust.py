from locust import HttpUser, TaskSet, task

class MyTaskSet(TaskSet):
	@task
	def get_user_list(self):
		self.client.get("/api/users")

	@task
	def get_user_list(self):
		self.client.get("/api/users/2")

class MyLocust(HttpUser):
	task_set = MyTaskSet


