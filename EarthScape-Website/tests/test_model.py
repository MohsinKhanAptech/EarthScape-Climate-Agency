import unittest
from app import create_app
from app.models.ml_engine import predict_temperature, get_all_cities

class MLModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_get_cities(self):
        """Test if the system can load the list of cities."""
        cities = get_all_cities()
        self.assertIsInstance(cities, list)
        self.assertTrue(len(cities) > 0, "City list should not be empty")
        self.assertIn("New York", cities, "New York should be in the city list")

    def test_prediction_output(self):
        """Test if the model returns a valid float prediction."""
        # Test Case: New York, Year 2030, Month 7 (July)
        prediction = predict_temperature("New York", 2030, 7)
        
        self.assertIsNotNone(prediction, "Prediction should not be None")
        self.assertIsInstance(prediction, float, "Prediction should be a float number")
        
        # Sanity check: Temp should be reasonable (e.g., between -50 and 60 C)
        self.assertTrue(-50 < prediction < 60, "Temperature prediction is out of realistic bounds")

    def test_invalid_city(self):
        """Test how the model handles a non-existent city."""
        prediction = predict_temperature("Atlantis_Fake_City", 2030, 1)
        self.assertIsNone(prediction, "Model should return None for unknown cities")

if __name__ == '__main__':
    unittest.main()
