from rest_framework.test import APITestCase
from goals.serializers import Goals
from users.models import User


class UserListCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/goals"
        cls.BASE_URL_USERS = "/api/users"
        cls.id_nonexistent = "1e0e9d2f-872a-47a7-a223-0be34f64f5e2"
        cls.data_not_found = {"detail": "Not found."}
        cls.user_data = {"name": "raphael", "weight_kg": 84.2}
        cls.goal_data = {"date": "2023-9-2"}

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_goal_creation_without_required_fields(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        response = self.client.post(
            f"{self.BASE_URL}/user/create/{str(added_user.id)}", data={}, format="json"
        )

        expected_data = {
            "date": ["This field is required."],
        }
        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do Goal retornadas no POST "
            + f"em `{self.BASE_URL}/user/create/<uuid:user_id>` com dados validos estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(response.status_code, 400)

    def test_goal_creation_without_user_id(self):
        response = self.client.post(
            f"{self.BASE_URL}/user/create/{self.id_nonexistent}",
            data=self.goal_data,
            format="json",
        )

        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do Goal retornadas no POST "
            + f"em `{self.BASE_URL}/user/create/<uuid:user_id>` com dados validos estão corretas."
        )
        self.assertDictEqual(self.data_not_found, resulted_data, msg)
        self.assertEqual(response.status_code, 404)

    def test_goal_creation(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        response = self.client.post(
            f"{self.BASE_URL}/user/create/{str(added_user.id)}",
            data=self.goal_data,
            format="json",
        )

        added_goal = Goals.objects.last()

        expected_data = {
            "id": str(added_goal.id),
            "goal_of_the_day_ml": 2947.0,
            "remaining_goals_ml": 0.0,
            "goal_consumed_ml": 0.0,
            "goal_consumed_percentage": 0.0,
            "user": str(added_user.id),
            "date": str(added_goal.date),
        }
        resulted_data = response.json()
        msg = (
            "\nVerifique se as informações do Goal retornadas no POST "
            + f"em `{self.BASE_URL}/user/create/<uuid:user_id>` com dados validos estão corretas."
        )

        self.assertDictEqual(expected_data, resulted_data, msg)
        self.assertEqual(resulted_data["user"], str(added_user.id))
        self.assertEqual(response.status_code, 201)

    def test_goal_retrieve_a_specific_goal(self):
        self.client.post(self.BASE_URL_USERS, data=self.user_data, format="json")
        added_user = User.objects.last()

        self.client.post(
            f"{self.BASE_URL}/user/create/{str(added_user.id)}",
            data=self.goal_data,
            format="json",
        )

        added_goal = Goals.objects.last()

        expected_data = {
            "id": str(added_goal.id),
            "goal_of_the_day_ml": 2947.0,
            "remaining_goals_ml": 0.0,
            "goal_consumed_ml": 0.0,
            "goal_consumed_percentage": 0.0,
            "user": added_user.id,
            "date": str(added_goal.date),
        }

        response = self.client.get(f"{self.BASE_URL}/{str(added_goal.id)}")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_data, response.data)

    def test_goal_retrieve_a_specific_goal_nonexistent(self):
        response = self.client.get(f"{self.BASE_URL}/{self.id_nonexistent}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.data_not_found, response.data)
