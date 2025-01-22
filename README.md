## Finance app API

  - Built using [django-rest-framework](https://www.django-rest-framework.org/)
  - [rest-knox](https://jazzband.github.io/django-rest-knox/) for authentication
  - hosted on [railway](https://railway.com/)
  - [Frontend repo](https://github.com/MauritzLM/finance-app-client)

### Models

  - transactions

  - pots

  - budgets

### Views
#### index

  - Gets all user pots and budgets
  - 5 most recent transactions
  - Creates budgets spending object and calculates budgets spending for each budget
  - Calculates income and expenses    

#### budget list

  - Get method: gets all user budgets and calculates budget spending
  - Post method: create a new budget 

#### budget detail

  - Get method: gets a specific budget by id
  - Put method: update a budget
  - Delete method: delete a budget 

#### budget spending

  - Gets the three most recent transactions of a particular budget (transaction category)

### new budget spending

  - Calculates the budget spending amount of a newly created budget 

### transaction list
  
  - Gets a paginated list of transactions based on sort, search term and category

#### transaction search
  
  - Gets a paginated list of transactions based on search term and sort

#### recurring transactions
  
  - Gets all recurring transactions

#### pot list

  - Get method: gets all user pots
  - Post method: create a new pot 

#### pot detail
  
  - Get method: gets a specific pot
  - Put method: update a pot
  - Delete method: delete a pot

#### pot withdraw

  - Put method: withdraw from a pot total 

#### pot add

  - Put method: add to a pot total
