import unittest

from Restaurant_Browsing import RestaurantBrowsing, RestaurantDatabase


class TestRestaurantBrowsing(unittest.TestCase):
    """
    Unit tests for the RestaurantBrowsing class, testing various search functionalities.
    """

    def setUp(self):
        """
        Set up the test case by initializing a RestaurantDatabase and RestaurantBrowsing instance.
        """
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

    def test_search_by_cuisine(self):
        """
        Test searching for restaurants by cuisine type.
        """
        # Normal condition test
        results = self.browsing.search_by_cuisine("Italian")
        self.assertEqual(len(results), 2)
        self.assertTrue(all([restaurant['cuisine'] == "Italian" for restaurant in results]))

        # Anomaly test
        with self.assertRaises(ValueError):
            self.browsing.search_by_cuisine("")
        with self.assertRaises(ValueError):
            self.browsing.search_by_cuisine(None)

    def test_search_by_location(self):
        """
        Test searching for restaurants by location.
        """
        # Normal condition test
        results = self.browsing.search_by_location("Downtown")
        self.assertEqual(len(results), 2)
        self.assertTrue(all([restaurant['location'] == "Downtown" for restaurant in results]))

        # Anomaly test
        with self.assertRaises(ValueError):
            self.browsing.search_by_location("")
        with self.assertRaises(ValueError):
            self.browsing.search_by_location(None)

    def test_search_by_rating(self):
        """
        Test searching for restaurants by minimum rating.
        """
        # Normal condition test
        results = self.browsing.search_by_rating(4.0)
        self.assertEqual(len(results), 4)
        self.assertTrue(all([restaurant['rating'] >= 4.0 for restaurant in results]))

        # Boundary value test
        results = self.browsing.search_by_rating(0)
        self.assertEqual(len(results), 5)
        results = self.browsing.search_by_rating(5)
        self.assertEqual(len(results), 0)

        # Anomaly test
        with self.assertRaises(ValueError):
            self.browsing.search_by_rating(-0.1)
        with self.assertRaises(ValueError):
            self.browsing.search_by_rating(5.1)

    def test_search_by_filters(self):
        """
        Test searching for restaurants by multiple filters (cuisine type, location, and minimum rating).
        """
        # Normal condition test
        results = self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=4.0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Italian Bistro")

        # Multi-condition combination test
        results = self.browsing.search_by_filters(cuisine_type="Fast Food", location="Uptown", min_rating=4.0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Burger King")

        # The filtering order does not affect the result test
        results1 = self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=4.0)
        results2 = self.browsing.search_by_filters(location="Downtown", cuisine_type="Italian", min_rating=4.0)
        self.assertEqual(results1, results2)

        # All conditions do not meet the test (including invalid cuisine type, now expect to throw an exception)
        with self.assertRaises(ValueError):
            self.browsing.search_by_filters(cuisine_type="Chinese", location="Suburb", min_rating=5.5)

        # Abnormal condition test (other invalid parameter condition)
        with self.assertRaises(ValueError):
            self.browsing.search_by_filters(cuisine_type="Italian", location="Invalid Location", min_rating=4.0)
        with self.assertRaises(ValueError):
            self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=-1)


if __name__ == '__main__':
    unittest.main()