import cv2
import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html, ctx
from dash.dependencies import Input, Output

VIDEOFILE = '/Users/lc/Movies/CGGbAFH.mp4'

TOTAL_FRAME_COUNT = 1000
READ_START = 100
READ_DUR = 300
HIST_SIZE = 256

def readHist(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    hist = cv2.calcHist([frame], [0], None, [HIST_SIZE], [0.0, 256.0])
    hist = np.power(hist, 0.3)
    return hist

def readVideo(file, start, end):
    global TOTAL_FRAME_COUNT
    video = cv2.VideoCapture(file)
    # TOTAL_FRAME_COUNT = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    array = np.array([])
    for i in range(end+1):
        ret = video.grab()
        if not ret:
            break
        ret, frame = video.retrieve()
    # ret, frame = video.read()
        if frame is None:
            break
        if i == end:
            break
        if ret == True:
            if i < end and i > start:
                resized = cv2.resize(frame, (960, 540))
                hist = readHist(resized)
                array = np.append(array, hist)
            else:
                pass
        if cv2.waitKey(10) & 0xFF == 27:
            break
    video.release()
    cv2.destroyAllWindows()
    return array

def buildDataFrame(readFile, range):
    start = range[0]
    end = range[1]
    duration = end - start
    histArray = readVideo(readFile, start, end)
    x = np.repeat(np.arange(start, end+1, 1), HIST_SIZE)
    y = np.tile(np.arange(1, HIST_SIZE+1, 1), duration)
    z = histArray
    return (x,y,z)

def showHistogram(file):
    df = buildDataFrame(file, (READ_START, READ_START+READ_DUR))
    fig = go.Figure(go.Histogram2d(
            x=df[0],
            y=df[1],
            z=df[2],
            histfunc='sum',
            nbinsx=READ_DUR,
            nbinsy=HIST_SIZE,
            colorscale='Inferno',
        ))
    fig.update_layout(
        xaxis = dict(
            rangeslider=dict(visible=True),
        )
    )
    fig.show()

HEAD = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <style type="text/css">
            html,
            body {
                height: 100%;
                margin: 0;
                padding: 0;
            }
            #hat {
                background: #000000;
                height: 20%;
            }
            #graph {
                background: #000000;
                height: 100%;
            }
            #foot {
                background: #000000;
                height: 100%;
            }
        </style>
    </head>
    <body>
        <div id="hat"> </div>
        {%app_entry%}
        <div id="foot"> </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


def dash_main():
    app = dash.Dash(__name__)  # remove "Updating..." from title
    app.index_string = HEAD
    app.layout = html.Div([
        html.Button('Prev', id='prev-range', n_clicks=0),
        html.Button('Main', id='main-range', n_clicks=0),
        html.Button('Next', id='next-range', n_clicks=0),
        html.Div([dcc.Graph(id='histo')])
                  ])


    @app.callback(
            Output('histo', 'figure'), 
            Input('prev-range', 'n_clicks'),
            Input('main-range', 'n_clicks'),
            Input('next-range', 'n_clicks'),
            )
            
    def update_pgdata(bt1, bt2, bt3):
        button = ctx.triggered_id
        range = (READ_START, READ_START+READ_DUR)
        if button == 'prev-range':
            start = 0 if READ_START-READ_DUR < 0 else READ_START-READ_DUR
            range = (start, READ_START)
        if button == 'next-range':
            range = (READ_START+READ_DUR, READ_START+READ_DUR+READ_DUR)
        if button == 'main-range':
            pass
        df = buildDataFrame(VIDEOFILE, range)
        fig = go.Figure(go.Histogram2d  (
                x=df[0],
                y=df[1],
                z=df[2],
                histfunc='sum',
                nbinsx=READ_DUR,
                nbinsy=HIST_SIZE,
                colorscale='Inferno',
            ))
        fig.update_layout(
            xaxis = dict(
                rangeslider=dict(visible=True),
            )
        )
        return fig

    app.run_server(debug=True)

if __name__ == '__main__':
    # config(title='End Credit ToolBox', theme='dark')
    # start_server(main, port=8888)
    dash_main()