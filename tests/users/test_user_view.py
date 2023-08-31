from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User
from users.serializers import UserSerializer


class UserListCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {"name": "raphael", "weight_kg": 84.2}
        cls.BASE_URL = "/api/users"
        cls.id_nonexistent = "1e0e9d2f-872a-47a7-a223-0be34f64f5e2"
        cls.data_not_found = {"detail": "Not found."}

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_user_creation_without_required_fields(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        resulted_data: dict = response.json()
        expected_data = {
            "name": ["This field is required."],
            "weight_kg": ["This field is required."],
        }

        msg = (
            "\nVerifique se as informações do usuário retornadas no POST "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertDictEqual(expected_data, resulted_data, msg)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
            + f"em `{self.BASE_URL}` é {expected_status_code}."
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_user_creation_with_name_and_weight(self):
        response = self.client.post(self.BASE_URL, data=self.user_data, format="json")

        added_user = User.objects.last()

        expected_data = {
            "id": str(added_user.pk),
            "name": "raphael",
            "weight_kg": 84.2,
            "goal_ml": 2947.0,
        }
        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do usuário retornadas no POST "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = (
            "\nVerifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` com dados validos é {expected_status_code}."
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_user_retrieve_a_specific_user(self):
        self.client.post(self.BASE_URL, data=self.user_data, format="json")

        added_user = User.objects.last()

        response = self.client.get(f"{self.BASE_URL}/{added_user.id}")

        msg = (
            "\nVerifique se as informações do usuário retornadas no GET "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(added_user.id), msg)
        self.assertEqual(UserSerializer(instance=added_user).data, response.data, msg)

    def test_user_retrieve_a_specific_user_nonexistent(self):
        response = self.client.get(f"{self.BASE_URL}/{self.id_nonexistent}")

        msg = (
            "\nVerifique se as informações do usuário retornadas no GET "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.data_not_found, response.data, msg)

    def test_user_update_a_specific_user_nonexistent(self):
        response = self.client.patch(f"{self.BASE_URL}/{self.id_nonexistent}")

        msg = (
            "\nVerifique se as informações do usuário retornadas no PATCH "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.data_not_found, response.data, msg)

    def test_user_update_name_a_specific_user(self):
        self.client.post(self.BASE_URL, data=self.user_data, format="json")

        added_user = User.objects.last()

        updated_user_data = {
            "name": "user atualizado",
            "weight_kg": 89.2,
        }

        response = self.client.patch(
            f"{self.BASE_URL}/{str(added_user.id)}",
            data=updated_user_data,
            format="json",
        )

        expected_data = {
            "id": str(added_user.id),
            "name": "user atualizado",
            "weight_kg": 89.2,
            "goal_ml": 3122.0,
        }
        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do usuário retornadas no PATCH "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(response.status_code, 200)

    def test_user_update_weight_a_specific_user(self):
        self.client.post(self.BASE_URL, data=self.user_data, format="json")

        added_user = User.objects.last()

        updated_user_data = {
            "weight_kg": 89.2,
        }

        response = self.client.patch(
            f"{self.BASE_URL}/{str(added_user.id)}",
            data=updated_user_data,
            format="json",
        )

        expected_data = {
            "id": str(added_user.id),
            "name": added_user.name,
            "weight_kg": 89.2,
            "goal_ml": 3122.0,
        }
        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do usuário retornadas no PATCH "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(response.status_code, 200)

    def test_user_delete_a_specific_user_nonexistent(self):
        self.client.post(self.BASE_URL, data=self.user_data, format="json")

        response = self.client.delete(f"{self.BASE_URL}/{self.id_nonexistent}")

        msg = (
            "\nVerifique se as informações do usuário retornadas no DELETE "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.data_not_found, response.data, msg)

    def test_user_delete_a_specific_user(self):
        self.client.post(self.BASE_URL, data=self.user_data, format="json")
        added_user = User.objects.last()

        response = self.client.delete(f"{self.BASE_URL}/{str(added_user.id)}")

        msg = (
            "\nVerifique se as informações do usuário retornadas no DELETE "
            + f"em `{self.BASE_URL}` com dados validos estão corretas."
        )
        self.assertEqual(response.status_code, 204, msg)
