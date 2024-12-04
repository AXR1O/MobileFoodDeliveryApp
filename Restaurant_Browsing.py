class RestaurantBrowsing:
    """
    A class for browsing restaurants in a database based on various criteria like cuisine type, location, and rating.

    Attributes:
        database (RestaurantDatabase): An instance of RestaurantDatabase that holds restaurant data.
    """

    def __init__(self, database):
        """
        Initialize RestaurantBrowsing with a reference to a restaurant database.

        Args:
            database (RestaurantDatabase): The database object containing restaurant information.
        """
        self.database = database

    def search_by_cuisine(self, cuisine_type):
        """
        Search for restaurants based on their cuisine type.

        Args:
            cuisine_type (str): The type of cuisine to filter by (e.g., "Italian").

        Returns:
            list: A list of restaurants that match the given cuisine type.

        Raises:
            ValueError: If the cuisine_type is empty or None.
        """
        if not cuisine_type:
            raise ValueError("Cuisine type cannot be empty or None.")
        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['cuisine'].lower() == cuisine_type.lower()]

    def search_by_location(self, location):
        """
        Search for restaurants based on their location.

        Args:
            location (str): The location to filter by (e.g., "Downtown").

        Returns:
            list: A list of restaurants that are located in the specified area.

        Raises:
            ValueError: If the location is empty or None.
        """
        if not location:
            raise ValueError("Location cannot be empty or None.")
        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['location'].lower() == location.lower()]

    def search_by_rating(self, min_rating):
        """
        Search for restaurants based on their minimum rating.

        Args:
            min_rating (float): The minimum acceptable rating to filter by (e.g., 4.0).

        Returns:
            list: A list of restaurants that have a rating greater than or equal to the specified rating.

        Raises:
            ValueError: If the min_rating is not within the valid range (0 to 5).
        """
        if not (0 <= min_rating <= 5):
            raise ValueError("Minimum rating must be between 0 and 5.")
        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['rating'] >= min_rating]

    def search_by_filters(self, cuisine_type=None, location=None, min_rating=None):
        """
        Search for restaurants based on multiple filters: cuisine type, location, and/or rating.

        Args:
            cuisine_type (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            min_rating (float, optional): The minimum acceptable rating to filter by.

        Returns:
            list: A list of restaurants that match all specified filters.

        Raises:
            ValueError: If any of the filter parameters are invalid.
        """
        results = self.database.get_restaurants()
        valid_cuisines = {restaurant['cuisine'].lower() for restaurant in results}
        valid_locations = {restaurant['location'].lower() for restaurant in results}

        if cuisine_type and cuisine_type.lower() not in valid_cuisines:
            raise ValueError(f"Invalid cuisine type: {cuisine_type}")
        if location and location.lower() not in valid_locations:
            raise ValueError(f"Invalid location: {location}")
        if min_rating is not None and not (0 <= min_rating <= 5):
            raise ValueError(f"Invalid minimum rating: {min_rating}")

        if cuisine_type:
            results = [restaurant for restaurant in results
                       if restaurant['cuisine'].lower() == cuisine_type.lower()]
        if location:
            results = [restaurant for restaurant in results
                       if restaurant['location'].lower() == location.lower()]
        if min_rating is not None:
            results = [restaurant for restaurant in results
                       if restaurant['rating'] >= min_rating]

        return results


class RestaurantDatabase:
    """
    A simulated in-memory database that stores restaurant information.

    Attributes:
        restaurants (list): A list of dictionaries, where each dictionary represents a restaurant with
                            fields like name, cuisine, location, rating, price range, and delivery status.
    """

    def __init__(self):
        """
        Initialize the RestaurantDatabase with a predefined set of restaurant data.
        """
        self.restaurants = [
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown", "rating": 4.5,
             "price_range": "$$", "delivery": True},
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": 4.8,
             "price_range": "$$$", "delivery": False},
            {"name": "Burger King", "cuisine": "Fast Food", "location": "Uptown", "rating": 4.0,
             "price_range": "$", "delivery": True},
            {"name": "Taco Town", "cuisine": "Mexican", "location": "Downtown", "rating": 4.2,
             "price_range": "$", "delivery": True},
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "Uptown", "rating": 3.9,
             "price_range": "$$", "delivery": True}
        ]

    def get_restaurants(self):
        """
        Retrieve the list of restaurants in the database.

        Returns:
            list: A list of dictionaries, where each dictionary contains restaurant information.
        """
        return self.restaurants


class RestaurantSearch:
    """
    A class that interfaces with RestaurantBrowsing to perform restaurant searches based on user input.

    Attributes:
        browsing (RestaurantBrowsing): An instance of RestaurantBrowsing used to perform searches.
    """

    def __init__(self, browsing):
        """
        Initialize the RestaurantSearch with a reference to a RestaurantBrowsing instance.

        Args:
            browsing (RestaurantBrowsing): An instance of the RestaurantBrowsing class.
        """
        self.browsing = browsing

    def search_restaurants(self, cuisine=None, location=None, rating=None):
        """
        Search for restaurants using multiple optional filters: cuisine, location, and rating.

        Args:
            cuisine (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            rating (float, optional): The minimum rating to filter by.

        Returns:
            list: A list of restaurants that match the provided search criteria.
        """
        results = self.browsing.search_by_filters(cuisine_type=cuisine, location=location, min_rating=rating)
        return results


# Unit tests for RestaurantBrowsing class
import unittest


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
        self.assertEqual(len(results), 5)  # All restaurants have a rating greater than 0, so all restaurants are returned
        results = self.browsing.search_by_rating(5)
        self.assertEqual(len(results), 0)  # Update expected result is 0 because there are no restaurants with a rating of 5

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