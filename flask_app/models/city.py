from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class City:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    def __repr__(self):
        return f"ID: {self.id} City: {self.name}"

    # queries database and return all cities in database as instances of City class
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM weather.cities;"
        r = connectToMySQL('weather').query_db(query)
        cities_cls = []
        for one_city in r:
            cities_cls.append(cls(one_city))
        return cities_cls

    # inserts new city in database
    @classmethod
    def add_city(cls, data):
        # validation for existing city, check if city already exists in database
        query = "SELECT * FROM weather.cities;"
        all_cites = connectToMySQL('weather').query_db(query)
        name_lst = [city['name'] for city in all_cites]
        if data['name'] in name_lst:
            flash(f"{data['name'].title()} is already been tracked", 'duplicate-error')
            return
        query = "INSERT INTO weather.cities (name) VALUES (%(name)s);"
        r = connectToMySQL('weather').query_db(query, data)
        return r

    # deletes city from database
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM weather.cities WHERE id=%(id)s"
        r = connectToMySQL('weather').query_db(query, data)
        return r