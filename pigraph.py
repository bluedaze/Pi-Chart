#!/usr/bin/python
import sqlite3
import plotly.graph_objects as go
import plotly.io as pio
import pisql as ps
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flask import Flask



app = Flask(__name__)
def create_dashboard(server):
	dash_app = dash.Dash(routes_pathname_prefix='/', external_stylesheets=[dbc.themes.CYBORG], server=server)
	dash_app.title = 'Pi-chart.com'
	dash_app.layout = dbc.Container([html.Title("Pi-chart.com"),
	        dcc.Store(id="localstorage", storage_type="local"),
	        html.Div(id='tab-content'),
	        html.Div(id='tabs'),
	        dcc.Interval(
	            id='interval-component',
	            interval=1*60000, # in millisecond
	            n_intervals=0
	        )
	    ])


	@dash_app.callback(Output('localstorage', 'data'),
	              [Input('interval-component', 'n_intervals')])
	def create_figure(n):
		graphs = {}
		brackets = {}
		marketData=[]
		fetch_tables = ps.fetch_tables()
		tables = list(fetch_tables)
		count = 0
		for market in tables:
			bracketData = {}
			fig = go.Figure()
			for i in range(9):
				bracket = 'B' + str(i + 1)
				data = ps.query_bracket(bracket, market)
				prices, timeStamp = map(list, zip(*[[k, v] for k, v in data]))
				bracketData[bracket] = prices, timeStamp
			graphs.update({market: bracketData})

		return graphs

	@dash_app.callback(
	    Output("tab-content", "children"),
	    [Input("localstorage", "data")],
	)
	def create_layout(graphs):
		figures = {}
		markets = graphs.keys()
		for market in markets:
			brackets = graphs[market].keys()
			fig = go.Figure()
			for bracket in brackets:
				prices = graphs[market][bracket][0]
				timeStamp = graphs[market][bracket][1]
				figure = fig.add_trace(go.Scatter(x=timeStamp, y=prices,
				name=bracket,
				hovertemplate='<b>Bracket: ' + bracket
				+ '</b>.<br>Price: %{y:$.2f}<extra></extra><br>'
				+ '%{x}<br>', line_shape="spline"))

			figures.update({market: fig})


			template = 'plotly_dark'
			fig.update_layout(
			template=template,
			xaxis=dict(
			autorange=True,
			showgrid=False,
			mirror=True,
			ticks='outside',
			showline=True,
			linecolor='#FFFFFF',
			rangeslider=dict(visible=True, thickness=0.08),
			),
			yaxis=dict(showgrid=False),
			height=768,
			width=1070,
			title_text=market,
			showlegend=True,
			margin=dict(l=100, t=100, r=20, b=20),
			uirevision="uirevisionstring"
			)

			fig.update_xaxes(tickformatstops=[
			dict(dtickrange=[None, 1000], value='%-I:%M:%S%.%L%p ms'),
			dict(dtickrange=[1000, 60000], value='%-I:%M:%S%p s'),
			dict(dtickrange=[60000, 3600000], value='%-I:%M%p'),
			dict(dtickrange=[3600000, 86400000], value='%-a %-I:%M%p'),
			dict(dtickrange=[86400000, 604800000], value='%e. %b d'),
			dict(dtickrange=[604800000, 'M1'], value='%e. %b w'),
			dict(dtickrange=['M1', 'M12'], value="%b '%y M"),
			dict(dtickrange=['M12', None], value='%Y Y'),
			])
			graphs.update({market: fig})

		tabscontent=[]


		for key in figures:
			tabscontent.append(dbc.Tab(dcc.Graph(figure=figures[key]), label=key))

		return 		dbc.Card(dbc.CardBody([html.H5('Pi-chart presently in beta.', className='card-title'),
	                 html.P('Look forward to more in the future!'),
	                 html.Div(dbc.Tabs(tabscontent))]), color='secondary',
	                 outline=True, inverse=True)



	return dash_app.server


with app.app_context():
	app = create_dashboard(app)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)