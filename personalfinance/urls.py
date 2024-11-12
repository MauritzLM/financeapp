from django.urls import path

from .views import BudgetListView, IndexView, PotListView, BudgetDetailView, BudgetSpendingView, TransactionListView, TransactionCategoryView, TransactionSearchView
from .auth_views import UserCreate

urlpatterns = [
    path('overview', IndexView.as_view()),
    path('users', UserCreate.as_view()),
    path('budget', BudgetListView.as_view()),
    path('pot', PotListView.as_view()),
    path('budget/<int:budget_id>', BudgetDetailView.as_view()),
    path('budget/<str:category>', BudgetSpendingView.as_view()),
    path('transactions/<str:sort_by>/<int:page>', TransactionListView.as_view()),
    path('transactions/category/<str:category>/<str:sort_by>/<int:page>', TransactionCategoryView.as_view()),
    path('transactions/search/<str:search_term>/<str:sort_by>/<int:page>', TransactionSearchView.as_view()),
]