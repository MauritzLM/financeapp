from django.test import TestCase
from rest_framework.test import APIClient
from personalfinance.models import Budget, Transaction, Pot

from django.contrib.auth import get_user_model
User = get_user_model()

# index view test
class IndexViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_url_exists(self):
        client = APIClient()
        client.login(username='testuser1', password='1X<ISRUkw+tuK')

        response = client.get('/finance-api/')
        self.assertEqual(response.status_code, 200)


# budget list view
class BudgetListViewTest(TestCase):
     
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        Budget.objects.create(category='Entertainment', maximum=400.00, theme='#277C78', user=test_user1)
        Budget.objects.create(category='Personal care', maximum=200.00, theme='#626070', user=test_user1)
     
    def test_user_not_logged_in(self):
        client = APIClient()
        response = client.get('/finance-api/budget')
        self.assertEqual(response.status_code, 403)

    # get - all budgets of user then serialize then response = serialized data
    def test_get_response(self):
        client = APIClient()
        # login user
        client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = client.get('/finance-api/budget')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


    # post - post data then serialize data then save if valid
    def test_post_with_invalid_data(self):
        client = APIClient()
        client.login(username='testuser1', password='1X<ISRUkw+tuK')

        data = {
             'category': 'Entertainment', 
             'maximum': 900.56,
             'theme': '',
         }

        response = client.post('/finance-api/budget', data)
        # print(response.data)
        # add check for error* 
        self.assertEqual(response.status_code, 400)

    def test_post_with_valid_data(self):
        client = APIClient()
        client.login(username='testuser1', password='1X<ISRUkw+tuK')

        data = {
             'category': 'Entertainment', 
             'maximum': 900.56,
             'theme': '#626070',
         }

        response = client.post('/finance-api/budget', data)

        self.assertEqual(response.status_code, 201)             
         
             


# budget detail view
class BudgetDetailViewTest(TestCase):
    ...


# pot list view



# pot detail view



# transaction list view