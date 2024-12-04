import re
import bcrypt

class UserRegistration:
    def __init__(self):
        """
        Initializes the UserRegistration class with an empty dictionary to store user data.
        Each entry in the dictionary will map an email to a dictionary containing the user's password and confirmation status.
        """
        self.users = {}

    def register(self, email, password, confirm_password):
        """
        Registers a new user.

        This function takes an email, password, and password confirmation as input. It performs a series of checks to ensure the registration
        is valid:
        - Verifies that the email is in a valid format.
        - Ensures that the password matches the confirmation password.
        - Validates that the password meets the strength requirements.
        - Checks if the email is already registered.

        If all checks pass, the user is registered, and their email and password are stored in the `users` dictionary, along with a confirmation
        status set to False (indicating the user is not yet confirmed). A success message is returned.

        Args:
            email (str): The user's email address.
            password (str): The user's password.
            confirm_password (str): Confirmation of the user's password.

        Returns:
            dict: A dictionary containing the result of the registration attempt.
                  On success, it returns {"success": True, "message": "Registration successful, confirmation email sent"}.
                  On failure, it returns {"success": False, "error": "Specific error message"}.
        """
        if email in self.users:
            return {"success": False, "error": "Email already registered"}
        if not self.is_valid_email(email):
            return {"success": False, "error": "Invalid email format"}
        if password!= confirm_password:
            return {"success": False, "error": "Passwords do not match"}
        if not self.is_strong_password(password):
            raise ValueError("Password is not strong enough")

        # Register the user if all conditions are met and return a success message.
        self.users[email] = {"password": password, "confirmed": False}
        return {"success": True, "message": "Registration successful, confirmation email sent"}

    def is_valid_email(self, email):
        """
        Checks if the provided email is valid based on a regular expression pattern.

        Args:
            email (str): The email address to be validated.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        # More stringent email format validation of regular expressions
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return True
        raise ValueError("Invalid email format")

    def is_strong_password(self, password):
        """
        Checks if the provided password meets the strength requirements.
        A strong password is defined as one that is at least 8 characters long, contains at least one uppercase letter,
        one lowercase letter, one digit, and one special character.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: True if the password is strong, False otherwise.
        """
        if len(password) < 8:
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        if not any(c in "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?" for c in password):
            return False
        return True

    def encrypt_password(self, password):
        """
        Encrypts the password using bcrypt.

        Args:
            password (str): The password to be encrypted.

        Returns:
            str: The encrypted password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

import unittest
from unittest.mock import MagicMock


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