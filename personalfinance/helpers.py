# get sort string
def get_sort_str(term):
    if term == 'Oldest':
        return 'date'
    if term == 'A-to-Z':
        return 'name'
    if term == 'Z-to-A':
        return '-name'
    if term == 'Highest':
        return 'amount'
    if term == 'Lowest':
        return '-amount'
    
    return '-date'