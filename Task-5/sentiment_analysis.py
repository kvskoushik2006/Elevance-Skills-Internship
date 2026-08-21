from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Create the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """
    Detect whether the user's message is
    Positive, Negative, or Neutral.
    """

    scores = analyzer.polarity_scores(text)

    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"

    elif compound <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, scores


# Test the sentiment analysis
if __name__ == "__main__":

    messages = [
        "I am very happy today!",
        "I am really angry and frustrated.",
        "What is artificial intelligence?"
    ]

    for message in messages:

        sentiment, scores = analyze_sentiment(message)

        print("--------------------------------")
        print("Message:", message)
        print("Sentiment:", sentiment)
        print("Scores:", scores)