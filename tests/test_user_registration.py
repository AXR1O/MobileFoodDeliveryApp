import unittest
from unittest.mock import MagicMock
from User_Registration import UserRegistration


class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by creating an instance of the UserRegistration class.
        This instance will be used across all test cases.
        """
        self.registration = UserRegistration()

    def test_successful_registration(self):
        """
        Test case for successful user registration.
        It verifies that a valid email and matching strong password results in successful registration.
        """
        result = self.registration.register("user@example.com", "Password123!", "Password123!")
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Registration successful, confirmation email sent")

    def test_invalid_email_format(self):
        """
        Test case for invalid email format.
        It verifies that attempting to register with an incorrectly formatted email results in an error.
        """
        with self.assertRaises(ValueError) as context:
            self.registration.register("invalid_email", "Password123", "Password123")
        self.assertEqual(str(context.exception), "Invalid email format")

    def test_password_mismatch(self):
        """
        Test case for password mismatch.
        It verifies that when the password and confirmation password do not match, registration fails.
        """
        result = self.registration.register("user@example.com", "Password123", "DifferentPassword")
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Passwords do not match")

    def test_weak_password(self):
        """
        Test case for weak password.
        It verifies that a password not meeting the strength requirements results in an error.
        """
        with self.assertRaises(ValueError) as context:
            self.registration.register("user@example.com", "weak", "weak")
        self.assertEqual(str(context.exception), "Password is not strong enough")

    def test_email_already_registered(self):
        """
        Test case for duplicate email registration.
        It verifies that attempting to register an email that has already been registered results in an error.
        """
        self.registration.register("user@example.com", "Password123!", "Password123!")
        result = self.registration.register("user@example.com", "Password123!", "Password123!")
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Email already registered")

    def test_password_encryption(self):
        """
        Test case for password encryption.
        It verifies that the password is encrypted correctly before being stored.
        """
        password = "Password123!"
        hashed_password = self.registration.encrypt_password(password)
        # Check that the encrypted password matches the expected encryption format (bcrypt encrypted password format)
        self.assertTrue(hashed_password.startswith("$2b$"))


if __name__ == '__main__':
    unittest.main()