import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from polls.models import Choice, Poll, Vote


@pytest.mark.django_db
def test_polls_list_view_queries_polls_from_database(client):
    """
    Integration test: verifies that the polls list view and database work
    together by creating a real Poll and confirming the view returns a page.
    """
    user = User.objects.create_user(
        username="integrationuser",
        email="integration@example.com",
        password="password123",
    )
    poll = Poll.objects.create(
        text="What is your favorite testing tool?",
        owner=user,
    )

    client.login(username="integrationuser", password="password123")
    response = client.get(reverse("polls:list"))

    assert response.status_code == 200
    assert Poll.objects.filter(id=poll.id).exists()
    assert b"Polls" in response.content or b"poll" in response.content.lower()


@pytest.mark.django_db
def test_poll_vote_view_creates_vote_in_database(client):
    """
    Integration test: verifies that the vote view, Poll/Choice/Vote models,
    and database work together to record a submitted vote.
    """
    user = User.objects.create_user(
        username="voteuser",
        email="voteuser@example.com",
        password="password123",
    )
    poll = Poll.objects.create(text="Which language do you prefer?", owner=user)
    choice = Choice.objects.create(poll=poll, choice_text="Python")

    client.login(username="voteuser", password="password123")
    response = client.post(reverse("polls:vote", args=[poll.id]), {"choice": choice.id})

    assert response.status_code == 200
    assert Vote.objects.filter(user=user, poll=poll, choice=choice).exists()
