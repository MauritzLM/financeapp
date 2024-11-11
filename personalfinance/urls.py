from django.urls import path

from .views import BudgetListView, IndexView, PotListView, BudgetDetailView, BudgetSpendingView
from .auth_views import UserCreate

urlpatterns = [
    path('overview', IndexView.as_view()),
    path('users', UserCreate.as_view()),
    path('budget', BudgetListView.as_view()),
    path('pot', PotListView.as_view()),
    path('budget/<int:budget_id>', BudgetDetailView.as_view()),
    path('budget/<str:category>', BudgetSpendingView.as_view()),
]