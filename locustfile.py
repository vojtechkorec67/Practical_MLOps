from locust import HttpUser, task, between
import random

class AddServiceUser(HttpUser):
    """Load test for the add API endpoint"""
    wait_time = between(1, 3)
    
    @task(3)
    def add_numbers(self):
        """Test the /add endpoint"""
        x = random.uniform(1, 100)
        y = random.uniform(1, 100)
        self.client.get(f"/add?x={x}&y={y}")
    
    @task(1)
    def health_check(self):
        """Test the /health endpoint"""
        self.client.get("/health")
    
    def on_start(self):
        """Called when a simulated user starts"""
        pass
