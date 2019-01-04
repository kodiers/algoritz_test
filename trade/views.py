import json

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from chartjs.views.lines import BaseLineChartView

from .forms import RequestAlgoData
from .core.api_functions import get_prices
from .core.algo_functions import algo_result
from .models import RequestedAlgoData

# Create your views here.


def request_data_view(request):
    """
    Show and handle form for request algo data
    """
    if request.method == 'GET':
        form = RequestAlgoData()
        return render(request, 'request_algo_data.html', {'form': form})
    if request.method == 'POST':
        form = RequestAlgoData(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            signal = form.cleaned_data['signal']
            trade = form.cleaned_data['trade']
            prices = get_prices(ticker)
            try:
                [positions, PnL] = algo_result(signal, trade, prices)
                algo_data = RequestedAlgoData()
                algo_data.name = form.cleaned_data['algo_name']
                algo_data.ticker = ticker
                algo_data.positions = json.dumps(positions)
                algo_data.pnl = json.dumps(PnL)
                algo_data.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Algo data for {} requested and saved'.format(algo_data.name))
            except SystemExit:
                messages.add_message(request, messages.ERROR, 'Could not process data with this params')
        return render(request, 'request_algo_data.html', {'form': form})


class AlgoDataListView(ListView):
    """
    Show saved algos list
    """
    template_name = 'list_algo_data.html'
    queryset = RequestedAlgoData.objects.all()


class AlgoDataDetailView(DetailView):
    """
    Show charts for selected algo
    """
    template_name = 'detail_algo_data.html'
    queryset = RequestedAlgoData.objects.all()


class AlgoChartJSONView(BaseLineChartView):
    """
    Get data for selected algo
    """
    def dispatch(self, request, *args, **kwargs):
        self.algo = get_object_or_404(RequestedAlgoData, pk=kwargs.get('pk'))
        return super(AlgoChartJSONView, self).dispatch(request, *args, **kwargs)

    def get_labels(self):
        return self.algo.get_positions_as_python()

    def get_providers(self):
        return [self.algo.name]

    def get_data(self):
        return [self.algo.get_pnl_as_python()]
