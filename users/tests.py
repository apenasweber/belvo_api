from urllib import response

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

user_sample = {"name": "Teste", "email": "tester@email.com"}
transaction_sample = {
    "reference": "Teste",
    "date": "2020-01-01",
    "type": "inflow",
    "amount": 100,
    "category": "Teste",
    "user_email": "tester@email.com",
}

class TesteUserPost(APITestCase):
    def test_user_post_with_valid_data(self):
        response = self.client.post(reverse("users-list"), user_sample)
        self.assertEqual(response.status_code, 201)

    def test_user_post_with_invalid_data(self):
        sample = {"name": "Teste", "email": 123}
        response = self.client.post(reverse("users-list"), sample)
        self.assertEqual(response.status_code, 400)

    def test_user_post_with_duplicate_email(self):
        self.client.post(reverse("users-list"), user_sample)
        user_sample_2 = {"name": "Teste", "email": "tester@email.com"}
        response = self.client.post(reverse("users-list"), user_sample_2)
        self.assertEqual(response.status_code, 400)


class TestUserGet(APITestCase):
    def test_user_get_with_valid_data(self):
        self.client.post(reverse("users-list"), user_sample)
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, 200)

    def test_user_get_by_email(self):
        self.client.post(reverse("users-list"), user_sample)
        response = self.client.get(reverse("users-list"), {"email": "tester@email.com"})
        email = response.data[0]["email"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(email, "tester@email.com")


class TestTransactionPost(APITestCase):
    def test_transaction_post_with_valid_data(self):
        self.client.post(reverse("users-list"), user_sample)

        response = self.client.post(reverse("transactions-list"), transaction_sample)
        self.assertEqual(response.status_code, 201)

    def test_transaction_post_with_bulk_data(self):
        self.client.post(reverse("users-list"), user_sample)
        bulk_transaction_sample = [
            {
                "reference": "000061",
                "date": "2020-01-03",
                "amount": "-51.13",
                "type": "outflow",
                "category": "groceries",
                "user_email": "tester@email.com",
            },
            {
                "reference": "000062",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_email": "tester@email.com",
            },
            {
                "reference": "000063",
                "date": "2020-01-10",
                "amount": "-150.72",
                "type": "outflow",
                "category": "transfer",
                "user_email": "tester@email.com",
            },
        ]
        for transaction in bulk_transaction_sample:
            response = self.client.post(reverse("transactions-list"), transaction)
            self.assertEqual(response.status_code, 201)

    def test_transaction_post_without_amount(self):
        self.client.post(reverse("users-list"), user_sample)
        not_amount_transaction_sample = {
            "reference": "Teste",
            "date": "2020-01-01",
            "type": "inflow",
            "category": "Teste",
            "user_email": "tester@email.com",
            "amount": "",
        }
        response = self.client.post(reverse("transactions-list"), not_amount_transaction_sample)
        self.assertEqual(response.status_code, 400)

    def test_transaction_post_with_inflow_type_and_negative_amount(self):
        self.client.post(reverse("users-list"), user_sample)
        negative_inflow_transaction_sample = {
            "reference": "Teste",
            "date": "2020-01-01",
            "type": "inflow",
            "category": "Teste",
            "user_email": "tester@email.com",
            "amount": "-100",
        }
        response = self.client.post(reverse("transactions-list"), negative_inflow_transaction_sample)
        self.assertEqual(response.status_code, 400)

    def test_transaction_post_with_outflow_type_and_positive_amount(self):
        self.client.post(reverse("users-list"), user_sample)
        positive_outflow_transaction_sample = {
            "reference": "Teste",
            "date": "2020-01-01",
            "type": "outflow",
            "category": "Teste",
            "user_email": "tester@email.com",
            "amount": "100",
        }
        response = self.client.post(reverse("transactions-list"), positive_outflow_transaction_sample)
        self.assertEqual(response.status_code, 400)

    def test_transaction_post_with_existing_reference(self):
        self.client.post(reverse("users-list"), user_sample)
        self.client.post(reverse("transactions-list"), transaction_sample)
        duplicated_transaction_sample = {
            "reference": "Teste",
            "date": "2020-01-01",
            "type": "inflow",
            "category": "Teste",
            "user_email": "tester@email.com",
            "amount": "100",
        }
        response = self.client.post(reverse("transactions-list"), duplicated_transaction_sample)
        self.assertEqual(response.status_code, 400)


class TestTransactionGet(APITestCase):
    def test_transaction_get_all(self):
        self.client.post(reverse("users-list"), user_sample)
        self.client.post(reverse("transactions-list"), transaction_sample)
        response = self.client.get(reverse("transactions-list"))
        number_of_transactions = len(response.data)
        self.assertEqual(number_of_transactions, 1)

    def test_transaction_get_by_email(self):
        self.client.post(reverse("users-list"), user_sample)
        self.client.post(reverse("transactions-list"), transaction_sample)
        response = self.client.get(
            reverse("transactions-list"), {"user_email": "tester@email.com"}
        )
        email = response.data[0]["user_email"]
        self.assertEqual(email, "tester@email.com")

    def test_transaction_get_by_email_and_type(self):
        self.client.post(reverse("users-list"), user_sample)
        self.client.post(reverse("transactions-list"), transaction_sample)
        response = self.client.get(
            reverse("transactions-list"),
            {"user_email": "tester@email.com", "type": "inflow"},
        )
        transaction_type = response.data[0]["type"]
        email = response.data[0]["user_email"]
        number_of_transactions = len(response.data)
        self.assertEqual(transaction_type, "inflow")
        self.assertEqual(email, "tester@email.com")
        self.assertEqual(number_of_transactions, 1)
    
    def test_transaction_get_summary_by_type(self):
        self.client.post(reverse("users-list"), user_sample)
        self.client.post(reverse("transactions-list"), transaction_sample)
        transaction_sample_2 = {
            "reference": "000064",
            "date": "2020-01-10",
            "amount": "100",
            "type": "inflow",
            "category": "salary",
            "user_email": "tester@email.com",
        }
        self.client.post(reverse("transactions-list"), transaction_sample_2)
        transaction_sample_3 = {
            "reference": "000065",
            "date": "2020-01-10",
            "amount": "-100",
            "type": "outflow",
            "category": "salary",
            "user_email": "tester@email.com",
        }
        self.client.post(reverse("transactions-list"), transaction_sample_3)
        inflow_response = self.client.get(reverse("transactions_summary-list"))
        expected_email = "tester@email.com"
        expected_total_inflow = 200
        expected_total_outflow = -100
        self.assertEqual(inflow_response.data[0]["email"], expected_email)
        self.assertEqual(inflow_response.data[0]["total_amount_by_inflow"], expected_total_inflow)
        self.assertEqual(inflow_response.data[0]["total_amount_by_outflow"], expected_total_outflow)
        
        # ('total_amount_by_inflow', Decimal('200')), ('total_amount_by_outflow', Decimal('-100')
    def test_transaction_get_summary_by_category(self):
        self.client.post(reverse("users-list"), user_sample)
        self.client.post(reverse("transactions-list"), transaction_sample)
        transaction_sample_2 = {
            "reference": "000064",
            "date": "2020-01-10",
            "amount": "-100",
            "type": "outflow",
            "category": "mcdonalds",
            "user_email": "tester@email.com",
        }
        self.client.post(reverse("transactions-list"), transaction_sample_2)
        transaction_sample_3 = {
            "reference": "000065",
            "date": "2020-01-10",
            "amount": "10000",
            "type": "inflow",
            "category": "salary",
            "user_email": "tester@email.com",
        }
        self.client.post(reverse("transactions-list"), transaction_sample_3)
        categories_response = self.client.get(reverse("transactions_summary-summary"))
        expected_inflow = 10000.00
        expected_outflow = -100.00
        self.assertEqual(categories_response.data["inflow"]["salary"], expected_inflow)
        self.assertEqual(categories_response.data["outflow"]["mcdonalds"], expected_outflow)