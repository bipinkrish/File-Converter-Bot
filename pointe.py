from requests import post
import json
import plotly.io as pio
import plotly.graph_objects as go
# import plotly.offline as pyo

def pointE(prompt):

    reqUrl = "https://openai-point-e.hf.space/run/predict"
    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/json" 
    }
    payload = json.dumps({"data": [prompt]})
    response = post(reqUrl, data=payload,  headers=headersList).json()

    plot_data = json.loads(response["data"][0]["plot"])
    fig = go.Figure(data=plot_data["data"])
    pio.write_image(fig, f'{prompt}.png', format='png')
    pio.write_html(fig, f'{prompt}.html')
    # pyo.plot(fig, filename='figure.html', auto_open=True)
    return f'{prompt}.html', f'{prompt}.png'
