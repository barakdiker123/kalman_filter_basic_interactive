# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import numpy as np
from linear_kalman_filter import *
import plotly.graph_objects as go

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
        html.Div(
            [
                "time_jumps",
                dcc.Input(id="time_jumps", value="3", type="number"),
            ]
        ),
        html.Div(["time_dur", dcc.Input(
            id="time_dur", value="400", type="number")]),
        html.Div(["Q_0_0", dcc.Input(id="Q_0_0", value="0.05", type="number")]),
        html.Div(["Q_1_1", dcc.Input(id="Q_1_1", value="0.05", type="number")]),
        html.Div(["R_0_0", dcc.Input(id="R_0_0", value="16", type="number")]),
        html.Div(["R_1_1", dcc.Input(id="R_1_1", value="16", type="number")]),
        dcc.Graph(figure={}, id="x_location_estimate"),
        dcc.Graph(figure={}, id="y_location_estimate"),
        dcc.Graph(figure={}, id="z_location_estimate"),
    ]
)

# Add controls to build the interaction


@callback(
    Output(component_id="x_location_estimate", component_property="figure"),
    Output(component_id="y_location_estimate", component_property="figure"),
    Output(component_id="z_location_estimate", component_property="figure"),
    Input(component_id="time_jumps", component_property="value"),
    Input(component_id="time_dur", component_property="value"),
    Input(component_id="Q_0_0", component_property="value"),
    Input(component_id="Q_1_1", component_property="value"),
    Input(component_id="R_0_0", component_property="value"),
    Input(component_id="R_1_1", component_property="value"),
)
def update_graph_x_location(time_jumps, time_dur, Q_0_0, Q_1_1, R_0_0, R_1_1):
    (
        time,
        error_x,
        location_x_variance,
        error_y,
        location_y_variance,
        leng_pos_x_in,
        leng_pos_x_total,
        leng_pos_y_in,
        leng_pos_y_total,
    ) = main_run(
        time_jumps=int(time_jumps),
        time_dur=int(time_dur),
        Q_0_0=float(Q_0_0),
        Q_1_1=float(Q_1_1),
        R_0_0=float(R_0_0),
        R_1_1=float(R_1_1),
    )
    location_x_uncertainty = np.sqrt(location_x_variance)
    location_y_uncertainty = np.sqrt(location_y_variance)
    d = {
        "error_x": error_x.ravel(),
        "location_x_uncertainty1": location_x_uncertainty,
        "location_x_uncertainty2": -location_x_uncertainty,
        "error_y": error_y.ravel(),
        "location_y_uncertainty1": location_y_uncertainty,
        "location_y_uncertainty2": -location_y_uncertainty,
    }
    df = pd.DataFrame(data=d)
    percent_x = 100 * int(leng_pos_x_in) / int(leng_pos_x_total)
    fig_x = px.line(
        df,
        y=["location_x_uncertainty1", "location_x_uncertainty2", "error_x"],
        title="Estimate X "
        + str(leng_pos_x_in)
        + "/"
        + str(leng_pos_x_total)
        + " Percent:"
        + str(percent_x),
    )
    # fig_x.add_scatter(
    #    x=df.index, y=df["error_x"], mode="markers", marker={"size": 7})
    fig_x.update_layout(
        xaxis_title="time [time_dur*s]", yaxis_title="error_x[m]")
    percent_y = 100 * int(leng_pos_y_in) / int(leng_pos_y_total)
    fig_y = px.line(
        df,
        y=["location_y_uncertainty1", "location_y_uncertainty2", "error_y"],
        title="Estimate Y "
        + str(leng_pos_y_in)
        + "/"
        + str(leng_pos_y_total)
        + " Percent:"
        + str(percent_y),
    )
    # fig_y.add_scatter(
    #    x=df.index, y=df["error_y"], mode="markers", marker={"size": 7})

    fig_y.update_layout(
        xaxis_title="time [time_dur*s]", yaxis_title="error_y[m]")
    fig3 = go.Figure(data=fig_x.data + fig_y.data)  # Cool Fusion !!
    return fig_x, fig_y, fig3

    # Run the app


if __name__ == "__main__":
    # app.run(debug=True)
    app.run_server(host="0.0.0.0", port="8050")
