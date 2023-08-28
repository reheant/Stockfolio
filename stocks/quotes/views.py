from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm
from .models import Stock
import matplotlib as plt
import logging


def home(request):
    #OG: 4DVZB2KRL6NTL6OX

    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request_prices = requests.get(
            'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=XJ3MJQWE2LQS5DLL')
        api_request_data = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol='+ ticker +'&apikey=XJ3MJQWE2LQS5DLL')
        date_x = []
        price_y = []

        try:

            api = json.loads(api_request_data.content)

            api_price = json.loads(api_request_prices.content)
            api_price = api_price["Time Series (Daily)"]
            for date in api_price:
                date_x.append(date)
                price_y.append(api_price[date]['4. close'])





        except Exception as e:

            api = 'Error'
        return render(request, 'home.html', {'api': api, 'api_price': price_y, 'api_date': date_x,})

    else:
        return render(request, 'home.html', {'ticker': "Enter a ticker symbol"})




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
            value = str(value)
            api_request_prices = requests.get(
                'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + value + '&apikey=XJ3MJQWE2LQS5DLL')

            api_request_data = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + value + '&apikey=XJ3MJQWE2LQS5DLL')

            try:
                api = json.loads(api_request_data.content)
                api_price = json.loads(api_request_prices.content)
                api['price'] = api_price['Global Quote']['05. price']
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
