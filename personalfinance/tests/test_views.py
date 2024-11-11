from django.test import TestCase
from rest_framework.test import APIClient
from personalfinance.models import Budget, Transaction, Pot

from django.contrib.auth import get_user_model
User = get_user_model()


# index view test
class IndexViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/')
        self.assertEqual(response.status_code, 200)


# budget list view
class BudgetListViewTest(TestCase):
     
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Budget.objects.create(category='Entertainment', maximum=400.00, theme='#277C78', user=self.test_user1)
        Budget.objects.create(category='Personal care', maximum=200.00, theme='#626070', user=self.test_user1)
     
    def test_user_not_logged_in(self):
        client = APIClient()
        response = client.get('/finance-api/budget')
        self.assertEqual(response.status_code, 401)

    # get - all budgets of user then serialize then response = serialized data
    def test_get_response(self):
        client = APIClient()
        # login user
        client.force_authenticate(self.test_user1)
        
        response = client.get('/finance-api/budget')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


    # post - post data then serialize data then save if valid
    def test_post_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

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
        client.force_authenticate(self.test_user1)

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
    # url exists

    # user not logged in

    # get -> no instance found 400, success 200

    # put -> no instance found 400, success 200

    # delete -> no instance found 400, success 200


# pot list view
class PotListViewTest(TestCase):
    ...
    # url

    # user not logged in

    # get -> status & len 

    # post -> valid data, invalid data



# pot detail view
class PotDetailView(TestCase):
    ...
    # url exists

    # user not logged in

    # get -> no instance found 400, success 200

    # put -> no instance found 400, success 200

    # delete -> no instance found 400, success 200

# pot status view
class PotStatusViewTest(TestCase):
    ...

    # url

    # user not logged in

    # put -> withdraw, add, valid/invalid

# transaction list view
class TransactionListView(TestCase):
    ...

    # url

    # user not logged in

    # get -> status & pagination
