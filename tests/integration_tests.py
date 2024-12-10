import unittest
from unittest import mock

from Order_Placement import (Cart, CartItem, OrderPlacement, PaymentFailedException,
                             PaymentMethod, RestaurantMenu, UserProfile)


class TestOrderPlacementIntegration(unittest.TestCase):
    def setUp(self):
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"])
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.order = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)
        self.payment_method = PaymentMethod()

    def test_full_order_process_success(self):
        """
        Test the complete order process, including adding items, validating orders, checking out,
        and successful payment confirmation of orders.
        """
        # Add items to cart
        self.cart.add_item("Burger", 8.99, 2)
        self.cart.add_item("Pizza", 12.99, 1)

        # Verify the order
        validation_result = self.order.validate_order()
        self.assertTrue(validation_result["success"])
        self.assertEqual(validation_result["message"], "Order is valid")

        # Check out
        checkout_result = self.order.proceed_to_checkout()
        expected_checkout_result = {
            "items": [{"name": "Burger", "quantity": 2, "subtotal": 17.98}, {"name": "Pizza", "quantity": 1, "subtotal": 12.99}],
            "total_info": {"subtotal": 30.97, "tax": 3.1, "delivery_fee": 5.0, "total": 39.07},
            "delivery_address": "123 Main St"
        }
        self.assertEqual(checkout_result["items"], expected_checkout_result["items"])
        self.assertEqual(checkout_result["delivery_address"], expected_checkout_result["delivery_address"])
        self.assertAlmostEqual(checkout_result["total_info"]["subtotal"], expected_checkout_result["total_info"]["subtotal"], places=2)
        self.assertAlmostEqual(checkout_result["total_info"]["tax"], expected_checkout_result["total_info"]["tax"], places=2)
        self.assertAlmostEqual(checkout_result["total_info"]["total"], expected_checkout_result["total_info"]["total"], places=2)

        # Simulate successful payment and confirm the order
        with mock.patch.object(self.payment_method, 'process_payment', return_value=True):
            confirm_result = self.order.confirm_order(self.payment_method)
            self.assertTrue(confirm_result["success"])
            self.assertEqual(confirm_result["message"], "Order confirmed")
            self.assertEqual(confirm_result["order_id"], "ORD123456")

    def test_order_process_with_unavailable_item(self):
        """
        Testing the order flow when adding unavailable items should fail during the validation order phase.
        """
        # Add unavailable items to cart
        self.cart.add_item("Pasta", 15.99, 1)

        # Verify the order
        validation_result = self.order.validate_order()
        self.assertFalse(validation_result["success"])
        self.assertEqual(validation_result["message"], "Pasta is not available")

    def test_order_process_with_empty_cart(self):
        """
        The order flow when testing an empty shopping cart should fail during the order validation phase.
        """
        # Verify order directly (cart is empty)
        validation_result = self.order.validate_order()
        self.assertFalse(validation_result["success"])
        self.assertEqual(validation_result["message"], "Cart is empty")

    def test_order_process_with_failed_payment(self):
        """
        To test the order flow when a payment fails,
        throw a PaymentFailedException during the order confirmation phase.
        """
        # Add items to cart
        self.cart.add_item("Burger", 8.99, 1)

        # Simulate payment failure and confirm the order
        with mock.patch.object(self.payment_method, 'process_payment', return_value=False):
            with self.assertRaises(PaymentFailedException):
                self.order.confirm_order(self.payment_method)

    def test_add_item_with_invalid_price(self):
        """
        To test if the price is not greater than 0 when adding an item, raise a ValueError.
        """
        with self.assertRaises(ValueError):
            self.cart.add_item("InvalidItem", 0, 1)

    def test_add_item_with_invalid_quantity(self):
        """
        To test if the number of items added is less than 0, a ValueError should be raised.
        """
        with self.assertRaises(ValueError):
            self.cart.add_item("InvalidItem", 10, -1)

    def test_add_item_with_empty_name(self):
        """
        To test if the name of the item is empty when you add it, raise a ValueError.
        """
        with self.assertRaises(ValueError):
            self.cart.add_item("", 10, 1)

    def test_update_item_quantity_with_invalid_quantity(self):
        """
        To test if the number of updated items is less than 0, ValueError should be raised.
        """
        self.cart.add_item("Burger", 8.99, 1)
        with self.assertRaises(ValueError):
            self.cart.update_item_quantity("Burger", -1)

    def test_remove_nonexistent_item(self):
        """
        Test to remove items that do not exist, should return the corresponding prompt message.
        """
        result = self.cart.remove_item("NonexistentItem")
        self.assertEqual(result, "NonexistentItem not found in cart")

    def test_calculate_total_with_no_items(self):
        """
        The test calculates the total price of the empty shopping cart and should
        return the correct default value (such as the total price is 0, etc.).
        """
        total_info = self.cart.calculate_total()
        expected_total_info = {"subtotal": 0, "tax": 0, "delivery_fee": 5.0, "total": 5.0}
        self.assertEqual(total_info, expected_total_info)

    def test_confirm_order_with_zero_amount_payment(self):
        """
        Test the order confirmation when the payment amount is 0, and the corresponding result should be
        returned according to the processing logic of the PaymentMethod (assuming the payment fails).
        """
        self.cart.add_item("Burger", 8.99, 1)
        with mock.patch.object(self.payment_method, 'process_payment', return_value=False):
            with self.assertRaises(PaymentFailedException):
                self.order.confirm_order(self.payment_method)


if __name__ == "__main__":
    unittest.main()