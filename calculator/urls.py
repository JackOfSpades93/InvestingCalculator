from django.urls import path
import calculator.views as views

urlpatterns = [
    path('', views.random_json_response),
    path('hello', views.hello_world),
    path('search', views.SearchAsset.as_view()),
    path('calculate', views.Calculate.as_view())

]
