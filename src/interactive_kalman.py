# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import numpy as np

# Incorporate data
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

# Initialize the app
app = Dash()

# App layout
app.layout = html.Div(
    [
        html.Div(children="My First App with Data, Graph, and Controls"),
        html.Hr(),
        dcc.RadioItems(
            options=["pop", "lifeExp", "gdpPercap"],
            value="lifeExp",
            id="controls-and-radio-item",
        ),
        dash_table.DataTable(data=df.to_dict("records"), page_size=6),
        dcc.Graph(figure={}, id="controls-and-graph"),
        dcc.Graph(figure={}, id="line_plot"),
    ]
)

# Add controls to build the interaction


@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    return fig


@callback(
    Output(component_id="line_plot", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_graph1(col_chosen):
    d = {"col1": np.arange(4), "col2": np.arange(4) + 2}
    df = pd.DataFrame(data=d)
    fig = px.line(df, y=["col1", "col2"])
    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
