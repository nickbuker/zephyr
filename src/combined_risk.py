import numpy as np


def combined_risk(weather_risk, tweet_risk):
    combined = np.mean([weather_risk, tweet_risk])
    combined_score = int(round(combined * 5))
    if combined_score == 0:
        combined_score += 1
    return combined_score
