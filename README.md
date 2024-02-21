# NFL Big Data Bowl 2024 Repository

Welcome to the repository for the NFL Big Data Bowl 2024, where we delve into the intricacies of tackling performance, particularly focusing on yards after contact in pass plays. This project is part of the Kaggle competition, aiming to extract valuable insights from the extensive NFL tracking data.

## Overview

The primary objective of this project is to analyze and model the factors influencing yards gained after contact during pass plays. Leveraging the rich dataset provided by the NFL, we explore various features such as player speeds, distances, and physical attributes to gain a comprehensive understanding of tackling dynamics.

## Key Features

- **Data Exploration:** I embarked on my journey by delving into the wealth of NFL dataframes at our disposal, meticulously dissecting their diverse structures to unearth crucial variables and discern patterns that might exert influence on yards after contact. While each dataframe offered its unique insights, it was our tracking dataframe that emerged as the treasure trove of invaluable information. Visit the [YAC EDA.ipynb](https://github.com/quincy928/BDB-2024/blob/main/YAC%20EDA.ipynb) to better understand the dataframes. This dynamic resource furnished us with real-time player positions, angles, and velocities on the field, providing a comprehensive snapshot of gameplay. However, to paint a complete picture, we needed to supplement this with pertinent attributes sourced from our supporting dataframes. Extracting details such as ballcarrier identification, yards to first down, and player biometrics including heights and weights from these auxiliary sources, we ensured a comprehensive understanding to fuel our analysis.

- **Data Preprocessing:** Considerable resources were allocated to meticulously clean and refine the dataset. Our efforts encompassed a range of tasks, including play categorization, key player identification, and the creation of pertinent features. These features, which included metrics such as average speed before contact, the distance between the ballcarrier and the defender at the moment of ball reception, and the angle disparities between players at initial contact, were pivotal in our analysis. Notably, I also engineered the dependent variable, yards after contact, in hopes to predict broken tackles. Check out the following play in which Derrick Henry gains 5.31 yards after initial contact. For further exploration of this play, check out the file in the [html folder](https://github.com/quincy928/BDB-2024/tree/main/html), or play around with the `plot_football_play` function in the [Modeling.ipynb file](https://github.com/quincy928/BDB-2024/blob/main/Modeling.ipynb).
![Alt Text](images/Henry0.png)
<img src="images/Henry1.png" alt="Alt Text" width="300" height="200">                                              <img src="images/Henry2.png" alt="Alt Text" width="300" height="200">



  To streamline this process, I developed custom functions housed within the [FeatureEngineering.py](https://github.com/quincy928/BDB-2024/blob/main/YAC%20EDA.ipynb) file. These functions were designed to compute these features for each play from our tracking dataframe. Subsequently, the calculated features were integrated into our newly formed `yac_df` dataframe, which served as the foundation for our modeling endeavors.

- **Modeling:** I experimented with a number of models, both for regression and classification. In the majority of plays, yards after contact was fewer than 3 yards, making it very difficult for a regression model to accurately predict the number of yards gained on a broken tackle. Additionally, the goal here was to identify the first broken tackle, and not subsequent ones. I found it more useful to reframe the problem into a classification setting: did the ballcarrier gain 3 or more yards after initial contact.

  I employed random forest, xgboost, adaboost, and even experimented with a rudimentary feedforward neural network. I found the xgboost model to have slightly better performance than the other models, though they were all only around 70% accurate with an AUC score of 0.60-0.65.
  
<img src="images/rf_roc.png" alt="Alt Text" width="250" height="200"> <img src="images/xg_roc.png" alt="Alt Text" width="250" height="200"> <img src="images/ada_roc.png" alt="Alt Text" width="250" height="200">

## Potential Sources of Error

1. **Undersampling of Minority Class:**
   Plays in which we determined a tackle was broken make up only around 27% of our data, making it more difficult for our model to identify cases where `broken_tackle` is True. SMOTE corrected for this, improving our F1 score for the True label from 0.15 to 0.3, though this really does not come anywhere close to predicting broken tackles the majority of the time. Obviously, the more lenient I was with the cutoff amount of yards (3) qualifying a player as having broken a tackle, the more plays we would have labeled as "True" class. There is a tradeoff here, and what one considers a 'broken tackle' depends on more factors than simply yards gained after contact. 

2. **Variation Between Football Plays:**
   Football plays vary greatly, and more complicated features than the ones engineered for this project probably also play a role in predicting a successful tackle. Understanding the nuances and intricacies of each play, such as player positioning, defensive strategies, and offensive tactics, could provide valuable insights into improving tackle success prediction. Further exploration and incorporation of these factors into the modeling process may enhance the accuracy and robustness of the predictive model.

