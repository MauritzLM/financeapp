from django.urls import path
from .views import (
    BudgetListView, IndexView, PotListView, BudgetDetailView,
    BudgetSpendingView, NewBudgetSpendingView, TransactionListView, RecurringTransactionsView,
    TransactionSearchView, PotDetailView, PotAddView, PotWithdrawView, TransactionCreateView, TransactionDetailView
    ) 
from .auth_views import UserCreate, LoginAPI
from knox import views as knox_views

urlpatterns = [
    path('overview', IndexView.as_view()),
    path('users', UserCreate.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', knox_views.LogoutView.as_view()),
    path('budgets', BudgetListView.as_view()),
    path('pots', PotListView.as_view()),
    path('pots/<int:pot_id>', PotDetailView.as_view()),
    path('pots/withdraw/<int:pot_id>', PotWithdrawView.as_view()),
    path('pots/add/<int:pot_id>', PotAddView.as_view()),
    path('budgets/<int:budget_id>', BudgetDetailView.as_view()),
    path('budgets/<str:category>', BudgetSpendingView.as_view()),
    path('budgets/new/<str:category>', NewBudgetSpendingView.as_view()),
    path('transactions/create', TransactionCreateView.as_view()),
    path('transactions/<int:t_id>', TransactionDetailView.as_view()),
    path('transactions/recurring', RecurringTransactionsView.as_view()),
    path('transactions/search/<str:search_term>/<str:sort_by>/<int:page>', TransactionSearchView.as_view()),
    path('transactions/<str:search_term>/<str:category>/<str:sort_by>/<int:page>', TransactionListView.as_view()),
]