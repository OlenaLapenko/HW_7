# 1. Створити клас Circle(x,y,radius). Додати метод contains.
# Цей метод приймає екземпляр класу Point(x,y). Цей метод має повертати
# True or False. Якшо точка в колі то True якшо поза колом то False.
import math
from flask import Flask, jsonify, request, render_template
from http import HTTPStatus
from databse_handler import execute_query


class Point:

    def __init__(self, x, y):
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.x = x
            self.y = y
        else:
            print('Values are not numeric!')


class Circle:

    def __init__(self, x, y, radius):
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(radius, (int, float)):
            self.x = x
            self.y = y
            self.radius = radius
        else:
            print('Values are not numeric!')

    def contains(self, point):
        if (math.sqrt((self.x - point.x) ^ 2 + (self.y - point.y) ^ 2)) > self.radius:
            return False
        else:
            return True


p1 = Point(100, 300)
c1 = Circle(1, 2, 3)
print(c1.contains(p1))

# 2. Вивести місто в якому найбільше слухають Hip Hop. Створити view і вивести в браузер.

app = Flask(__name__, static_url_path='/static')


@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handling(error):
    headers = error.data.get("headers", None)
    messages = error.data.get("messages", ["Invalid request."])

    if headers:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
            headers
        )
    else:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
        )


@app.route("/hiphop_page")
def hiphop_genre():
    query_hiphop = f'SELECT customers.City, COUNT(DISTINCT tracks.TrackId) ' \
        f'FROM customers ' \
        f'JOIN invoices ON invoices.CustomerId = customers.CustomerID ' \
        f'JOIN invoice_items ON invoice_items.InvoiceId = invoices.InvoiceId ' \
        f'JOIN tracks ON tracks.TrackId = invoice_items.TrackId ' \
        f'JOIN genres ON genres.GenreId = tracks.GenreId ' \
        f'WHERE genres.Name = \'Hip Hop/Rap\' GROUP BY City ORDER BY COUNT(DISTINCT tracks.TrackId) DESC'
    records_hiphop = execute_query(query=query_hiphop)
    if records_hiphop:
        cities = [records_hiphop[0][0],]
        for record in records_hiphop[1:]:
            if record[1] == records_hiphop[0][1]:
                cities.append(record[0])
    else:
        return ('Nobody listen such music',)
    return render_template('result.html', rezult=cities)


# *3. Замість Hip Hop щоб можна було використати будь який стиль.
# /stats_by_city?genre=HipHop

@app.route("/genre")
def popular_genre():
    genre = request.args.get('genre')
    genres_name = (genre,)
    if genre:
        query = f'SELECT customers.City, COUNT(DISTINCT tracks.TrackId) ' \
            f'FROM customers ' \
            f'JOIN invoices ON invoices.CustomerId = customers.CustomerID ' \
            f'JOIN invoice_items ON invoice_items.InvoiceId = invoices.InvoiceId ' \
            f'JOIN tracks ON tracks.TrackId = invoice_items.TrackId ' \
            f'JOIN genres ON genres.GenreId = tracks.GenreId ' \
            f'WHERE genres.Name = ? GROUP BY City ORDER BY COUNT(DISTINCT tracks.TrackId) DESC'
        records = execute_query(query, genres_name)
        if records:
            cities = [records[0][0], ]
            for record in records[1:]:
                if record[1] == records[0][1]:
                    cities.append(record[0])
            return render_template('result.html', rezult=cities)
        else:
            return 'Nobody listen such music'
    else:
        return render_template('result.html', rezult=('You have to enter a genre',))


app.run(debug=True, port=5000)

