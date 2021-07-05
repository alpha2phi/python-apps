import json
import requests
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

API_URL = "https://aeab47j4z7.execute-api.ap-southeast-1.amazonaws.com/prod/inference"

app = dash.Dash()

app.layout = html.Div([
    html.Div(id='waitfor'),
    dcc.Upload(id='upload',
               children=html.Div(
                   ['Drag and Drop or ',
                    html.A('Select a File')]),
               style={
                   'width': '100%',
                   'height': '60px',
                   'lineHeight': '60px',
                   'borderWidth': '1px',
                   'borderStyle': 'dashed',
                   'borderRadius': '5px',
                   'textAlign': 'center',
                   'margin': '10px'
               }),
    html.Div(id='output'),
    html.Div(dt.DataTable(data=[{}]), style={'display': 'none'})
])

pre_style = {
    'whiteSpace': 'pre-wrap',
    'wordBreak': 'break-all',
    'whiteSpace': 'normal'
}


def predict(contents):
    payload = contents[contents.find(",") + 1:]
    data = {"data": payload}
    response = requests.post(API_URL, data=json.dumps(data))
    return response.text


@app.callback(Output('output', 'children'), [Input('upload', 'contents')])
def update_output(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        if 'image' in content_type:
            predictions = predict(contents)
            return html.Div([
                html.Div('Predictions'),
                html.Pre(predictions, style=pre_style),
                html.Hr(),
                html.Img(src=contents)
            ])


if __name__ == '__main__':
    app.run_server(debug=True)
