import os
import unittest

import requests
from dotenv import load_dotenv


load_dotenv()
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME", "test-repo")
API_URL = "https://api.github.com/user/repos"


def create_repository():
    """Создает новый репозиторий на GitHub."""
    response = requests.post(
        API_URL,
        json={"name": REPO_NAME, "private": False},
        auth=(GITHUB_USERNAME, GITHUB_TOKEN)
    )
    return response


def check_repository_exists():
    """Проверяет, существует ли репозиторий на GitHub."""
    response = requests.get(
        f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}",
        auth=(GITHUB_USERNAME, GITHUB_TOKEN)
    )
    return response.status_code == 200


def delete_repository():
    """Удаляет репозиторий на GitHub."""
    response = requests.delete(
        f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}",
        auth=(GITHUB_USERNAME, GITHUB_TOKEN)
    )
    return response


class TestGitHubAPI(unittest.TestCase):
    def setUp(self):
        """Создает репозиторий перед каждым тестом"""
        if check_repository_exists():
            delete_repository()
        self.create_response = create_repository()
        self.assertEqual(
            self.create_response.status_code,
            201,
            "Ошибка при создании репозитория"
        )

    def tearDown(self):
        """Удаляет репозиторий после каждого теста, если он существует."""
        if check_repository_exists():
            self.delete_response = delete_repository()
            self.assertEqual(
                self.delete_response.status_code,
                204,
                "Ошибка при удалении репозитория"
            )

    def test_repository_creation(self):
        """Проверяет, что репозиторий был успешно создан и существует."""
        self.assertTrue(
            check_repository_exists(),
            f"Репозиторий '{REPO_NAME}' не существует после создания."
        )

    def test_repository_deletion(self):
        """Проверяет, что репозиторий был успешно удален."""
        delete_repository()
        self.assertFalse(
            check_repository_exists(),
            f"Репозиторий '{REPO_NAME}' все еще существует после удаления."
        )


if __name__ == "__main__":
    unittest.main()
