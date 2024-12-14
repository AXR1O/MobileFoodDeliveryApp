import unittest
# Red Phase

class TestWishlist(unittest.TestCase):
    def test_add_to_wishlist(self):
        # 测试添加到愿望清单
        pass

    def test_remove_from_wishlist(self):
        # 测试从愿望清单移除
        pass

# Green Phase
class Wishlist1:
    def __init__(self):
        self.items = []

    def add_to_wishlist(self, item):
        if item not in self.items:
            self.items.append(item)

    def remove_from_wishlist(self, item):
        if item in self.items:
            self.items.remove(item)


# Refactor Phase
class Wishlist2:
    def __init__(self):
        self.items = set()  # 使用集合避免重复

    def add_to_wishlist(self, item):
        self.items.add(item)

    def remove_from_wishlist(self, item):
        self.items.discard(item)  # 使用discard避免删除时抛出异常