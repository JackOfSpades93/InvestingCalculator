from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from calculator.models import Asset, AssetDateValue
from django.db.models import Q
from django.core import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import datetime
import requests


# Create your views here.

def random_json_response(request):
    dic = {
        'hi': 'hello'
    }
    return JsonResponse(dic, safe=False)


def hello_world(request):
    today = datetime.datetime.now().date()
    return render(request, 'hello.html', {'today': today})


class Calculate(View):
    def get(self, request):
        ticker = request.GET.get('ticker', "AAPL")
        monthly = float(request.GET.get('monthly', "100"))
        start_date = self.determine_start_date(request)

        self.update_historic_data(ticker)
        return HttpResponse('ih')

    def determine_start_date(self, request):
        default_start = datetime.date.today()
        default_start = str(default_start.replace(year=default_start.year - 10))
        start_date = request.GET.get('start', default_start)
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        return start_date

    def update_historic_data(self, ticker):
        asset = Asset.objects.get(ticker__iexact=ticker)
        if asset.last_update is None or asset.last_update < (
                datetime.datetime.now() - datetime.timedelta(days=3)).date():
            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={}&apikey={}'.format(
                ticker, 'UNFVDVR01R2YAANJ')
            data = requests.get(url).json()['Monthly Adjusted Time Series']

            self.delete_redundant_data(data, ticker)
            existing_dates = AssetDateValue.objects.all().values_list('date', flat=True)
            for key, value in data.items():
                key_date = datetime.datetime.strptime(key, '%Y-%m-%d').date()
                if key_date not in list(existing_dates):
                    new = AssetDateValue()
                    new.asset = asset
                    new.date = key
                    new.open = value['1. open']
                    new.high = value['2. high']
                    new.low = value['3. low']
                    new.close = value['4. close']
                    new.adjusted_close = value['5. adjusted close']
                    new.volume = value['6. volume']
                    new.dividend = value['7. dividend amount']
                    print('saving {}'.format(new))
                    new.save()
            asset.last_update = datetime.datetime.now().date()
            asset.save()
        return asset

    def delete_redundant_data(self, data, ticker):
        stuff_to_delete = AssetDateValue.objects.filter(asset__ticker__iexact=ticker).exclude(date__in=data.keys())
        for asset_date_value in stuff_to_delete:
            print('deleting {}'.format(asset_date_value))
            asset_date_value.delete()


class SearchAsset(View):
    def post(self, request):
        search = request.POST.get('search', "")
        print('search is : {}'.format(search))
        result = list(Asset.objects.filter(Q(ticker__icontains=search) | Q(name__icontains=search)))
        serialized = serializers.serialize('json', result)
        return HttpResponse(serialized, content_type='application/json')
