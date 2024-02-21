# NFL Big Data Bowl 2024 Repository

Welcome to the repository for the NFL Big Data Bowl 2024, where we delve into the intricacies of tackling performance, particularly focusing on yards after contact in pass plays. This project is part of the Kaggle competition, aiming to extract valuable insights from the extensive NFL tracking data.

## Overview

The primary objective of this project is to analyze and model the factors influencing yards gained after contact during pass plays. Leveraging the rich dataset provided by the NFL, we explore various features such as player speeds, distances, and physical attributes to gain a comprehensive understanding of tackling dynamics.

## Key Features

- **Data Exploration:** We embarked on our journey by delving into the wealth of NFL dataframes at our disposal, meticulously dissecting their diverse structures to unearth crucial variables and discern patterns that might exert influence on yards after contact. While each dataframe offered its unique insights, it was our tracking dataframe that emerged as the treasure trove of invaluable information. This dynamic resource furnished us with real-time player positions, angles, and velocities on the field, providing a comprehensive snapshot of gameplay. However, to paint a complete picture, we needed to supplement this with pertinent attributes sourced from our supporting dataframes. Extracting details such as ballcarrier identification, yards to first down, and player biometrics including heights and weights from these auxiliary sources, we ensured a comprehensive understanding to fuel our analysis.
  
- **Data Preprocessing:** Significant efforts were dedicated to cleaning and preparing the dataset. We categorized plays, identified key players, and engineered relevant features to facilitate meaningful analysis. 

- **Modeling:** We experimented with various regression models, including linear regression, Lasso regression, and Random Forest regression, to predict yards after contact. These models were assessed based on metrics like mean squared error and R-squared.
- **Feature Importance:** Utilizing a number of classification models, we attempted to predict wether or not a tackle would be broken on a given play

## Project Structure

- **Notebooks:** The repository includes Jupyter notebooks detailing the step-by-step process of data exploration, preprocessing, modeling, and feature analysis.

- **Data:** The 'data' directory contains the raw and processed datasets used throughout the project. Note that the tracking data files were too large and can instead be found [here](https://www.kaggle.com/competitions/nfl-big-data-bowl-2024/data)

- **Animation:** This section houses the function for animating plays from the tracking data
