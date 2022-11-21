import pytest
from newsletter.models import Message, Article, Newsletter

from meetings.renderers import render_message


def get_title(faker):
    words = faker.words()
    words[0].capitalize()
    return " ".join(words)


@pytest.fixture
def message(faker):
    newsletter = Newsletter()
    newsletter.save()

    message = Message(title=faker.catch_phrase())
    message.save()

    articles = Article.objects.bulk_create([
        Article(title=get_title(faker), text=faker.paragraph(), sortorder=0, post=message),
        Article(title=get_title(faker), text=faker.paragraph(), sortorder=1, post=message),
    ])
    message.articles.set(articles)
    message.save()
    return message


@pytest.mark.django_db
def test_render_message(message):
    result = render_message(message)

    assert result != ""
