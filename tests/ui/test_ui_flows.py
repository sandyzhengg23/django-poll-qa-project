import re
import time

BASE_URL = "http://127.0.0.1:8000"


def unique_user():
    timestamp = int(time.time() * 1000)
    return {
        "username": f"uitest{timestamp}",
        "email": f"uitest{timestamp}@example.com",
        "password": "password123",
    }


def register_user(page, user):
    page.goto(f"{BASE_URL}/accounts/register/")

    page.locator("#id_username").fill(user["username"])
    page.locator("#id_email").fill(user["email"])
    page.locator("#id_password1").fill(user["password"])
    page.locator("#id_password2").fill(user["password"])

    page.get_by_role("button", name=re.compile("sign up", re.I)).click()


def login_user(page, user):
    page.goto(f"{BASE_URL}/accounts/login/")

    page.get_by_placeholder("Enter Username").fill(user["username"])
    page.get_by_placeholder("Password").fill(user["password"])

    page.get_by_role("button", name=re.compile("login", re.I)).click()


def test_get_started_navigates_to_login_page(page):
    """Verify that Get Started takes a visitor from the home page to the login page."""
    page.goto(BASE_URL)

    page.get_by_role("button", name=re.compile("get started", re.I)).click()

    assert page.get_by_role("heading", name=re.compile("login", re.I)).is_visible()


def test_register_new_user(page):
    """Verify that a new user can register with valid account information."""
    user = unique_user()

    register_user(page, user)

    assert page.get_by_text(re.compile("thanks for registering", re.I)).is_visible()


def test_login_with_valid_credentials(page):
    """Verify that a registered user can log in and access authenticated navigation."""
    user = unique_user()

    register_user(page, user)
    login_user(page, user)

    assert page.get_by_role("link", name=re.compile("my polls", re.I)).is_visible()
    assert page.get_by_role("link", name=re.compile("logout", re.I)).is_visible()

    page.get_by_role("link", name=re.compile("my polls", re.I)).click()

    assert page.get_by_text(re.compile("welcome to polls list", re.I)).is_visible()


def test_login_with_invalid_credentials_shows_error(page):
    """Verify that invalid login credentials are rejected with an error message."""
    page.goto(f"{BASE_URL}/accounts/login/")

    page.get_by_placeholder("Enter Username").fill("not_a_real_user")
    page.get_by_placeholder("Password").fill("wrongpassword")
    page.get_by_role("button", name=re.compile("login", re.I)).click()

    assert page.get_by_text(
        re.compile("username or password is incorrect", re.I)
    ).is_visible()


def test_unauthorized_user_cannot_open_add_poll_page(page):
    """
    Verify that a logged-in user without poll creation permission
    sees a permission error.
    """
    user = unique_user()

    register_user(page, user)
    login_user(page, user)

    # Navigate directly to the protected Add Poll page after logging in.
    page.goto(f"{BASE_URL}/polls/add/")

    assert page.get_by_text(
        re.compile("sorry but you don't have permission to do that", re.I)
    ).is_visible()
