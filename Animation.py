import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from IPython.display import HTML

def plot_football_play(playId, gameId, week, plays, games, colors):
    # Filter the DataFrame for the specified playId and gameId
    selected_tracking = week[(week['playId'] == playId) & (week['gameId'] == gameId)]
    selected_play = plays[(plays['playId'] == playId) & (plays['gameId'] == gameId)]
    
    down = selected_play['down'].values[0]
    down_mapping = {
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th"
    }
    down_text = down_mapping.get(down, "Unknown")

    quarter = selected_play['quarter'].values[0]
    quarter_text = down_mapping.get(quarter, "Unknown")
    game_clock = selected_play['gameClock'].values[0]
    playDescription = selected_play['playDescription'].values[0]
    playDirection = selected_tracking['playDirection'].values[0]
    homeTeam = games.homeTeamAbbr.values[0]
    visitorTeam = games.visitorTeamAbbr.values[0]
    ballCarrierId = plays.ballCarrierId.values[0]

    #make the away team white
    modified_colors = colors.copy()
    modified_colors[visitorTeam] = "#FFFFFF"
    
    #Set line of scrimmage and first down
    #Offense on own half and going right
    if (selected_play['possessionTeam'].values[0] == selected_play['yardlineSide'].values[0] and playDirection == 'right'):
        line_of_scrimmage = selected_play['yardlineNumber'].values[0] + 10
        first_down_line = line_of_scrimmage + selected_play['yardsToGo'].values[0]
    #Offense on opponents half and going right
    elif (selected_play['possessionTeam'].values[0] != selected_play['yardlineSide'].values[0] and playDirection == 'right'):
        line_of_scrimmage = 110 - selected_play['yardlineNumber'].values[0]
        first_down_line = line_of_scrimmage + selected_play['yardsToGo'].values[0]
    #Offense on own half and going left
    elif (selected_play['possessionTeam'].values[0] == selected_play['yardlineSide'].values[0] and playDirection == 'left'):
        line_of_scrimmage = 110 - selected_play['yardlineNumber'].values[0]
        first_down_line = line_of_scrimmage - selected_play['yardsToGo'].values[0]
    #Offense on opponents half and going left
    elif (selected_play['possessionTeam'].values[0] != selected_play['yardlineSide'].values[0] and playDirection == 'left'):
        line_of_scrimmage = selected_play['yardlineNumber'].values[0] + 10
        first_down_line = line_of_scrimmage - selected_play['yardsToGo'].values[0]

    scorebug = f'{homeTeam} : {selected_play.preSnapHomeScore.values[0]} {visitorTeam} : {selected_play.preSnapVisitorScore.values[0]} || {quarter_text} {game_clock} || {down_text} and {selected_play.yardsToGo.values[0]}'

    # Create an animated scatter plot with Plotly Express
    scatter_fig = px.scatter(selected_tracking, x='x', y='y', animation_frame='frameId', color='club', color_discrete_map = modified_colors,
                     hover_data=['jerseyNumber', 'displayName', 's', 'event'],
                     title=playDescription)


    # Add football field shapes and annotations
    field_shapes = [
        dict(type='rect', x0=0, x1=10,y0=0,y1=53.3, fillcolor='blue', opacity=0.5),
        dict(type='rect', x0=110, x1=120,y0=0,y1=53.3, fillcolor='blue', opacity=0.5),
        dict(type='line', x0=line_of_scrimmage, x1=line_of_scrimmage,y0=0,y1=53.3, line=dict(color='blue')),
        dict(type='line', x0=first_down_line, x1=first_down_line,y0=0,y1=53.3, line=dict(color='yellow'))
    ]
    for x in range(10, 115, 5):
        field_shapes.append(dict(type='line', x0=x, x1=x, y0=0, y1=53.3, line=dict(color='white', width=1)))


    field_annotations = [
        dict(x=5, y=26.65,textangle=270, text=homeTeam, showarrow=False, font=dict(color='white', size=12)),
        dict(x=115, y=26.65,textangle=90, text=homeTeam, showarrow=False, font=dict(color='white', size=12)),
    ]

    for x in range(20, 70, 10):
        field_annotations.append(dict(x=x, y=8, text=(x-10), showarrow=False, font=dict(color='white', size=12)))
        field_annotations.append(dict(x=x, y=45.3, text=(x-10), showarrow=False, font=dict(color='white', size=12)))
    for x in range(70, 110, 10):
        field_annotations.append(dict(x=x, y=8, text=(110-x), showarrow=False, font=dict(color='white', size=12)))
        field_annotations.append(dict(x=x, y=45.3, text=(110-x), showarrow=False, font=dict(color='white', size=12)))

    title_annotation = dict(
    x=0.5,  # X-coordinate (0.5 is the center of the plot)
    y=-0.2,  # Y-coordinate (negative to position under the plot)
    xref='paper',
    yref='paper',
    text=scorebug,
    showarrow=False,
    font=dict(size=14, color='black')  # Customize the font size and color
    )
    
    # Create football field layout
    field_layout = go.Layout(
        shapes=field_shapes,
        annotations=field_annotations + [title_annotation],
        xaxis=dict(range=[0, 120], title =''),
        yaxis=dict(range=[0, 53.3], title=''),
        showlegend=True,
        height = 533,
        width = 1200
    )
    field_layout['xaxis'].update(showgrid=False)
    field_layout['yaxis'].update(showgrid=False)

    scatter_fig.update_layout(field_layout, plot_bgcolor='green')

    # Show the combined plot
    scatter_fig.show()
    # Generate a custom filename if not provided
    filename = f"play_{playId}_game_{gameId}.html"
    
    # Ensure the "gifs" folder exists
    os.makedirs("html", exist_ok=True)
    
    # Save the animation as a GIF
    pio.write_html(scatter_fig, f'html/{filename}', include_plotlyjs='cdn')