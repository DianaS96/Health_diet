import plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pandas as pd


def get_PFC_stat_daily(sum_prot, sum_fats, sum_co2, date):
    sum_PFC = sum_prot + sum_fats + sum_co2

    labels = ['Proteins', 'Fats', 'Carbohydrates']
    values = [(round(float(sum_prot / sum_PFC), 2)),
              (round(float(sum_fats / sum_PFC), 2)),
              (round(float(sum_co2 / sum_PFC), 2))]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text=f"Breakdown by PFC as of {date}",
                      paper_bgcolor="rgba(255, 255, 255, 0)",
                      plot_bgcolor="rgba(255, 255, 255, 0)")
    graphJSON = json.dumps(fig, cls=py.utils.PlotlyJSONEncoder)

    return graphJSON


def get_stats_by_type_daily(type_amount_per_day, date):
    df_type = pd.DataFrame(data=type_amount_per_day, columns=['Type', 'Amount'])
    print(df_type)

    fig = go.Figure(data=[go.Pie(labels=df_type['Type'],
                                 values=df_type['Amount'],
                                 hole=.3,
                                 name='Breakdown by type of product',
                                 hoverinfo="label+percent+name")])

    #        fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(title_text=f"Breakdown by type of product as of {date}",
                      paper_bgcolor="rgba(255, 255, 255, 0)",
                      plot_bgcolor="rgba(255, 255, 255, 0)")

    graphJSON = json.dumps(fig, cls=py.utils.PlotlyJSONEncoder)

    return (graphJSON)