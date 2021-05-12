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
    tradingviewsignal,
    signal_top_gainers,
    signal_top_losers,
    top_losers_list,
    top_gainers_list,
    nsetop50list,
    bsetop30list,
    signal_nse_50,
    database,
    aliceblueallorderhistory

    )

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("",login_required(home),name="home"),
    path("data/",data,name="data"),
    path("signal/",login_required(signal),name="signal"),
    path("order_history/",login_required(order_history),name="order"),
    path("trade_history/",login_required(trade_history),name="trade"),
    path("source/",login_required(signal_source),name="source"),
    path("live_signal/<str:pk>/",login_required(live_signal),name="live"),
    path("api_login",login_required(loginwithapi),name="api"),
    path("indexquote/", nse_index_quote, name="indexquote"),
    path("nselotsize/", nse_lot_size, name="nselotsize"),
    path("tradingviewsignal/", tradingviewsignal, name="tradingviewsignal"),
    path("topgainersignal",signal_top_gainers,name="topgainersignal"),
    path("toplosersignal",signal_top_losers,name="toplosersignal"),
    path("toploserlist",top_losers_list,name="toploserlist"),
    path("topgainerlist",top_gainers_list,name="topgainerlist"),
    path("nse50",nsetop50list,name="nse50"),
    path("bse30",bsetop30list,name="bse30"),
    path("signalnse50",signal_nse_50,name="signalnse50"),
    path("database/", login_required(database), name="database"),
    path("history/",aliceblueallorderhistory,name="history")


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