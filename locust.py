from locust import HttpLocust, TaskSet, task

class MyTaskSet(TaskSet):
	@task
	def get_user_list(self):
		self.client.get("/api/users")

	@task
	def get_user_list(self):
		self.client.get("/api/users/2")

class MyLocust(HttpLocust):
	task_set = MyTaskSet

