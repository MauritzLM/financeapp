from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import UserSerializer, GroupSerializer, TransactionSerializer, BudgetSerializer, PotSerializer
from .models import Transaction, Budget, Pot

# Create your views here.
from django.http import HttpResponse


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class IndexView(APIView):
    # check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ...
        # get content of overview page
        return Response({'message': 'hello'}) 
    

class BudgetListView(APIView):
    # check if user is authenticated
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
                {'message': 'Object with budget id does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BudgetSerializer(budget_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    
    # UPDATE
    def put(self, request, budget_id, *args, **kwargs):
        
        budget_instance = self.get_object(budget_id, request.user_id)

        if not budget_instance:
            return Response(
                {'message': 'Object with budget id does not exists'}, 
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
                {'message': 'Object with budget id does not exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        budget_instance.delete()

        return Response(
            {'message': 'Budget deleted!'},
            status=status.HTTP_200_OK
        )   


class TransactionListView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        ...
        # get transactions (paginated) of user
        return Response({'message': 'transaction get view'})


class PotListView(APIView):

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
        
        

