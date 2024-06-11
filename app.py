import pandas as pd

import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import dash_cytoscape as cyto

import dash_bootstrap_components as dbc

import plotly.express as px
from neo4j import GraphDatabase

from mysql_utils import get_university,  \
     get_keyword_by_year, get_keyword_trend, get_AI_faculty, \
     insert_professor, delete_professor_by_email

from mongodb_utils import pub_keyword
from neo4j_utils import faculty_keyword

#publications = pub_cnt()
#publications = pd.DataFrame(publications).to_dict('records')
neo_db = db = GraphDatabase.driver('bolt://127.0.0.1:7687')
AI_faculty = get_AI_faculty()

#app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(

    style={
        'backgroundColor': '#F5F5F5',
        'marginRight': '80px',
        'marginLeft': '80px',
        'marginTop': '50px',
        'marginBottom': '50px'
    },

    children=[
    html.H1(children='Academic Keyword Explorer',
            style={
                'textAlign': 'center',
                'color': 'WhiteSmoke',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '30px',
                'fontWeight': 'bold',
                'marginTop': '50px',
                'marginBottom': '30px',
                'background-color': '#003366',  # Set the background color##003366 #
                'padding': '20px' # Add some padding to the header
            },

            ),

html.Br(),
html.Br(),
html.Br(),
dbc.Row([
    dbc.Col([
#sql : R3, R6, R8, 
    html.H2("Top Keywords by Year", style={'textAlign':'center','backgroundColor': 'Silver','fontSize': '30px'}),
        dcc.Input(id='input4'),
    html.Button('Search year', id='search_button4'),
    html.Plaintext('e.g. 2015', style={'fontSize': '12px'}),

        dcc.Graph(id="keywords_by_year"),
], width=6),
    dbc.Col([
#sql : R3, R6, R8, 
    html.H2("Keyword Trend by Year",style={'textAlign':'center','backgroundColor': 'Silver','fontSize': '30px'}),
#    html.Plaintext('e.g. "deep learning"'),
    dcc.Input(id='input5'),
    html.Button('Search Keyword', id='search_button5'),
    html.Plaintext('e.g. deep learning', style={'fontSize': '12px'}),

        dcc.Graph(id="keyword_trend"),
], width=6),
]),

html.Br(),
html.Br(),
html.Br(),
dbc.Row([

    dbc.Col([
#mongo :R4, R6, R8,
    html.H1(children='Top Publications by Keyword', style={'textAlign':'center','backgroundColor': 'Silver','fontSize': '30px'}),
    dcc.Input(id='input9'),
    html.Plaintext('e.g. deep learning',style={'fontSize': '12px'}),
    html.Button('Search Keyword', id='search_button9'),
    dash_table.DataTable(
        columns = [{'name': 'title', 'id': 'title'},
                   {'name': 'year', 'id': 'year'},
                   {'name': 'citations', 'id': 'numCitations'},
                   {'name': 'score', 'id': 'score'}
                   ],
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': 'SteelBlue',  # Set the background color of the header
            'color': 'white',
            'textAlign': 'left'# Set the text color of the header
        },
        style_cell={
            'backgroundColor': 'LightSilver',
            'whiteSpace': 'normal',# Set the background color of the cells
            'textAlign': 'left'
        },
        page_size=10,
        id='Pub_by_Keywords_table'),
], width=6),
    dbc.Col([
#neo4j : R5, R6, R8
    html.H1(children='Top Faculties by Keyword', style={'textAlign':'center','backgroundColor': 'Silver','fontSize': '30px'}),
    dcc.Input(id='input7'),
    html.Plaintext('e.g. deep learning',style={'fontSize': '12px'}),
    html.Button('Search Keyword', id='search_button7'),
    dash_table.DataTable(
        columns=[{'name': 'name', 'id': 'name'},
                 {'name': 'position', 'id': 'position'},
                 {'name': 'university', 'id': 'university'},
                 {'name': 'score', 'id': 'score'}
                 ],
        style_table={'overflowX': 'auto'},

        style_header={
            'backgroundColor': 'SteelBlue',  # Set the background color of the header
            'color': 'white',  # Set the text color of the header
            'textAlign': 'left'
        },
        style_cell={
            'backgroundColor': 'LightSilver',
            'whiteSpace': 'normal',# Set the background color of the cells
            'textAlign': 'left'
        },

        page_size=10,
        id='fal_by_Keywords_table'),
], width=6)
]),

html.Br(),
html.Br(),
html.Br(),
#sql: R3, R6,
    html.H1("Top Deep Learning Faculty by Citation Count",style={'textAlign':'center','backgroundColor': 'Silver','fontSize': '30px'}),
    dash_table.DataTable(
        data = AI_faculty,
        style_header = {
    'backgroundColor': 'SteelBlue',  # Set the background color of the header
    'color': 'white',
    'textAlign': 'left'  # Set the text color of the header
},
        style_cell={
            'backgroundColor': 'PowderBlue',
            'whiteSpace': 'normal',  # Set the background color of the cells
            'textAlign': 'left'
        }
    ),

html.Br(),
html.Br(),
html.Br(),
html.H1("Faculty Record Management", style={'textAlign':'center','backgroundColor': 'Silver'}),
dbc.Row([
    dbc.Col([
#sql: R3,R6,R7,
    html.H4('Insert Faculty', style={'textAlign':'center','backgroundColor': 'Silver'}),
    dbc.Row([
        html.Plaintext('faculty name, e.g. "John Doe"'),
        dcc.Input(id='infname', style={'width': '50%'}),
        html.Plaintext('faculty school, e.g. "University of Illinois Urbana-Champaign"'),
        dcc.Input(id='infschool', style={'width': '50%'}),
        html.Plaintext('faculty title, e.g."associate professor"'),
        dcc.Input(id='inftitle', style={'width': '50%'}),
        html.Plaintext('faculty email, e.g. "jd@illinois.edu"'),
        dcc.Input(id='infemail', style={'width': '50%'})
    ]),
    html.Button('Add Faculty', id='add_button'),
    html.Br(),
    dcc.Textarea(id='outfInfo',style={'width': '50%', 'height': 100}),
        ], width=6),

    dbc.Col([
#sql: R3, R6,R7, 
    html.H4('Delete Faculty using email',style={'textAlign':'center','backgroundColor': 'Silver'}),
    dcc.Input(id='infemail_delete', style={'width': '50%'}),
    html.Plaintext('faculty email, e.g. "jd@illinois.edu"'),
    html.Button('Delete Faculty', id='delete_button'),
    html.Br(),
    dcc.Textarea(id='outfInfo_delete',style={'width': '50%', 'height': 100}),
    ], width=6),
])


])

#Good_Mongo
@callback(
    Output('Pub_by_Keywords_table', 'data'),
    State('input9', 'value'),
    Input('search_button9', 'n_clicks')
)
def update_table3(input_value, n_clicks):
    if not input_value:
        return dash.no_update
    result = pub_keyword(input_value)
    print(result)
    return result

#good neo4j

@callback(
    Output('fal_by_Keywords_table', 'data'),
    State('input7', 'value'),
    Input('search_button7', 'n_clicks')
)
def update_table7(input_value, n_clicks):
    if not input_value:
        return dash.no_update
    result = faculty_keyword(input_value)
    print(result)
    return result


#Good sql
@callback(
    Output("keywords_by_year", "figure"),
    State('input4', 'value'),
    Input("search_button4", "n_clicks"))
def keyword_byYear(input_value, n_clicks):
    Sql_result = get_keyword_by_year(input_value)
    df = pd.DataFrame(Sql_result)
    fig = px.histogram(df, x='name',y='count', labels={'name': 'Keywords', 'count':'count'},color_discrete_sequence=['purple'])
    return fig

#Good sql
@callback(
    Output("keyword_trend", "figure"),
    State('input5', 'value'),
    Input("search_button5", "n_clicks"))
def keyword_by_trend(input_value, n_clicks):
    Sql_result = get_keyword_trend(input_value)
    df = pd.DataFrame(Sql_result)
    fig = px.line(df, x='year',y='count')
    return fig

#Good sql
@callback(
    Output("outfInfo", "value"),
    State('infname', 'value'),
    State('infschool', 'value'),
    State('inftitle', 'value'),
    State('infemail', 'value'),
    Input("add_button", "n_clicks"))
def insert_faculty(infname, infschool, inftitle, infemail, n_clicks):
    print(infname, infschool, inftitle, infemail)
    response = insert_professor(','.join([infname, infschool, inftitle, infemail]))
    return response

# sql
@callback(
    Output('outfInfo_delete', 'value'),
    State('infemail_delete', 'value'),
    Input('delete_button', 'n_clicks')
)
def delete_faculty(input_value, n_clicks):
   response = delete_professor_by_email(input_value)
   return response

if __name__ == '__main__':
    app.run_server()
