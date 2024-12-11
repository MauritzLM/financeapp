from django.test import TestCase
from rest_framework.test import APIClient
from personalfinance.models import Budget, Transaction, Pot

from django.contrib.auth import get_user_model
User = get_user_model()


# index view test
class IndexViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        
        # test budgets
        Budget.objects.create(category='Entertainment', maximum=20000, theme='#277C78', user=self.test_user1)
        Budget.objects.create(category='Bills', maximum=70000, theme='#626070', user=self.test_user1)
        Budget.objects.create(category='Shopping', maximum=70000, theme='#626070', user=self.test_user1)
        # test transactions
        Transaction.objects.create(avatar='/imgurl', name='James Thompson', category='General', date='2024-07-12T13:40:46Z', amount=10000, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='EcoFuel Energy', category='Shopping', date='2024-07-30T13:20:14Z', amount=-3500, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Aqua Flow Utilities', category='Bills', date='2024-07-29T11:55:29Z', amount=-10000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Nimbus Data Storage', category='Bills', date='2024-07-21T10:05:42Z', amount=-999, recurring=True, user=self.test_user1)
        # test pots
        Pot.objects.create(name='Savings', target=200000, total=15000, theme='#277C78', user=self.test_user1) 
        
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/overview')
        self.assertEqual(response.status_code, 200)

    def test_user_not_logged_in(self):
        client = APIClient()
        response = client.get('/finance-api/overview')
        self.assertEqual(response.status_code, 401)    

    def test_get_response(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)
        
        response = client.get('/finance-api/overview')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(len(response.data['budgets']), 3)
        self.assertEqual(len(response.data['pots']), 1)
        self.assertEqual(len(response.data['recent_transactions']), 4)
        self.assertEqual(len(response.data['income']), 1)
        self.assertEqual(len(response.data['expenses']), 3)
        self.assertEqual(len(response.data['recurring_bills']), 2)
        self.assertEqual(response.data['budget_spending']['Shopping'], -3500)
        self.assertEqual(response.data['budget_spending']['Bills'], -10999)             

# budget list view
class BudgetListViewTest(TestCase):
     
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Budget.objects.create(category='Entertainment', maximum=40000, theme='#277C78', user=self.test_user1)
        Budget.objects.create(category='Personal care', maximum=20000, theme='#626070', user=self.test_user1)

    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets')
        self.assertEqual(response.status_code, 200)    
     
    def test_user_not_logged_in(self):
        client = APIClient()
        response = client.get('/finance-api/budgets')
        self.assertEqual(response.status_code, 401)

    
    def test_get_response(self):
        client = APIClient()
        # login user
        client.force_authenticate(self.test_user1)
        
        response = client.get('/finance-api/budgets')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


    # post -> create new budget
    def test_post_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        data = {
             'category': 'Entertainment', 
             'maximum': 900.56,
             'theme': '',
         }

        response = client.post('/finance-api/budgets', data)
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

        response = client.post('/finance-api/budgets', data)

        self.assertEqual(response.status_code, 201)             
         
             
# budget detail view
class BudgetDetailViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Budget.objects.create(category='Entertainment', maximum=40000, theme='#277C78', user=self.test_user1)
        Budget.objects.create(category='Personal care', maximum=20000, theme='#626070', user=self.test_user1)

    # url exists
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets/1')
        self.assertEqual(response.status_code, 200)

    # user not logged in
    def test_user_not_logged_in(self):
        client = APIClient()

        response = client.get('/finance-api/budgets/1')
        self.assertEqual(response.status_code, 401)

    # get
    def test_get_budget_found(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['maximum'], 40000)
        self.assertEqual(response.data['theme'], '#277C78')

    def test_get_budget_not_found(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets/100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Object with budget id does not exist')
    
    # put
    def test_put_with_valid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)
        
        data = {
            'category': 'Entertainment', 
            'maximum': 450,
            'theme': '#000', 
            'user': self.test_user1
        }

        response = client.put('/finance-api/budgets/1', data)
        self.assertEqual(response.status_code, 200)
        # updated fields
        self.assertEqual(response.data['maximum'], 45000)
        self.assertEqual(response.data['theme'], '#000')

    def test_put_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        data = {
            'category': 'Entertainment', 
            'maximum': 450,
            'theme': '', 
            'user': self.test_user1
        }
        
        response = client.put('/finance-api/budgets/1', data)
        # print(response.data)
        # add check for error*
        self.assertEqual(response.status_code, 400)
                
    # delete
    def test_delete_with_valid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.delete('/finance-api/budgets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Budget deleted!')


    def test_delete_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.delete('/finance-api/budgets/100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Object with budget id does not exist')    


# budget spending view
class BudgetSpendingViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        
        Transaction.objects.create(avatar='/imgurl', name='James Thompson', category='Bills', date='2024-07-12T13:40:46Z', amount=-9550, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='EcoFuel Energy', category='Bills', date='2024-07-30T13:20:14Z', amount=-3500, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Aqua Flow Utilities', category='Bills', date='2024-07-29T11:55:29Z', amount=-10000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Nimbus Data Storage', category='Bills', date='2024-07-21T10:05:42Z', amount=-999, recurring=True, user=self.test_user1)
        
    # url
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets/Bills')
        self.assertEqual(response.status_code, 200)

    # user not logged in
    def user_not_logged_in(self):
        client = APIClient()
        
        response = client.get('/finance-api/budgets/Bills')
        self.assertEqual(response.status_code, 401)

    # get
    def test_empty_category(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets/Empty')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_returns_only_three_objects(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets/Bills')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)


# new budget spending view
class NewBudgetSpendingViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        
        Transaction.objects.create(avatar='/imgurl', name='James Thompson', category='Bills', date='2024-07-12T13:40:46Z', amount=-9550, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='EcoFuel Energy', category='Bills', date='2024-07-30T13:20:14Z', amount=-3500, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Aqua Flow Utilities', category='Bills', date='2024-07-29T11:55:29Z', amount=-10000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Nimbus Data Storage', category='Bills', date='2024-07-21T10:05:42Z', amount=-999, recurring=True, user=self.test_user1)
        
    # url
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets/new/Bills')
        self.assertEqual(response.status_code, 200)

    # user not logged in
    def user_not_logged_in(self):
        client = APIClient()
        
        response = client.get('/finance-api/budgets/new/Bills')
        self.assertEqual(response.status_code, 401)

    # test spending amount
    def test_get_response_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/budgets/new/Bills')
        self.assertEqual(response.data['Bills'], -24049)      


# pot list view
class PotListViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Pot.objects.create(name='Savings', target=200000, total=15000, theme='#277C78', user=self.test_user1)
        Pot.objects.create(name='Gift', target=15000, total=11000, theme='#82C9D7', user=self.test_user1)

    # url
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/pots')
        self.assertEqual(response.status_code, 200)

    # user not logged in
    def test_user_not_logged_in(self):
        client = APIClient()
        
        response = client.get('/finance-api/pots')
        self.assertEqual(response.status_code, 401)

    # get -> status & len
    def test_get_response(self):
        client = APIClient()
        # login user
        client.force_authenticate(self.test_user1)
        
        response = client.get('/finance-api/pots')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    # post -> create new pot
    def test_post_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        data = {
             'name': 'New Laptop', 
             'target': 900,
             'total': 315,
             'theme': '',
         }

        response = client.post('/finance-api/pots', data)
        # print(response.data)
        # add check for error* 
        self.assertEqual(response.status_code, 400)

    def test_post_with_valid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        data = {
             'name': 'New Laptop', 
             'target': 900.00,
             'total': 315,
             'theme': '#F2CDAC',
         }

        response = client.post('/finance-api/pots', data)
        print(response.data)

        self.assertEqual(response.status_code, 201)


# pot detail view
class PotDetailViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Pot.objects.create(name='Savings', target=200000, total=15000, theme='#277C78', user=self.test_user1)

    # url exists
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/pots/1')
        self.assertEqual(response.status_code, 200)

    # user not logged in
    def test_user_not_logged_in(self):
        client = APIClient()

        response = client.get('/finance-api/pots/1')
        self.assertEqual(response.status_code, 401)

    # get
    def test_get_pot_found(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/pots/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Savings')
        self.assertEqual(response.data['target'], 200000)
        self.assertEqual(response.data['theme'], '#277C78')

    def test_get_pot_not_found(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/pots/100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Object with pot id does not exist')
    
    # put
    def test_put_with_valid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)
        
        data = {
            'name': 'Savings', 
            'target': 2100,
            'theme': '#82C9D7', 
            'user': self.test_user1
        }

        response = client.put('/finance-api/pots/1', data)
        self.assertEqual(response.status_code, 200)
        # updated fields
        self.assertEqual(response.data['target'], 210000)
        self.assertEqual(response.data['theme'], '#82C9D7')

    def test_put_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        data = {
            'name': 'Savings', 
            'target': -100,
            'theme': '#82C9D7', 
            'user': self.test_user1
        }
        
        response = client.put('/finance-api/pots/1', data)
        
        # add check for error*, empty name, negative target
        self.assertEqual(response.status_code, 400)
        # print(response.data)
        # self.assertEqual(response.data['name'][0], 'This field may not be blank')
        self.assertEqual(response.data['target'][0], 'Target can\'t be negative')
                
    # delete
    def test_delete_with_valid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.delete('/finance-api/pots/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Pot deleted!')


    def test_delete_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.delete('/finance-api/pots/100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Object with pot id does not exist')

# pot status view
class PotWithdrawViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Pot.objects.create(name='Savings', target=200000, total=15000, theme='#277C78', user=self.test_user1)

    # url exists
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/pots/withdraw/1')
        # no get method
        self.assertEqual(response.status_code, 405)

    # user not logged in
    def test_user_not_logged_in(self):
        client = APIClient()

        response = client.get('/finance-api/pots/withdraw/1')
        self.assertEqual(response.status_code, 401)

    # put
    def test_put_subtracts_amount_from_total(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)
        
        data = {
            'amount': 100,
        }

        response = client.put('/finance-api/pots/withdraw/1', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 5000)


    def test_amount_puts_total_below_zero_raises_validation_error(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)
        
        data = {
            'amount': 160,
        }

        response = client.put('/finance-api/pots/withdraw/1', data)
        # add check for error
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['total'][0], 'Total can\'t be negative')


class PotAddViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Pot.objects.create(name='Savings', target=200000, total=15000, theme='#277C78', user=self.test_user1)

    # url exists
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/pots/add/1')
        # no get method
        self.assertEqual(response.status_code, 405)

    # user not logged in
    def test_user_not_logged_in(self):
        client = APIClient()

        response = client.get('/finance-api/pots/add/1')
        self.assertEqual(response.status_code, 401)
    
    # put
    def test_put_adds_amount_to_total(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)
        
        data = {
            'amount': 100,
        }

        response = client.put('/finance-api/pots/add/1', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 25000)


    def test_amount_puts_target_above_total_raises_validation_error(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)
        
        data = {
            'amount': 2000,
        }

        response = client.put('/finance-api/pots/add/1', data)
        # add check for error
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['value'][0], 'Total can\'t be higher than target') 


# transaction list view
class TransactionListViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        
        # create 11 object to test pagination
        Transaction.objects.create(avatar='/imgurl', name='James Thompson', category='Bills', date='2024-07-12T13:40:46Z', amount=-9550, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='EcoFuel Energy', category='Bills', date='2024-07-30T13:20:14Z', amount=-3500, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Aqua Flow Utilities', category='Bills', date='2024-07-29T11:55:29Z', amount=-10000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Swift Ride Share', category='Transportation', date='2024-07-02T19:50:05Z', amount=-1650, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Serenity Spa & Wellness', category='Personal Care', date='2024-07-03T14:00:37Z', amount=-3000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Elevate Education', category='Education', date='2024-07-05T11:15:22Z', amount=-5000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='William Harris', category='General', date='2024-07-06T17:10:09Z', amount=2000, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Sebastian Cook', category='Transportation', date='2024-07-07T11:45:55Z', amount=-2000, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Mason Martinez', category='Lifestyle', date='2024-07-08T15:20:41Z', amount=-6500, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Sofia Peterson', category='Transportation', date='2024-07-09T08:55:27Z', amount=-1250, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Yuna Kim', category='Dining Out', date='2024-07-10T12:30:13Z', amount=-2750, recurring=False, user=self.test_user1)

    # url
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/All/Latest/1')
        self.assertEqual(response.status_code, 200) 
       
    # user not logged in
    def test_user_not_logged_in(self):
        client = APIClient()
        
        response = client.get('/finance-api/transactions/All/Latest/1')
        self.assertEqual(response.status_code, 401)

    # get
    def test_get_first_page_content_and_pagination(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/All/Latest/1')
        self.assertEqual(len(response.data['page_list']), 10)
        self.assertEqual(response.data['num_pages'], 2)

    def test_get_second_page_content_and_pagination(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/All/Latest/2')
        self.assertEqual(len(response.data['page_list']), 1)
        self.assertEqual(response.data['num_pages'], 2)
    
    def test_get_category_list(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/Transportation/Latest/1')
        self.assertEqual(len(response.data['page_list']), 3)
        self.assertEqual(response.data['num_pages'], 1)

    # test diff sort?* 

    def test_get_empty_page(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/All/Latest/3')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(response.data['page_list']), 0)
        self.assertEqual(response.data['num_pages'], 0)   


# transaction search  
class TransactionSearchViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Transaction.objects.create(avatar='/imgurl', name='Aqua Flow Utilities', category='Bills', date='2024-07-29T11:55:29Z', amount=-10000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Swift Ride Share', category='Transportation', date='2024-07-02T19:50:05Z', amount=-1650, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Serenity Spa & Wellness', category='Personal Care', date='2024-07-03T14:00:37Z', amount=-3000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Elevate Education', category='Education', date='2024-07-05T11:15:22Z', amount=-5000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='William Harris', category='General', date='2024-07-06T17:10:09Z', amount=2000, recurring=False, user=self.test_user1)
     
    # url
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/search/aqua/Latest/1')
        self.assertEqual(response.status_code, 200) 

    # user not logged in
    def test_user_not_logged_in(self):
        client = APIClient()
        
        response = client.get('/finance-api/transactions/search/aqua/Latest/1')
        self.assertEqual(response.status_code, 401)

    # get 
    def test_get_search_ignores_case(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/search/s/Latest/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['page_list']), 4)

    def test_get_no_matches(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/search/notfound/Latest/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['page_list']), 0)

    def test_get_empty_page(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/search/s/Latest/2')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(response.data['page_list']), 0)        


# recurring transactions view
class RecurringTransactionsViewTest(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        Transaction.objects.create(avatar='/imgurl', name='Aqua Flow Utilities', category='Bills', date='2024-07-29T11:55:29Z', amount=-10000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Swift Ride Share', category='Transportation', date='2024-07-02T19:50:05Z', amount=-1650, recurring=False, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Serenity Spa & Wellness', category='Personal Care', date='2024-07-03T14:00:37Z', amount=-3000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='Elevate Education', category='Education', date='2024-07-05T11:15:22Z', amount=-5000, recurring=True, user=self.test_user1)
        Transaction.objects.create(avatar='/imgurl', name='William Harris', category='General', date='2024-07-06T17:10:09Z', amount=2000, recurring=False, user=self.test_user1)
     
    # url
    def test_url_exists(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/recurring')
        self.assertEqual(response.status_code, 200) 

    # user not logged in
    def test_user_not_logged_in(self):
        client = APIClient()
        
        response = client.get('/finance-api/transactions/recurring')
        self.assertEqual(response.status_code, 401)

    def test_response_data(self):
        client = APIClient()
        client.force_authenticate(self.test_user1)

        response = client.get('/finance-api/transactions/recurring')
        self.assertEqual(len(response.data), 3)    