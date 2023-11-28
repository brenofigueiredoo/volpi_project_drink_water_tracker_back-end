from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer


class UserListCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users"
        cls.LOGIN_URL = "/api/login"
        cls.token_not_found = {
            "detail": "Authentication credentials were not provided."
        }
        cls.user_data = {
            "username": "raphael",
            "email": "raphael@email.com",
            "password": "1234",
            "weight_kg": 84.2,
        }
        cls.user_data_login = {
            "email": "raphael@email.com",
            "password": "1234",
        }

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_user_creation_without_required_fields(self):
        response = self.client.post(
            self.BASE_URL,
            data={},
            format="json",
        )

        resulted_data: dict = response.json()
        expected_data = {
            "username": ["This field is required."],
            "email": ["This field is required."],
            "password": ["This field is required."],
            "weight_kg": ["This field is required."],
        }

        msg = (
            "\nVerifique se as informações do usuário retornadas no POST "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(
            response.status_code, 400, "Verifique se o status code está correto!"
        )

    def test_user_creation_with_required_fields(self):
        response = self.client.post(
            self.BASE_URL,
            data=self.user_data,
            format="json",
        )

        added_user = User.objects.last()

        expected_data = {
            "id": str(added_user.pk),
            "username": "raphael",
            "email": "raphael@email.com",
            "weight_kg": 84.2,
            "goal_ml": 2947.0,
        }
        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do usuário retornadas no POST "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(
            response.status_code, 201, "Verifique se o status code está correto!"
        )

    def test_user_retrieve_a_specific_user(self):
        self.client.post(
            self.BASE_URL,
            data=self.user_data,
            format="json",
        )

        added_user = User.objects.last()

        login_response = self.client.post(
            self.LOGIN_URL,
            data=self.user_data_login,
            format="json",
        )

        token = login_response.data.get("access")

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get(
            f"{self.BASE_URL}/detail",
            headers=headers,
        )

        msg = (
            "\nVerifique se as informações do usuário retornadas no GET "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertEqual(
            response.status_code, 200, "Verifique se o status code está correto!"
        )
        self.assertEqual(response.json()["id"], str(added_user.id), msg)
        self.assertEqual(UserSerializer(instance=added_user).data, response.data, msg)

    def test_user_retrieve_a_specific_user_without_token(self):
        response = self.client.get(
            f"{self.BASE_URL}/detail",
        )

        msg = (
            "\nVerifique se as informações do usuário retornadas no GET "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertEqual(
            response.status_code, 401, "Verifique se o status code está correto!"
        )
        self.assertEqual(self.token_not_found, response.data, msg)

    def test_user_update_a_specific_user_without_token(self):
        response = self.client.patch(
            f"{self.BASE_URL}/detail",
        )

        msg = (
            "\nVerifique se as informações do usuário retornadas no PATCH "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertEqual(
            response.status_code, 401, "Verifique se o status code está correto!"
        )
        self.assertEqual(self.token_not_found, response.data, msg)

    def test_user_update_username_a_specific_user(self):
        self.client.post(
            self.BASE_URL,
            data=self.user_data,
            format="json",
        )

        added_user = User.objects.last()

        login_response = self.client.post(
            self.LOGIN_URL,
            data=self.user_data_login,
            format="json",
        )

        token = login_response.data.get("access")

        updated_user_data = {"username": "user atualizado"}

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.patch(
            f"{self.BASE_URL}/detail",
            data=updated_user_data,
            headers=headers,
            format="json",
        )

        expected_data = {
            "id": str(added_user.id),
            "username": "user atualizado",
            "email": added_user.email,
            "weight_kg": added_user.weight_kg,
            "goal_ml": added_user.goal_ml,
        }
        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do usuário retornadas no PATCH "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(
            response.status_code, 200, "Verifique se o status code está correto!"
        )

    def test_user_update_weight_a_specific_user(self):
        self.client.post(
            self.BASE_URL,
            data=self.user_data,
            format="json",
        )

        added_user = User.objects.last()

        login_response = self.client.post(
            self.LOGIN_URL,
            data=self.user_data_login,
            format="json",
        )

        token = login_response.data.get("access")

        updated_user_data = {"weight_kg": 89.2}

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.patch(
            f"{self.BASE_URL}/detail",
            data=updated_user_data,
            headers=headers,
            format="json",
        )

        expected_data = {
            "id": str(added_user.id),
            "username": added_user.username,
            "email": added_user.email,
            "weight_kg": 89.2,
            "goal_ml": 3122.0,
        }
        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do usuário retornadas no PATCH "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(
            response.status_code, 200, "Verifique se o status code está correto!"
        )

    def test_user_delete_a_specific_user_without_token(self):
        self.client.post(
            self.BASE_URL,
            data=self.user_data,
            format="json",
        )

        response = self.client.delete(
            f"{self.BASE_URL}/detail",
        )

        msg = (
            "\nVerifique se as informações do usuário retornadas no DELETE "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertEqual(
            response.status_code, 401, "Verifique se o status code está correto!"
        )
        self.assertEqual(self.token_not_found, response.data, msg)

    def test_user_delete_a_specific_user(self):
        self.client.post(
            self.BASE_URL,
            data=self.user_data,
            format="json",
        )

        login_response = self.client.post(
            self.LOGIN_URL,
            data=self.user_data_login,
            format="json",
        )

        token = login_response.data.get("access")

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.delete(
            f"{self.BASE_URL}/detail",
            headers=headers,
            format="json",
        )

        self.assertEqual(
            response.status_code, 204, "Verifique se o status code está correto!"
        )
