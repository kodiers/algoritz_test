from django.urls import path


from .apps import TradeConfig
from .views import request_data_view, AlgoDataListView, AlgoChartJSONView, AlgoDataDetailView


app_name = TradeConfig.name


urlpatterns = [
    path('', request_data_view, name='request_data'),
    path('list/', AlgoDataListView.as_view(), name='algos_list'),
    path('detail/<int:pk>/', AlgoDataDetailView.as_view(), name='algo_detail'),
    path('chart_data/<int:pk>/', AlgoChartJSONView.as_view(), name='algo_chart')
]
