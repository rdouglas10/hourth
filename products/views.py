import json

import requests
from bs4 import BeautifulSoup

from django.shortcuts import render

from django.http import JsonResponse


def home(request):
    return render(request, "products/home.html")


def products_json(request):
    url = "https://pastebin.com/QfMiu1D7"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    string_single_quotes = soup.find('div', {'class': 'de1'})
    string_double_quotes = string_single_quotes.text.replace("'", '"')
    string_double_quotes = string_double_quotes.replace(": datetime", ': "datetime')
    string_double_quotes = string_double_quotes.replace("),", ')",')
    products = json.loads(string_double_quotes)

    list_product = []

    for x in range(0, len(products)):
        product_url_created_at = formated_string_date((products[x]['product_url__created_at']).replace("'", ""))
        consult_date = formated_string_date((products[x]['consult_date']).replace("'", ""))
        url_image = "<img src='%s' width='40px' height='40px'>" % products[x]['product_url__image']

        dict_product = {'product_url__image': url_image,
                        'product_url': products[x]['product_url'],
                        'product_url__created_at': product_url_created_at,
                        'consult_date': consult_date,
                        'c': products[x]['c']}

        list_product.append(dict_product)

    response = {
        "draw": 1,
        "recordsTotal": 20,
        "recordsFiltered": 20,
        'data': list_product
    }

    return JsonResponse(response)


def formated_string_date(consult_date):
    aux = consult_date.split("(")[1].split(')')
    string_date = str(aux[0]).split(',')
    day_format = str(string_date[2]).replace(" ", "")
    day = day_format.zfill(2) if len(day_format) < 2 else day_format
    month_format = str(string_date[1]).replace(" ", "")
    month = month_format.zfill(2) if len(month_format) < 2 else month_format
    year = string_date[0]
    return year + '-' + month + '-' + day
