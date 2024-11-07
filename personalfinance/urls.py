from django.urls import path

from .views import BudgetListView, IndexView, PotListView, BudgetDetailView

urlpatterns = [
    path('', IndexView.as_view()),
    path('budget', BudgetListView.as_view()),
    path('pot', PotListView.as_view()),
    path('budget/<int:budget_id>/', BudgetDetailView.as_view()),
]