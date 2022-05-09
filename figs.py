import plotly as py
import plotly.graph_objects as go
import json
import pandas as pd
import sqlite3


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

def get_table_with_dropdown_menu():
    dat = sqlite3.connect('products.db')
    query = dat.execute('SELECT * FROM products')
    cols = [column[0] for column in query.description]
    results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    dat.close()

    results = results.drop(columns=['Measure_kkal', 'Measure_prot', 'Measure_fats', 'Measure_carb'])

    fig = go.Figure(go.Table(header={'values': results.columns}, cells={'values': results.T.values}))

    fig.update_layout(
        updatemenus=[
            {
                'buttons': [
                    {
                        'label': c,
                        'method': 'update',
                        'args': [
                            {
                                'cells': {
                                    'values': results.T.values
                                    if c == 'ALL'
                                    else results.loc[results['Type'].eq(c)].T.values
                                }
                            }
                        ],
                    }
                    for c in ['All'] + results['Type'].unique().tolist()
                ],
                "x": 0,
                "xanchor": "left",
                "y": 1.2,
                "yanchor": "top"
            }
        ]
    )
    #    fig.show()
    graphJSON = json.dumps(fig, cls=py.utils.PlotlyJSONEncoder)

    return graphJSON