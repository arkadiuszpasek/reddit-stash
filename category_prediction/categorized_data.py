import praw
import pickle
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from prawcore import Forbidden

list_of_categories = ["sports", "health", "religion", "politics", "technology", "science", "culture", "travel"]

def get_reddit(secret_file="./static/secret.txt"):
    result = {}
    with open(secret_file, "r") as secret:
        for line in secret:
            line = line.strip()
            key, value = line.split("=")
            result[key] = value

    return praw.Reddit(user_agent=result["user_agent"],
                       client_id=result["client_id"],
                       client_secret=result["client_secret"])


def fetch_categorized_posts():
    reddit = get_reddit()
    subreddits = ["sports", "health", "politics", "technology", "science", "culture", "travel"]

    posts = []
    for subreddit_name in subreddits:
        print(subreddit_name)
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for post in subreddit.top(limit=3000):
                body = post.selftext
                if not body:
                    body = "none"
                posts.append(
                    [post.title, body, subreddit_name])
        except Forbidden:
            print(f"Exception for subreddit {subreddit_name}")
            continue
    print(len(posts))
    return posts

def category_to_number(category):
    return list_of_categories.index(category) + 1

def process_post(post):
    title, body, category = post
    if body != 'none':
        title += body
    tokens = word_tokenize(title)
    filtered = [lemmatizer.lemmatize(token.lower()) for token in tokens if
                token not in stopwords.words("english")]
    words = dict()
    for word in filtered:
        words[word] = True
    if category in list_of_categories:
        num = category_to_number(category)
    else:
        num = 0

    return (words, num)

if __name__ == "__main__":
    posts = fetch_categorized_posts()
    lemmatizer = WordNetLemmatizer()
    processed = []
    for post in posts:
        processed.append(process_post(post))
    clf = nltk.NaiveBayesClassifier.train(processed)
    file = open("classifier", "wb")
    pickle.dump(clf, file)
