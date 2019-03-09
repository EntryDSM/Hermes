from sanic import Sanic

from user.router import bp
from user.listner import initialize, destroy

app = Sanic(__name__)

app.blueprint(bp)

app.register_listener(initialize, 'before_server_start')
app.register_listener(destroy, 'after_server_stop')