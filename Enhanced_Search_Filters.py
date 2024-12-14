import unittest
# Red Phase

class TestEnhancedSearchFilters(unittest.TestCase):
    def test_search_by_cuisine(self):
        # 测试按菜系搜索
        pass

    def test_search_by_rating(self):
        # 测试按评分搜索
        pass

    def test_search_by_delivery_speed(self):
        # 测试按配送速度搜索
        pass

# Green Phase
class Restaurant:
    def __init__(self, name, cuisine, rating, delivery_speed):
        self.name = name
        self.cuisine = cuisine
        self.rating = rating
        self.delivery_speed = delivery_speed

class RestaurantSearch1:
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def search_by_cuisine(self, cuisine):
        return [r for r in self.restaurants if r.cuisine == cuisine]

    def search_by_rating(self, min_rating):
        return [r for r in self.restaurants if r.rating >= min_rating]

    def search_by_delivery_speed(self, delivery_speed):
        return [r for r in self.restaurants if r.delivery_speed == delivery_speed]


# Refactor Phase
class RestaurantSearch2:
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def search(self, **filters):
        results = self.restaurants
        if 'cuisine' in filters:
            results = [r for r in results if r.cuisine == filters['cuisine']]
        if 'min_rating' in filters:
            results = [r for r in results if r.rating >= filters['min_rating']]
        if 'delivery_speed' in filters:
            results = [r for r in results if r.delivery_speed == filters['delivery_speed']]
        return results

