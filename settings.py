TRACK_TERMS = ['Ronaldo', 'CR7', 'Halamadrid', 'Real Madrid', 'RealMadrid', 'Cristiano']
CONNECTION_STRING = 'sqlite:///CR7tweets.db'
CSV_NAME = "tweets.csv"
TABLE_NAME = "CR7tweet"

try:
    from private import *
except Exception:
    pass