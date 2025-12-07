import unittest
import uuid
from app import create_app, mongo

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a temporary test client before each test runs."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Generate a random test user
        self.test_username = f"test_user_{uuid.uuid4().hex[:8]}"
        self.test_password = "testpassword123"

    def tearDown(self):
        """Clean up after tests."""
        mongo.db.users.delete_one({"username": self.test_username})
        self.app_context.pop()

    def test_signup(self):
        """Test if a new user can sign up successfully."""
        response = self.client.post('/signup', data={
            'username': self.test_username,
            'password': self.test_password,
            'role': 'analyst'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

    def test_login(self):
        """Test if the user can log in."""
        # Create user
        self.client.post('/signup', data={
            'username': self.test_username,
            'password': self.test_password,
            'role': 'analyst'
        })

        # Login
        response = self.client.post('/signin', data={
            'username': self.test_username,
            'password': self.test_password
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_logout(self):
        """Test logout functionality."""
        # Login first
        self.client.post('/signup', data={'username': self.test_username, 'password': self.test_password})
        self.client.post('/signin', data={'username': self.test_username, 'password': self.test_password})

        # Logout (FIXED URL HERE: Changed /auth/logout to /logout)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
