import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}


app = Flask("DayNine")


@app.route('/')
def home():
    order_by = request.args.get('order_by')
    if order_by == 'popular' or order_by == 'new':
        pass
    else:
        order_by = 'popular'

    if db.get(order_by) is None:
        if order_by == 'popular':
            r = requests.get(popular)
        elif order_by == 'new':
            r = requests.get(new)
        else:
            r = requests.get(popular)
            order_by = 'popular'

        title = []
        url = []
        points = []
        author = []
        num_comments = []
        objectID = []

        r = r.json()

        for num, _ in enumerate(r['hits']):
            title.append(r['hits'][num]['title'])
            url.append(r['hits'][num]['url'])
            points.append(r['hits'][num]['points'])
            author.append(r['hits'][num]['author'])
            num_comments.append(r['hits'][num]['num_comments'])
            objectID.append(r['hits'][num]['objectID'])

        db[order_by] = {
            'title': title,
            'url': url,
            'points': points,
            'author': author,
            'num_comments': num_comments,
            'objectID': objectID
        }
    else:
        title = db[order_by]['title']
        url = db[order_by]['url']
        points = db[order_by]['points']
        author = db[order_by]['author']
        num_comments = db[order_by]['num_comments']
        objectID = db[order_by]['objectID']

    return render_template("index.html", title=title, url=url, points=points, author=author, num_comments=num_comments, objectID=objectID, order_by=order_by, zip=zip)


@app.route('/<objectID_item>')
def detail(objectID_item):
    r = requests.get(make_detail_url(objectID_item))

    r = r.json()

    title = r['title']
    points = r['points']
    author = r['author']
    url = r['url']
    comment_author = []
    comment_text = []

    for num, _ in enumerate(r['children']):
        comment_author.append(r['children'][num]['author'])
        comment_text.append(r['children'][num]['text'])

    return render_template('detail.html', title=title, points=points, author=author, url=url, comment_author=comment_author, comment_text=comment_text, zip=zip)


app.run(host="127.0.0.1")
