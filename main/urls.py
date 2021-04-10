from django.urls import path,include
from .views import (
    home,
    signal,
    signal_source,
    nse_index_quote,
    nse_lot_size,
    order_history,
    trade_history,
    live_signal,
    loginwithapi,
    data,
    tradingviewsignal
    # database,


)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("",login_required(home),name="home"),
    path("data/",data,name="data"),
    path("signal/",login_required(signal),name="signal"),
    path("order_history/",login_required(order_history),name="order"),
    path("trade_history/",login_required(trade_history),name="trade"),
    path("source/",login_required(signal_source),name="source"),
    path("live_signal",login_required(live_signal),name="live"),
    path("api_login",login_required(loginwithapi),name="api"),
    path("indexquote/", nse_index_quote, name="indexquote"),
    path("nselotsize/", nse_lot_size, name="nselotsize"),
    path("tradingviewsignal/<str:pk>/", tradingviewsignal, name="tradingviewsignal")
    # path("database/", database, name="database")


]

# urlpatterns = [
#     path("",login_required(home),name="home"),
#     path("data/",data,name="data"),
#     path("signal/",login_required(signal),name="signal"),
#     path("order_history/",login_required(order_history),name="order"),
#     path("trade_history/",login_required(trade_history),name="trade"),
#     path("source/",login_required(signal_source),name="source"),
#     path("live_signal",login_required(live_signal),name="live"),
#     path("api_login",login_required(loginwithapi),name="api"),
#     path("indexquote/", nse_index_quote, name="indexquote"),
#     path("nselotsize/", nse_lot_size, name="nselotsize"),
#     path("database/", database, name="database")


# ]