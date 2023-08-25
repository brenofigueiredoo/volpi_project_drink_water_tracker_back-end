from rest_framework.test import APITestCase
from goals.serializers import Goals
from users.models import User


class UserListCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL_GOALS = "/api/goals"
        cls.BASE_URL_USERS = "/api/users"

        cls.id_nonexistent = "1e0e9d2f-872a-47a7-a223-0be34f64f5e2"
        cls.data_not_found = {"detail": "Not found."}
        cls.user_data = {"name": "raphael", "weight_kg": 84.2}

        cls.goal_date = "2023-09-02"
        cls.goal_invalid_date = "2023-09-200"
        cls.data_invalid_date = {"detail": ["Invalid date format"]}

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_goal_creation_without_date(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        response = self.client.post(f"/api/user/{added_user.id}/goals/")

        msg = (
            "\nVerifique se as informações do Goal retornadas no POST "
            + f"em `/api/user/<uuid:user_id>/goals/<string:date>` com dados validos estão corretas."
        )
        self.assertEqual(response.status_code, 404, msg)

    def test_goal_creation_without_user_id(self):
        response = self.client.post(
            f"/api/user/{self.id_nonexistent}/goals/{self.goal_date}"
        )

        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do Goal retornadas no POST "
            + f"em `/api/user/<uuid:user_id>/goals/<string:date>` com dados validos estão corretas."
        )
        self.assertDictEqual(self.data_not_found, resulted_data, msg)
        self.assertEqual(response.status_code, 404)

    def test_goal_creation(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        response = self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")

        added_goal = Goals.objects.last()

        expected_data = {
            "id": str(added_goal.id),
            "goal_of_the_day_ml": 2947.0,
            "remaining_goals_ml": 0.0,
            "goal_consumed_ml": 0.0,
            "goal_consumed_percentage": 0.0,
            "user": {
                "id": str(added_user.id),
                "name": added_user.name,
                "weight_kg": added_user.weight_kg,
                "goal_ml": added_user.goal_ml,
            },
            "date": str(added_goal.date),
        }
        resulted_data = response.json()

        msg = (
            "\nVerifique se as informações do Goal retornadas no POST "
            + f"em `/api/user/<uuid:user_id>/goals/<string:date>` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(resulted_data["user"]["id"], str(added_user.id), msg)

    def test_goal_retrieve_a_specific_goal_id(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")
        added_goal = Goals.objects.last()

        response = self.client.get(f"{self.BASE_URL_GOALS}/{added_goal.id}")
        resulted_data = response.json()

        msg = (
            "\nVerifique se as informações do Goal retornadas no GET "
            + f"em `{self.BASE_URL_GOALS}/<uuid:goal_id>` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resulted_data["id"], str(added_goal.id), msg)

    def test_goal_retrieve_a_specific_goal_nonexistent(self):
        response = self.client.get(f"{self.BASE_URL_GOALS}/{self.id_nonexistent}")
        resulted_data = response.json()

        msg = (
            "\nVerifique se as informações do Goal retornadas no GET "
            + f"em `{self.BASE_URL_GOALS}/<uuid:goal_id>` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.data_not_found, resulted_data, msg)

    def test_goal_retrieve_a_specific_goal_by_id(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")

        added_goal = Goals.objects.last()

        expected_data = {
            "id": str(added_goal.id),
            "goal_of_the_day_ml": 2947.0,
            "remaining_goals_ml": 0.0,
            "goal_consumed_ml": 0.0,
            "goal_consumed_percentage": 0.0,
            "user": {
                "id": str(added_user.id),
                "name": str(added_user.name),
                "weight_kg": added_user.weight_kg,
                "goal_ml": added_user.goal_ml,
            },
            "date": str(added_goal.date),
        }

        response = self.client.get(f"{self.BASE_URL_GOALS}/{str(added_goal.id)}")
        resulted_data = response.json()

        msg = (
            "\nVerifique se as informações do Goal retornadas no GET "
            + f"em `api/user/<uuid:user_id>/goals/<uuid:goal_id>` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_goal_retrieve_a_specific_goal_by_userid_and_date(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")
        added_goal = Goals.objects.last()

        response = self.client.get(f"/api/user/{added_user.id}/goals/{added_goal.date}")
        resulted_data = response.json()

        expected_data = [
            {
                "id": str(added_goal.id),
                "goal_of_the_day_ml": 2947.0,
                "remaining_goals_ml": 0.0,
                "goal_consumed_ml": 0.0,
                "goal_consumed_percentage": 0.0,
                "user": {
                    "id": str(added_user.id),
                    "name": str(added_user.name),
                    "weight_kg": added_user.weight_kg,
                    "goal_ml": added_user.goal_ml,
                },
                "date": str(added_goal.date),
            }
        ]

        msg = (
            "\nVerifique se as informações do Goal retornadas no GET "
            + f"em `api/user/<uuid:user_id>/goals/<uuid:goal_id>` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_data, resulted_data, msg)

    def test_goal_retrieve_a_specific_goal_by_userid_with_invalid_date(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")

        response = self.client.get(
            f"/api/user/{added_user.id}/goals/{self.goal_invalid_date}"
        )
        resulted_data = response.json()

        msg = (
            "\nVerifique se as informações do Goal retornadas no GET "
            + f"em `api/user/<uuid:user_id>/goals/<uuid:goal_id>` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.data_invalid_date, resulted_data, msg)

    def test_goal_list_of_user_by_userid(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")
        self.client.post(f"/api/user/{added_user.id}/goals/2023-09-20")

        response = self.client.get(f"/api/user/{added_user.id}/goals")
        resulted_data = response.json()

        msg = (
            "\nVerifique se as informações do Goal retornadas no GET "
            + f"em `api/user/<uuid:user_id>/goals` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resulted_data), 2, msg)

    def test_goal_delete_specific_goal_with_invalid_id(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")

        response = self.client.delete(f"{self.BASE_URL_GOALS}/{self.id_nonexistent}")
        resulted_data = response.json()

        msg = (
            "\nVerifique se as informações do Goal retornadas no DELETE "
            + f"em `{self.BASE_URL_GOALS}/<uuid:goal_id>` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(resulted_data, self.data_not_found, msg)

    def test_goal_delete_specific_goal(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")
        added_goal = Goals.objects.last()

        response = self.client.delete(f"{self.BASE_URL_GOALS}/{added_goal.id}")

        msg = (
            "\nVerifique se as informações do Goal retornadas no DELETE "
            + f"em `{self.BASE_URL_GOALS}/<uuid:goal_id>` com dados validos estão corretas e 204."
        )

        self.assertEqual(response.status_code, 204, msg)

    def test_goal_update_specific_goal(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")
        added_goal = Goals.objects.last()

        goal_update_data = {"quantity": 250}

        response = self.client.patch(
            f"{self.BASE_URL_GOALS}/{added_goal.id}/drinkwater",
            data=goal_update_data,
            format="json",
        )
        resulted_data = response.json()

        expected_data = {
            "id": str(added_goal.id),
            "goal_of_the_day_ml": 2947.0,
            "remaining_goals_ml": 2697.0,
            "goal_consumed_ml": 250.0,
            "goal_consumed_percentage": 8.48,
            "user": {
                "id": str(added_user.id),
                "name": added_user.name,
                "weight_kg": added_user.weight_kg,
                "goal_ml": added_user.goal_ml,
            },
            "date": str(added_goal.date),
        }

        msg = (
            "\nVerifique se as informações do Goal retornadas no PATCH "
            + f"em `/api/goals/<uuid:goal_id>/drinkwater` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(resulted_data, expected_data, msg)

    def test_goal_update_specific_goal_with_invalid_body(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")
        added_goal = Goals.objects.last()

        response = self.client.patch(
            f"{self.BASE_URL_GOALS}/{added_goal.id}/drinkwater",
            data={},
            format="json",
        )
        resulted_data = response.json()

        expected_data = {"quantity": ["O campo 'quantity' é obrigatório."]}

        msg = (
            "\nVerifique se as informações do Goal retornadas no PATCH "
            + f"em `/api/goals/<uuid:goal_id>/drinkwater` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(resulted_data, expected_data, msg)

    def test_goal_update_specific_goal_with_invalid_id(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(f"/api/user/{added_user.id}/goals/{self.goal_date}")

        goal_update_data = {"quantity": 250}

        response = self.client.patch(
            f"{self.BASE_URL_GOALS}/{self.id_nonexistent}/drinkwater",
            data=goal_update_data,
            format="json",
        )
        resulted_data = response.json()

        msg = (
            "\nVerifique se as informações do Goal retornadas no PATCH "
            + f"em `/api/goals/<uuid:goal_id>/drinkwater` com dados validos estão corretas."
        )

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(resulted_data, self.data_not_found, msg)
