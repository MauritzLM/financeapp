from django.shortcuts import render
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import TransactionSerializer, BudgetSerializer, PotSerializer
from .models import Transaction, Budget, Pot
from knox.auth import TokenAuthentication
from .helpers import get_sort_str

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
        
        # calculate budget spending
        budget_spending = {}
        # get all budget categories
        for budget in budgets:
            budget_spending[f'{budget.category}'] = 0
        
        # using budget category loop over transactions (might have to filter further using date*)
        for key in budget_spending:
            for transaction in transactions:
                if key == transaction.category:
                    budget_spending[f'{key}'] += transaction.amount

        # 5 recent transactions
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
                          'recurring_bills': recurring_serializer.data,
                          'budget_spending': budget_spending
                        }, status=status.HTTP_200_OK) 
    

class BudgetListView(APIView):
    # check if user is authenticated
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # get all budgets of user & budget spending
        budgets = Budget.objects.filter(user = request.user.id)
        transactions = Transaction.objects.filter(user=request.user.id)
        # calculate budget spending
        budget_spending = {}
        # get all budget categories
        for budget in budgets:
            budget_spending[f'{budget.category}'] = 0
        
        # using budget category loop over transactions (migth have to filter further using date*)
        for key in budget_spending:
            for transaction in transactions:
                if key == transaction.category:
                    budget_spending[f'{key}'] += transaction.amount

        serializer = BudgetSerializer(budgets, many=True)

        return Response({'budgets': serializer.data, 'budget_spending': budget_spending}, status=status.HTTP_200_OK)
    
    # CREATE NEW
    def post(self, request, *args, **kwargs):
        # create object from request
        data = {
            'category': request.data.get('category'), 
            'maximum': float(request.data.get('maximum')) * 100,
            'theme': request.data.get('theme'), 
            'user': request.user.id
        }

        serializer = BudgetSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        

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
        
        budget_instance = self.get_object(budget_id, request.user.id)

        if not budget_instance:
            return Response(
                { 'message': 'Object with budget id does not exists' }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'category': request.data.get('category'), 
            'maximum': float(request.data.get('maximum')) * 100,
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

        budget_instance = self.get_object(budget_id, request.user.id)

        if not budget_instance:
            return Response(
                { 'message': 'Object with budget id does not exist' }, 
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

    def get(self, request, category, *args, **kwargs):
        spending = Transaction.objects.filter(user=request.user.id, category=category).order_by('-date')[:3]

        serializer = TransactionSerializer(spending, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class NewBudgetSpendingView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, category, *args, **kwargs):
        spending = Transaction.objects.filter(user=request.user.id, category=category)

        budget_spending = {}
        budget_spending[category] = 0

        for transaction in spending:
            if category == transaction.category:
                budget_spending[category] += transaction.amount

        return Response(budget_spending, status=status.HTTP_200_OK)             


class TransactionListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, search_term, category, sort_by, page, *args, **kwargs):
        try:
            # sort by
            sort = get_sort_str(sort_by)

            transactions = Transaction.objects.filter(user=request.user.id).order_by(sort)

            # empty search and specific category
            if search_term == 'empty' and category != 'All':
                transactions = transactions.filter(category=category)    
            
            # with search term
            if search_term != 'empty':
                # all categories
                if category == 'All':
                    transactions = transactions.filter(name__icontains=search_term)
                    
                # specific category
                if category != 'All':
                    transactions = transactions.filter(category=category, name__icontains=search_term)

            # 10 transactions per page
            paginator = Paginator(transactions, 10)
            page_obj = paginator.page(page) 
            
            serializer = TransactionSerializer(page_obj, many=True)

            return Response({ 'page_list': serializer.data, 'num_pages': paginator.num_pages }, status=status.HTTP_200_OK)
        
        except:
            return Response({ 'page_list': [], 'num_pages': 0 }, status=status.HTTP_204_NO_CONTENT)


class TransactionSearchView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, sort_by, page, search_term, *args, **kwargs):
        try:
            sort = get_sort_str(sort_by)

            transactions = Transaction.objects.filter(user=request.user.id).order_by(sort)
            
            if search_term != 'empty':
                transactions = Transaction.objects.filter(user=request.user.id, name__icontains=search_term).order_by(sort)

            # 10 transactions per page
            paginator = Paginator(transactions, 10)
            page_obj = paginator.page(page) 
            
            serializer = TransactionSerializer(page_obj, many=True)
        
            return Response({ 'page_list': serializer.data, 'num_pages': paginator.num_pages }, status=status.HTTP_200_OK)
        
        except:
            return Response({ 'page_list': [], 'num_pages': 0 }, status=status.HTTP_204_NO_CONTENT)   


class RecurringTransactionsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        transactions = Transaction.objects.filter(user=request.user.id)
        recurring_bills = transactions.filter(recurring=True)

        serializer = TransactionSerializer(recurring_bills, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PotListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # get all pots of user
        pots = Pot.objects.filter(user = request.user.id)
        serializer = PotSerializer(pots, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # CREATE NEW
    def post(self, request, *args, **kwargs):
        
        data = {
            'name': request.data.get('name'), 
            'target': float(request.data.get('target')) * 100,
            'total': float(request.data.get('total')) * 100,
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

    # helper method to get budget instance
    def get_object(self, pot_id, user_id):
            try:
                return Pot.objects.get(id=pot_id,  user=user_id)
            except Pot.DoesNotExist:
                return None

    # GET
    def get(self, request, pot_id, *args, **kwargs):
       
        pot_instance = self.get_object(pot_id, request.user.id)

        if not pot_instance:
            return Response(
                { 'message': 'Object with pot id does not exist' },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PotSerializer(pot_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
    # UPDATE
    def put(self, request, pot_id, *args, **kwargs):
        
        pot_instance = self.get_object(pot_id, request.user.id)

        if not pot_instance:
            return Response(
                { 'message': 'Object with pot id does not exists' }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'name': request.data.get('name'), 
            'target': float(request.data.get('target')) * 100,
            'total': pot_instance.total,
            'theme': request.data.get('theme'), 
            'user': request.user.id
        }

        serializer = PotSerializer(pot_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pot_id, *args, **kwargs):

        pot_instance = self.get_object(pot_id, request.user.id)

        if not pot_instance:
            return Response(
                { 'message': 'Object with pot id does not exist' }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        pot_instance.delete()

        return Response(
            { 'message': 'Pot deleted!' },
            status=status.HTTP_200_OK
        )         


# withdraw from pot
class PotWithdrawView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pot_id, user_id):
        try:
            return Pot.objects.get(id=pot_id, user=user_id)
        except Pot.DoesNotExist:
            return None
        
    def put(self, request, pot_id, *args, **kwargs):

        pot_instance = self.get_object(pot_id, request.user.id)

        if not pot_instance:
            return Response(
                { 'message': 'Object with pot id does not exist' }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'name': pot_instance.name, 
            'target': pot_instance.target,
            'total': pot_instance.total - (float(request.data.get('amount')) * 100),
            'theme': pot_instance.theme, 
            'user': request.user.id
        }

        serializer = PotSerializer(pot_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
# add to pot
class PotAddView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pot_id, user_id):
        try:
            return Pot.objects.get(id=pot_id, user=user_id)
        except Pot.DoesNotExist:
            return None

    def put(self, request, pot_id, *args, **kwargs):
        
        pot_instance = self.get_object(pot_id, request.user.id)

        if not pot_instance:
            return Response(
                { 'message': 'Object with pot id does not exist' }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'name': pot_instance.name, 
            'target': pot_instance.target,
            'total': pot_instance.total + float(request.data.get('amount')) * 100,
            'theme': pot_instance.theme, 
            'user': request.user.id
        }

        serializer = PotSerializer(pot_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)