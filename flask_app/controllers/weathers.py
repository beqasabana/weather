from flask_app import app
from flask import render_template, request, redirect, flash
import requests
from flask_app.models.city import City


@app.route('/', methods=['GET', 'POST'])
def weather():
    API_KEY = ''
    api_url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}'
    
    # print(weather_data)
    if request.method == 'POST':
        # validates user input to check if city exists
        r = requests.get(api_url.format(city=request.form['city_name'], api_key=API_KEY)).json()
        if r['cod'] != 200:
            flash(f"{r['message'].title()} Error Code: {r['cod']}", 'error')
            return redirect('/')
        data = {
            'name': request.form['city_name']
        }
        City.add_city(data)
        return redirect('/')

    # get all cities from database
    cities = City.get_all()
    weather_data = []

    # calls API on all cities return from database
    for city in cities:
        r = requests.get(api_url.format(city=city.name, api_key=API_KEY)).json()
        weather_data_point = {
            'id': city.id,
            'name': r['name'],
            'temp': r['main']['temp'],
            'feels_like': r['main']['feels_like'],
            'temp_min': r['main']['temp_min'],
            'temp_max': r['main']['temp_max'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(weather_data_point)

    return render_template('weather.html', weather_data=weather_data)


@app.route('/delete/<int:id>/<string:name>')
def delete_city(id, name):
    data = {
        'id': id
    }
    City.delete(data)
    flash(f"{name} was successfully deleted.", 'delete-success')
    return redirect('/')