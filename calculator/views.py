from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from calculator.models import Asset, AssetDateValue, PreviousSearch
from django.db.models import Q
from django.core import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from config import CONFIG
import datetime
import traceback
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
        result = self.calculate_result(monthly, start_date, ticker)
        return JsonResponse(result, safe=False)

    def calculate_result(self, monthly, start_date, ticker):
        historic_data = AssetDateValue.objects \
            .filter(asset__ticker__iexact=ticker) \
            .filter(date__gte=start_date).order_by('date')
        cash = 0
        number_of_shares = 0
        total_invested = 0
        result = []
        for row in historic_data:
            cash += monthly
            total_invested += monthly
            bought_then = 0
            adjusted_bought = 0
            if row.close > 0 and row.adjusted_close > 0:
                adjustment_ratio = row.close / row.adjusted_close
                if adjustment_ratio == 0:
                    adjustment_ratio = 1
                if cash > row.close:
                    bought_then = cash // row.close
                    cash -= bought_then * row.close
                    adjusted_bought = bought_then * adjustment_ratio
                    number_of_shares += adjusted_bought
                result_row = {
                    'date': row.date,
                    'cash': cash,
                    'total_invested': total_invested,
                    'bought_then': bought_then,
                    'adjusted_bought': adjusted_bought,
                    'total_number_of_shares': number_of_shares,
                    'value_of_shares': number_of_shares / adjustment_ratio * row.close,
                    'portfolio_value': number_of_shares / adjustment_ratio * row.close + cash,
                    'close': row.close,
                    'adjusted_close': row.adjusted_close,
                    'ticker': ticker
                }
                result.append(result_row)
        return result

    def determine_start_date(self, request):
        default_start = datetime.date.today()
        default_start = str(default_start.replace(year=default_start.year - 10))
        start_date = request.GET.get('start', default_start)
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        return start_date

    def update_historic_data(self, ticker):
        asset = Asset.objects.get(ticker__iexact=ticker)
        three_days_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).date()
        if asset.last_update is None or asset.last_update < three_days_ago:
            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={}&apikey={}'
            url = url.format(ticker, CONFIG.alpha_vantage_key)
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    alpha_vantage_data = response.json()['Monthly Adjusted Time Series']
                    self.delete_redundant_data(alpha_vantage_data, ticker)
                    self.save_new_data(alpha_vantage_data, asset)
                except (ValueError, KeyError):
                    print('failed to update historic data at : {}'.format(url))

    def save_new_data(self, alpha_vantage_data, asset):
        existing_dates = AssetDateValue.objects \
            .filter(asset__ticker__iexact=asset.ticker) \
            .values_list('date', flat=True)
        for key, value in alpha_vantage_data.items():
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
        try:
            if self.should_search_for(search_string=search):
                url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords="{}"&apikey={}'
                url = url.format(search, CONFIG.alpha_vantage_key)
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()['bestMatches']
                    existing_tickers = Asset.objects.all().values_list('ticker', flat=True)
                    for row in data:
                        if row['1. symbol'] not in existing_tickers:
                            new = Asset()
                            new.ticker = row['1. symbol']
                            new.name = row['2. name']
                            new.save()
                            result.append(new)
                    searches = PreviousSearch.objects.filter(search__iexact=search)
                    found_search = searches[0]
                    found_search.search_date = datetime.datetime.now().date()
                    found_search.save()
        except:
            traceback.print_exc()
        serialized = serializers.serialize('json', result)
        return HttpResponse(serialized, content_type='application/json')

    def should_search_for(self, search_string):
        searches = PreviousSearch.objects.filter(search__iexact=search_string)
        if len(searches) == 0:
            new_search = PreviousSearch()
            new_search.search = search_string
            new_search.save()
            return True
        else:
            found_search = searches[0]
            thirty_days_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).date()
            if found_search.search_date and found_search.search_date < thirty_days_ago:
                return True
            else:
                return False
