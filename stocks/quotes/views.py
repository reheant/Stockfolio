from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm
from .models import Stock
import logging


def home(request):
    # pk_f6a0a38865df4ab8a67f6c96e3acf604
    # sk_c483d3953a954378b635026a08c4e040

    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        # api_request_prices = requests.get(
        #     'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey=4DVZB2KRL6NTL6OX')
        api_request_prices = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ ticker +'&apikey=VG2HN0RG5GY8TACN')
        try:

            api = json.loads(api_request_prices.content)

        except Exception as e:

            api = 'Error'

        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'ticker': "Enter a ticker symbol"})


# print("IUEHRFOIUHERFIOHEROIFUHOERIHUFOIEHRUFOIHUERFIE")


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):

    import requests
    import json

    if request.method == 'POST':

        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been Added"))
            return redirect('add_stock')

    else:

        ticker = Stock.objects.all()

        if request.method == 'POST':

            ticker = request.POST['ticker']

        output = []

        for value in ticker:

            # api_request_prices = requests.get(
            #     'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=4DVZB2KRL6NTL6OX')

            api_request_prices = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=VG2HN0RG5GY8TACN')

            try:
                api = json.loads(api_request_prices.content)
                output.append(api)

            except Exception as e:

                api = 'Error'

        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):

    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Successfully deleted"))
    return redirect(add_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})
