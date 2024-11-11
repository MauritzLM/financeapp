from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import TransactionSerializer, BudgetSerializer, PotSerializer
from .models import Transaction, Budget, Pot
from knox.auth import TokenAuthentication

# Create your views here.
# Overview page
class IndexView(APIView):
    # check if user is authenticated
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # get content of overview page
        # pots and budget
        pots = Pot.objects.filter(user=request.user.id)
        budgets = Budget.objects.filter(user=request.user.id)

        # transactions
        transactions = Transaction.objects.filter(user=request.user.id)
        # 5 recent
        recent_transactions = transactions.order_by('-date')[:5] 
        # expenses
        expenses = transactions.filter(amount__lt=0)
        # income
        income = transactions.filter(amount__gt=0)
        # recurring bills
        recurring_bills = transactions.filter(recurring=True)
        
        # pots and budget serializing
        pots_serializer = PotSerializer(pots, many=True)
        budgets_serializer = BudgetSerializer(budgets, many=True)

        # transactions serializing  
        recent_serializer = TransactionSerializer(recent_transactions, many=True)
        expenses_serializer = TransactionSerializer(expenses, many=True)
        income_serializer = TransactionSerializer(income, many=True)
        recurring_serializer = TransactionSerializer(recurring_bills, many=True)


        return Response({ 'pots': pots_serializer.data,
                          'budgets': budgets_serializer.data,
                          'income': income_serializer.data,
                          'expenses': expenses_serializer.data,
                          'recent_transactions': recent_serializer.data,
                          'recurring_bills': recurring_serializer.data
                        }, status=status.HTTP_200_OK) 
    

class BudgetListView(APIView):
    # check if user is authenticated
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        # get all budgets of user
        budgets = Budget.objects.filter(user = request.user.id)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # CREATE NEW
    def post(self, request, *args, **kwargs):
        # create object from request
        data = {
            'category': request.data.get('category'), 
            'maximum': request.data.get('maximum'),
            'theme': request.data.get('theme'), 
            'user': request.user.id
        }

        serializer = BudgetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BudgetDetailView(APIView):
    # check if user is authenticated
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    # helper method to get budget instance
    def get_object(self, budget_id, user_id):
            try:
                return Budget.objects.get(id=budget_id,  user=user_id)
            except Budget.DoesNotExist:
                return None

    # GET
    def get(self, request, budget_id, *args, **kwargs):
       
        budget_instance = self.get_object(budget_id, request.user.id)

        if not budget_instance:
            return Response(
                { 'message': 'Object with budget id does not exist' },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BudgetSerializer(budget_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
    # UPDATE
    def put(self, request, budget_id, *args, **kwargs):
        
        budget_instance = self.get_object(budget_id, request.user_id)

        if not budget_instance:
            return Response(
                { 'message': 'Object with budget id does not exists' }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'category': request.data.get('category'), 
            'maximum': request.data.get('maximum'),
            'theme': request.data.get('theme'), 
            'user': request.user.id
        }

        serializer = BudgetSerializer(budget_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, budget_id, *args, **kwargs):

        budget_instance = self.get_object(budget_id, request.user_id)

        if not budget_instance:
            return Response(
                { 'message': 'Object with budget id does not exists' }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        budget_instance.delete()

        return Response(
            { 'message': 'Budget deleted!' },
            status=status.HTTP_200_OK
        )   

class BudgetSpendingView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, category,*args, **kwargs):
        spending = Transaction.objects.filter(user=request.user.id, category=category).order_by('-date')[:3]

        serializer = TransactionSerializer(spending, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        ...
        # get transactions (paginated) of user*
        return Response({ 'message': 'transaction get view' })


class PotListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        ...
        # get all pots of user
        pots = Pot.objects.filter(user = request.user.id)
        serializer = PotSerializer(pots, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        
        data = {
            'name': request.data.get('name'), 
            'target': request.data.get('target'),
            'total': request.data.get('total'),
            'theme': request.data.get('theme'), 
            'user': request.user.id
        }

        serializer = PotSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class PotDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get():
        ...



    def put():
        ...



    def delete():
        ...        



# add / withdraw from pot*
class PotWithdrawView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def put():
        ...

class PotAddView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def put():
        ...