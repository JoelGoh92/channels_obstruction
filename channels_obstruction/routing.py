from channels.routing import route, route_class
from channels.staticfiles import StaticFilesConsumer
from game import consumers

# routes defined for channel calls
# this is similar to the Django urls, but specifically for Channels
channel_routing = [
    route_class(consumers.LobbyConsumer, path=r"^/lobby/"),
    route_class(consumers.GameConsumer, path=r"^/game/(?P<game_id>\d+)/$")
]