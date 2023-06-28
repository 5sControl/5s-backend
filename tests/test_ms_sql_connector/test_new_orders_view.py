from django.core.management import call_command
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from ..const_results import OPERATION_NEW_ORDER_VIEWS, ORDERS_NEW_ORDER_VIEWS


class CreateDatabaseConnectionAPIViewTestCase(APITestCase):
    fixtures = [
        "tests/fixtures/lic.json",
        "tests/fixtures/comp.json",
        "tests/fixtures/database_conn.json",
        "tests/fixtures/filtroprttypeid.json",
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

    def test_get_operation(self):
        param = "from=2023-06-21&to=2023-06-21"
        url = f"/api/order/all-orders//api/new-order/operations/?{param}"

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        
        self.assertEqual(data[0] == OPERATION_NEW_ORDER_VIEWS)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 15)
        
        for item in data:
            self.assertIsInstance(item, dict)

    def test_get_orders(self):
        param = "from=2023-06-21&to=2023-06-21"
        url = f"/api/new-order/orders/?{param}"

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data == ORDERS_NEW_ORDER_VIEWS)

    def test_get_orders_detail(self):
        param = "operation=1326033"
        url = f"/api/new-order/order-detail/?{param}"

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["id"] == 1326033)
        self.assertEqual(data["orId"] == "G66848")
        self.assertEqual(data["oprName"] == "Okucia")
        self.assertEqual(data["elType"] == "S9000 NL 6802/6003")
        self.assertEqual(data["sTime"] == 1687238338000)
        self.assertEqual(data["eTime"] == 1687241938000)
        self.assertEqual(data["frsName"] == "Virmantas")
        self.assertEqual(data["lstName"] == "Petraitis")
        self.assertEqual(data["status"] == None)
        self.assertEqual(data["video"] == {})

