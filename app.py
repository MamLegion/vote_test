from flask import Flask, request, render_template, url_for
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json

app = Flask(__name__)
app.debug = True

USERS = {
    '1': {'name': '钢弹', 'count': 0},
    '2': {'name': '铁锤', 'count': 0},
    '3': {'name': '贝贝', 'count': 100},
}

WEBSOCKET_LIST = []


@app.route('/index', methods=['GET'])
def index():
    return render_template('websocket.html', users=USERS)


@app.route('/message')
def message():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        return None
    WEBSOCKET_LIST.append(ws)
    while True:
        cid = ws.receive()
        if not cid:
            WEBSOCKET_LIST.remove(ws)
            break
        old = USERS[cid]['count']
        new = old + 1
        USERS[cid]['count'] = new
        for client in WEBSOCKET_LIST:
            client.send(json.dumps({'cid': cid, 'count': new}))


if __name__ == '__main__':
    http_server = WSGIServer(
        ('127.0.0.1', 5000),
        app,
        handler_class=WebSocketHandler
    )
    http_server.serve_forever()
