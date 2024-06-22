import pandas as pd
from sklearn import metrics
import nltk
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

lr = joblib.load('logistic_regression_model.pkl')
cv = joblib.load('count_vectorizer.pkl')
lemmatizer = WordNetLemmatizer()

def predict_category(text, threshold=0.5):
    r = re.sub('[^a-zA-Z]', ' ', text)
    r = r.lower()
    r = r.split()
    r = [word for word in r if word not in stopwords.words('english')]
    r = [lemmatizer.lemmatize(word) for word in r]
    r = ' '.join(r)
    text_cv = cv.transform([r])
    probabilities = lr.predict_proba(text_cv)[0]
    max_prob = max(probabilities)
    if max_prob < threshold:
        return "Other"
    else:
        prediction = lr.predict(text_cv)
        return prediction[0]

if __name__ == '__main__':
    data = pd.read_excel('C:\\Users\\Nick Olsz\\Desktop\\Email_Data.xlsx')
    # nltk.download('all')
    text = list(data['Message'])
    lemmatizer = WordNetLemmatizer()
    corpus = []
    for i in range(len(text)):
        r = re.sub('[^a-zA-Z]', ' ', text[i])
        r = r.lower()
        r = r.split()
        r = [word for word in r if word not in stopwords.words('english')]
        r = [lemmatizer.lemmatize(word) for word in r]
        r = ' '.join(r)
        corpus.append(r)

    data['Message'] = corpus
    data.head()
    X = data['Message']
    y = data['Category']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123)
    cv = CountVectorizer()
    X_train_cv = cv.fit_transform(X_train)
    lr = LogisticRegression()
    lr.fit(X_train_cv, y_train)

    # Save the model and vectorizer
    joblib.dump(lr, 'logistic_regression_model.pkl')
    joblib.dump(cv, 'count_vectorizer.pkl')

    X_test_cv = cv.transform(X_test)
    




