from locust import HttpUser, task, between
from locust.exception import StopUser
import json


class BlogUser(HttpUser):
    """
    Simulates a user interacting with a blog application API for performance testing.
    """

    wait_time = between(1, 3)

    def on_start(self):
        """
        Log in the user and set the Authorization header before tasks begin.
        """
        credentials = {"email": "Admin@gmail.com", "password": "Admin@1234"}

        with self.client.post(
            "/accounts/api/v1/jwt/create/",
            data=json.dumps(credentials),
            headers={"Content-Type": "application/json"},
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                access_token = response.json().get("access")
                if not access_token:
                    response.failure("No access token returned")
                    raise StopUser()
                self.client.headers.update({"Authorization": f"Bearer {access_token}"})
            else:
                response.failure(f"Login failed: {response.status_code}")
                raise StopUser()

    @task(3)
    def view_posts(self):
        """Simulates a GET request to fetch blog posts."""
        self.client.get("/blog/api/v1/posts/")

    @task(1)
    def view_categories(self):
        """Simulates a GET request to fetch blog categories."""
        self.client.get("/blog/api/v1/categories/")
