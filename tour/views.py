from django.shortcuts import render
import tour.data as data
from django.http import HttpResponse, HttpResponseNotFound
# Create your views here.
def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')

def main_view(request):
    context = {
        'title': data.title,
        'subtitle': data.subtitle,
        'tours': data.tours,
        'departures': data.departures,
        'description': data.description,
    }
    return render(request, 'index.html', context = context)
def name_without_preposition(str):
    mas = []
    last_place = -1
    for i in range(len(str)):
        if str[i] == " ":
            mas.append(str[last_place + 1:i])
            last_place = i
        elif i == len(str) - 1:
            mas.append(str[last_place + 1:i + 1])
    return mas
def departure_view(request, city):
    if city not in data.departures.keys():
        return HttpResponseNotFound('Такого города нет, лошок')
    else:
        mas = name_without_preposition(data.departures[city])
        count_tours = 0
        mas_tours = {}
        flag = True
        for key,value in data.tours.items():
            if value['departure'] == city:
                count_tours += 1
                if flag:
                    min_price = value['price']
                    max_price = value['price']
                    min_night = value['nights']
                    max_night = value['nights']
                    flag = False
                if value['price'] < min_price:
                    min_price = value['price']
                if value['price'] > max_price:
                    max_price = value['price']
                if value['nights'] < min_night:
                    min_night = value['nights']
                if value['nights'] > max_night:
                    max_night = value['nights']
                mas_tours[key] = value
        context = {
            'title': data.title,
            'tours': data.tours,
            'city': city,
            'departures': data.departures,
            'name_city': mas[1],
            'count_tours': count_tours,
            'min_price': min_price,
            'max_price': max_price,
            'min_night': min_night,
            'max_night': max_night,
            'mas_tours': mas_tours,
        }
        return render(request, 'departure.html', context=context)

def tour_view(request, city, tour):
    print(tour, type(tour))
    if city not in data.departures.keys():
        return HttpResponseNotFound('Такого города нет, лошок')
    if tour not in data.tours.keys():
        return HttpResponseNotFound('Такого тура нет, лошок')
    mas = name_without_preposition(data.departures[city])
    stars = '★' * int(data.tours[tour]['stars'])
    konch = ''
    countN = str(data.tours[tour]['nights'])
    if countN[-1] == '1' and countN != '11':
        konch = 'ь'
    elif int(countN[-1]) <= 4 and countN[-1] != '0' and countN != '11' and countN != '12' and countN != '13' and countN != '14':
        konch = 'и'
    elif int(countN[-1]) >= 5 or countN[-1] =='0' or countN == '11' or countN == '12' or countN == '13' or countN == '14':
        konch = 'ей'
    context = {
        'title': data.title,
        'tours': data.tours,
        'city': city,
        'departures': data.departures,
        'name_city': mas[1],
        'about_tour': data.tours[tour],
        'stars': stars,
        'konch': konch,
    }


    return render(request, 'tour.html', context=context)