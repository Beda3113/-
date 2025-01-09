import pytest
import responses
from your_module import fetch_articles  # Замените на ваше имя модуля

@pytest.fixture
def mock_habr_response():
    # Замокируем ответ от Habr
    responses.add(responses.GET, 'https://habr.com/ru/articles/',
                  body='<html><body><article>'
                       '<h2><a href="https://habr.com/ru/post/1/">Статья про дизайн</a></h2>'
                       '<time title="2023-01-01T00:00:00Z"></time>'
                       '<div class="post-preview__text">Краткое описание статьи.</div>'
                       '</article>'
                       '<article>'
                       '<h2><a href="https://habr.com/ru/post/2/">Статья про что-то другое</a></h2>'
                       '<time title="2023-01-02T00:00:00Z"></time>'
                       '<div class="post-preview__text">Краткое описание другой статьи.</div>'
                       '</article>'
                       '</body></html>',
                  status=200)

@pytest.mark.usefixtures("mock_habr_response")
def test_fetch_articles_success():
    expected = [
        ('2023-01-01T00:00:00Z', 'Статья про дизайн', 'https://habr.com/ru/post/1/')
    ]
    articles = fetch_articles('https://habr.com/ru/articles/')
    assert articles == expected

def test_fetch_articles_no_keywords():
    # Тест для случая, когда нет подходящих статей
    html_content = (
        '<html><body><article>'
        '<h2><a href="https://habr.com/ru/post/2/">Статья про что-то другое</a></h2>'
        '<time title="2023-01-02T00:00:00Z"></time>'
        '<div class="post-preview__text">Краткое описание другой статьи.</div>'
        '</article></body></html>'
    )
    
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'https://habr.com/ru/articles/', body=html_content, status=200)
        articles = fetch_articles('https://habr.com/ru/articles/')
        assert articles == []

def test_fetch_articles_error():
    # Тест для обработки ошибки при запросе
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'https://habr.com/ru/articles/', body=requests.exceptions.ConnectionError(), status=500)
        
        with pytest.raises(RuntimeError, match="Ошибка при получении статей"):
            fetch_articles('https://habr.com/ru/articles/')
