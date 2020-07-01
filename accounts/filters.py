import django_filters 
from .models import Order 

class OrderFilter(django_filters.FilterSet):
    # add more filtering options.
    start_date = django_filters.DateFilter(field_name='date_created', lookup_expr='gte')
    note = django_filters.CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ['customer', 'date_created']