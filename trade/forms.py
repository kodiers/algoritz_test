from django import forms


class RequestAlgoData(forms.Form):
    """
    Request algo data form
    """
    algo_name = forms.CharField(max_length=255, label='Algo name')
    signal = forms.CharField(max_length=120, label='Signal')
    trade = forms.CharField(max_length=120, label='Trade')
    ticker = forms.CharField(max_length=80, label='Ticker')
