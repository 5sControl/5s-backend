from django.core.management import call_command
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from ..const_results import OPERATIONS, G59811, ORDERS


class CreateDatabaseConnectionAPIViewTestCase(APITestCase):
    fixtures = [
        "tests/fixtures/lic.json",
        "tests/fixtures/comp.json",
        "tests/fixtures/database_conn.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.load_fixtures()
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    @classmethod
    def load_fixtures(cls):
        for fixture in cls.fixtures:
            call_command("loaddata", fixture, verbosity=0)

    def test_get_orders_view_orders(self):
        url = "/api/order/all-orders/"

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("count" in response.data)
        self.assertTrue("results" in response.data)

    def test_get_orders_by_id_1(self):
        url = "/api/order/by-order/PRW199234"

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["current_page"], 1)
        self.assertEqual(response.data["records_on_page"], 50)
        self.assertEqual(response.data["all_page_count"], 1)
        self.assertEqual(len(response.data["results"]), 1)

        self.assertEqual(response.data["results"][0]["indeks"], 363992)
        self.assertTrue(response.data["results"][0]["zlecenie"].startswith("PRW199234"))
        self.assertEqual(response.data["results"][0]["status"], "Started")
        self.assertEqual(
            response.data["results"][0]["terminrealizacji"], "2023-03-03 00:00:00.0000000"
        )
        self.assertEqual(response.data["results"][0]["datawejscia"], "23.02.2023 14:18:00")


    def test_get_orders_by_id_2(self):
        url = "/api/order/by-order/G59811"

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, follow=True)

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, G59811)

    def test_get_orders_by_id_3(self):
        for order in ORDERS:
            url = f"/api/order/by-order/{order}"

            self.client.force_authenticate(user=self.user)
            response = self.client.get(url, follow=True)

            self.assertEqual(response.status_code, 200)

    def test_get_orders_view_oprt_name(self):
        url = "/api/order/get-operations/"

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, follow=True)

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, OPERATIONS)
