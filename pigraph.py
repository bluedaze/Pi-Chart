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
	dash_app = dash.Dash(routes_pathname_prefix='/', external_stylesheets=[dbc.themes.SLATE], server=server)
	dash_app.index_string = '''
	<!DOCTYPE html>
	<html>
	    <head>
	        {%metas%}
	        <title>{%title%}</title>
	        {%favicon%}
	        {%css%}
		<!-- Global site tag (gtag.js) - Google Analytics -->
		<script async src="https://www.googletagmanager.com/gtag/js?id=UA-11302591-2"></script>
		<script>
		  window.dataLayer = window.dataLayer || [];
		  function gtag(){dataLayer.push(arguments);}
		  gtag('js', new Date());

		  gtag('config', 'UA-11302591-2');
		</script>

	    </head>
	    <body>
	        {%app_entry%}
	        <footer>
	            {%config%}
	            {%scripts%}
	            {%renderer%}
	        </footer>
	    </body>
	</html>
	'''
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
	    ], fluid=True)


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
			fig = go.Figure()
			data = ps.query_bracket(market)
			graphs[market] = data

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
				figure = fig.add_trace(go.Scattergl(x=timeStamp, y=prices,
				name=bracket,
				hovertemplate='<b>Bracket: ' + bracket
				+ '</b>.<br>Price: %{y:$.2f}<extra></extra><br>'
				+ '%{x}<br>'))

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
			#height=768,
			#width=1070,
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
			tabscontent.append(dbc.Col(dcc.Graph(figure=figures[key])))
		notice = "We may have to move on, but we don't have to give up." 
		return html.Div([dbc.Row(dbc.Col(


			[dbc.NavbarSimple([dbc.NavItem(dbc.NavLink("Tweet Markets", href="https://www.predictit.org/markets/search?query=tweet", target="_blank"))],
				brand="Pi-Chart", color="primary", dark=True, fluid=True)])), 
			

			dbc.Row(tabscontent, no_gutters=True),

			html.Div([html.P(notice), html.P([dcc.Link("Don't let this be the end. Join us on discord.", 
				href='https://discord.gg/V7wmfd', target="_blank")])])


			])



	return dash_app.server


with app.app_context():
	app = create_dashboard(app)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)