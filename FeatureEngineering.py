import numpy as np
import pandas as pd


def yards_after_contact(row, tracking):
    gameId = row['gameId']
    playId = row['playId']
    ballCarrierId = row['ballCarrierId']
    
    selected_tracking = tracking[(tracking.gameId == gameId) & (tracking.playId == playId) & (tracking.nflId == ballCarrierId)]

    # Check if there are matching rows
    if not selected_tracking.empty:
        first_contact_row = selected_tracking.loc[selected_tracking.event == 'first_contact', 'x']
        tackle_row = selected_tracking.loc[selected_tracking.event == 'tackle', 'x']

        # Check if rows with 'first_contact' and 'tackle' events exist
        if not first_contact_row.empty and not tackle_row.empty:
            x_first_contact = first_contact_row.values[0]
            x_tackle = tackle_row.values[0]

            play_direction = selected_tracking['playDirection'].values[0]

            if play_direction == 'right':
                yards_gained = x_tackle - x_first_contact
            else:
                yards_gained = x_first_contact - x_tackle

            # Forward progress rule
            yards_gained = max(0, yards_gained)
        else:
            # If events are not found, set yards_gained to 0
            yards_gained = 0
    else:
        # If no matching rows are found, set yards_gained to 0
        yards_gained = 0

    return yards_gained

def get_avg_speed(row, tracking_df, defender):
    gameId = row['gameId']
    playId = row['playId']
    defenderId = row['defender_first_contact']
    
    selected_tracking = tracking_df[(tracking_df.gameId == gameId) & (tracking_df.playId == playId)]

    # Filter for the relevant events
    relevant_events = ['handoff', 'run', 'pass_outcome_caught']
    event_frame = selected_tracking[selected_tracking['event'].isin(relevant_events)]['frameId'].values[0]
    last_frame = selected_tracking[selected_tracking.event == 'first_contact']['frameId'].values[0]
    numframes = last_frame - event_frame + 1

    speed_defender = 0
    speed_ballcarrier = 0
    
    for frame in range(event_frame, last_frame + 1):  # Use range to iterate over frames
        speed_defender += selected_tracking[(selected_tracking.frameId == frame) & (selected_tracking.nflId == defenderId)]['s'].values[0] / numframes
        speed_ballcarrier += selected_tracking[(selected_tracking.frameId == frame) & (selected_tracking.nflId == selected_tracking.ballCarrierId)]['s'].values[0] / numframes


    if defender:
        return speed_defender
    else:
        return speed_ballcarrier

def get_distance(row, tracking_df):
    gameId = row['gameId']
    playId = row['playId']
    defenderId = row['defender_first_contact']
    selected_tracking = tracking_df[(tracking_df.gameId == gameId) & (tracking_df.playId == playId)]

    # Filter for the relevant events
    relevant_events = ['handoff', 'run', 'pass_outcome_caught']
    event_frame = selected_tracking[selected_tracking['event'].isin(relevant_events)]['frameId'].values[0]
    
    x_ballcarrier = selected_tracking[(selected_tracking.frameId == event_frame) & (selected_tracking.nflId == selected_tracking.ballCarrierId)]['x'].values[0]
    y_ballcarrier = selected_tracking[(selected_tracking.frameId == event_frame) & (selected_tracking.nflId == selected_tracking.ballCarrierId)]['y'].values[0]
    x_defender = selected_tracking[(selected_tracking.frameId == event_frame) & (selected_tracking.nflId == defenderId)]['x'].values[0]
    y_defender = selected_tracking[(selected_tracking.frameId == event_frame) & (selected_tracking.nflId == defenderId)]['y'].values[0]
    
    return np.sqrt((x_defender - x_ballcarrier)**2 + (y_defender - y_ballcarrier)**2)


def get_num_defenders_near_ball(row, tracking_df):
    gameId = row['gameId']
    playId = row['playId']
    ballCarrierId = row['ballCarrierId']

    selected_play = tracking_df[(tracking_df['gameId'] == gameId) & (tracking_df['playId']==playId)]
    
    # Get the coordinates of the ball carrier
    ball_carrier_row = selected_play[(selected_play['event'] == 'first_contact') & (selected_play['nflId'] == ballCarrierId)]
    x_ballcarrier = ball_carrier_row['x'].values[0]
    y_ballcarrier = ball_carrier_row['y'].values[0]

    # Calculate distances for all defenders
    selected_play['distance_to_ballcarrier'] = np.sqrt((selected_play['x'] - x_ballcarrier)**2 + (selected_play['y'] - y_ballcarrier)**2)

    # Count the number of defenders within 3 yards
    num_defenders_near_ball = len(selected_play[(selected_play['event'] == 'first_contact') & (selected_play['nflId'] != ballCarrierId) & (selected_play['distance_to_ballcarrier'] <= 3)])

    return num_defenders_near_ball


def get_angles(row, tracking_df, event):
    gameId = row['gameId']
    playId = row['playId']
    defenderId = row['defender_first_contact']
    ballCarrierId = row['ballCarrierId']
    
    selected_tracking = tracking_df[(tracking_df.gameId == gameId) & (tracking_df.playId == playId)]
    angle_ballcarrier = selected_tracking[(selected_tracking.nflId == ballCarrierId) & (selected_tracking.event == event)]['o'].values[0]
    angle_defender = selected_tracking[(selected_tracking.nflId == defenderId) & (selected_tracking.event == event)]['o'].values[0]
    
    offense_angle = 0
    if selected_tracking['playDirection'].values[0] == 'left':
        offense_angle = 270
    else:
        offense_angle = 90
    
    raw_angle_difference = angle_defender - angle_ballcarrier
    standardized_angle_difference = (raw_angle_difference - offense_angle) % 360
    
    return standardized_angle_difference