from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Backtest, Metrics

# Vista simple
def index(request):
    return HttpResponse("Hello, this is Sancho, welcome to be my Quixote!")


# Vista para ver todos los Backtest
def bt_list(request):
    bts = Backtest.genboxbt.all()
    return render(request,
                  'sancho/backtest/list.html',
                  {'bts': bts})
    

# Vista para ver los detalles de un único BT
def bt_detail(request, bt_id: int):
    bt = get_object_or_404(Backtest,
                           id=bt_id,
                           status=Backtest.Source.GENBOX)
    return render(request,
                  'sancho/backtest/detail.html',
                  {'bt': bt})