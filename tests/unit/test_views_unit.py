from unittest.mock import Mock, patch

from django.test import RequestFactory

from polls.views import poll_vote, polls_add


class DummyUser:
    """
    Test double type: Dummy
    Replaces: a real authenticated Django user
    Why useful: the view only needs a user object with is_authenticated and has_perm
    How it isolates: avoids creating a real user in the database
    """

    is_authenticated = True
    username = "dummy-user"

    def has_perm(self, permission_name):
        return False


class StubPoll:
    """
    Test double type: Stub
    Replaces: a real Poll model object from the database
    Why useful: lets the test control whether the user can vote
    How it isolates: avoids database setup and makes user_can_vote deterministic
    """

    def __init__(self, can_vote):
        self.can_vote = can_vote

    def user_can_vote(self, user):
        return self.can_vote


class SpyVote:
    """
    Test double type: Spy
    Replaces: the real Vote model constructor
    Why useful: records whether save() was called
    How it isolates: avoids writing a real Vote to the database
    """

    instances = []

    def __init__(self, user, poll, choice):
        self.user = user
        self.poll = poll
        self.choice = choice
        self.saved = False
        SpyVote.instances.append(self)

    def save(self):
        self.saved = True


def test_polls_add_denies_user_without_permission_using_dummy_user():
    request = RequestFactory().get("/polls/add/")
    request.user = DummyUser()

    response = polls_add(request)

    assert response.status_code == 200
    assert b"Sorry but you don't have permission to do that!" in response.content


def test_poll_vote_redirects_when_user_already_voted_using_stub_and_mock():
    request = RequestFactory().post("/polls/1/vote/", data={"choice": "1"})
    request.user = DummyUser()

    stub_poll = StubPoll(can_vote=False)

    with (
        patch("polls.views.get_object_or_404", return_value=stub_poll),
        patch("polls.views.messages.error") as mock_error,
        patch("polls.views.redirect", return_value="redirected") as mock_redirect,
    ):
        response = poll_vote(request, poll_id=1)

    assert response == "redirected"
    mock_error.assert_called_once()
    mock_redirect.assert_called_once_with("polls:list")


def test_poll_vote_rejects_missing_choice_using_stub_and_mock():
    request = RequestFactory().post("/polls/1/vote/", data={})
    request.user = DummyUser()

    stub_poll = StubPoll(can_vote=True)

    with (
        patch("polls.views.get_object_or_404", return_value=stub_poll),
        patch("polls.views.messages.error") as mock_error,
        patch("polls.views.redirect", return_value="redirected") as mock_redirect,
    ):
        response = poll_vote(request, poll_id=1)

    assert response == "redirected"
    mock_error.assert_called_once()
    mock_redirect.assert_called_once_with("polls:detail", 1)


def test_poll_vote_saves_vote_using_spy_vote_and_mocked_choice():
    request = RequestFactory().post("/polls/1/vote/", data={"choice": "5"})
    request.user = DummyUser()

    stub_poll = StubPoll(can_vote=True)
    fake_choice = Mock(id=5)
    SpyVote.instances.clear()

    with (
        patch("polls.views.get_object_or_404", return_value=stub_poll),
        patch("polls.views.Choice.objects.get", return_value=fake_choice),
        patch("polls.views.Vote", SpyVote),
        patch("polls.views.render", return_value="rendered") as mock_render,
    ):
        response = poll_vote(request, poll_id=1)

    assert response == "rendered"
    assert len(SpyVote.instances) == 1
    assert SpyVote.instances[0].saved is True
    assert SpyVote.instances[0].choice == fake_choice
    mock_render.assert_called_once()
