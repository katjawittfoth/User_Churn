# Predicting mobile app purchases
Team Memebers:<br>
Hongdou Li<br>
Jacques Sham<br>
Katja Wittfoth<br>

# Project
As a final project for Advanced Machine Learning class at USF, an industry partner provided us with a real world 40 GB dataset of anonymized user app activity.
The goal was to predict whether or not those users would make a purchase within the next 7 or 14 days. 
### Why predicting purchases if we want to know user's risk for churn?
A user is said to have churned if they uninstalled or stopped using. Usually, it’s too late if the user has already churned. It’s easier and cheaper to retain existing users than acquire new ones. Therefore, we were asked to identify those at-risk users.

## Dataset
The data was distributed across four varioys datasets: messages, events, sessions, and attributes.

## Model
Our team achieved 0.98256 AUC using XGBoost.

* [Modeling](https://github.com/katjawittfoth/user-churn/blob/master/Model_with_Hyperparameter_Tunning.ipynb)
* [Script to extract labels](https://github.com/katjawittfoth/user-churn/blob/master/label_extract.py)
