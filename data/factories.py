"""
Data Factories
Factory classes for generating test data.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import random
import string


@dataclass
class UserData:
    """User data model for testing."""
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "user"


@dataclass
class FormData:
    """Form data model for testing."""
    email: str
    message: str
    subject: Optional[str] = None
    name: Optional[str] = None


class UserFactory:
    """Factory for generating user test data."""
    
    @staticmethod
    def create_user(
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: str = "Test123!",
        role: str = "user"
    ) -> UserData:
        """
        Create a user with test data.
        
        Args:
            username: Username (auto-generated if not provided)
            email: Email (auto-generated if not provided)
            password: Password (default: Test123!)
            role: User role (default: user)
            
        Returns:
            UserData instance
        """
        if username is None:
            username = f"user_{UserFactory._random_string(8)}"
        
        if email is None:
            email = f"{username}@example.com"
        
        return UserData(
            username=username,
            email=email,
            password=password,
            role=role
        )
    
    @staticmethod
    def create_admin_user() -> UserData:
        """
        Create an admin user.
        
        Returns:
            UserData instance with admin role
        """
        return UserFactory.create_user(role="admin")
    
    @staticmethod
    def _random_string(length: int = 10) -> str:
        """Generate random string."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class FormFactory:
    """Factory for generating form test data."""
    
    @staticmethod
    def create_form_data(
        email: Optional[str] = None,
        message: Optional[str] = None,
        subject: Optional[str] = None,
        name: Optional[str] = None
    ) -> FormData:
        """
        Create form data for testing.
        
        Args:
            email: Email address
            message: Message text
            subject: Subject line
            name: Name field
            
        Returns:
            FormData instance
        """
        if email is None:
            email = f"test_{FormFactory._random_string(5)}@example.com"
        
        if message is None:
            message = f"Test message generated at {datetime.now().isoformat()}"
        
        return FormData(
            email=email,
            message=message,
            subject=subject,
            name=name
        )
    
    @staticmethod
    def create_invalid_email_data() -> FormData:
        """
        Create form data with invalid email.
        
        Returns:
            FormData instance with invalid email
        """
        invalid_emails = ["notanemail", "@example.com", "test@", "test"]
        return FormData(
            email=random.choice(invalid_emails),
            message="Test message"
        )
    
    @staticmethod
    def _random_string(length: int = 10) -> str:
        """Generate random string."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

