from accounts.forms import UserRegistrationForm
from polls.forms import ChoiceAddForm, PollAddForm


def test_user_registration_form_accepts_valid_data():
    form = UserRegistrationForm(
        data={
            "username": "sandytest",
            "email": "sandy@example.com",
            "password1": "password123",
            "password2": "password123",
        }
    )

    assert form.is_valid()


def test_user_registration_form_rejects_short_username():
    form = UserRegistrationForm(
        data={
            "username": "abc",
            "email": "sandy@example.com",
            "password1": "password123",
            "password2": "password123",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


def test_poll_add_form_accepts_valid_question_and_choices():
    form = PollAddForm(
        data={
            "text": "What is your favorite programming language?",
            "choice1": "Python",
            "choice2": "JavaScript",
        }
    )

    assert form.is_valid()


def test_choice_add_form_rejects_empty_choice():
    form = ChoiceAddForm(data={"choice_text": ""})

    assert not form.is_valid()
    assert "choice_text" in form.errors