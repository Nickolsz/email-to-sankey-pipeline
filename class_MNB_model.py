import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

def predict_category1(message):
    pipeMNB = joblib.load('pipeMNB_model.joblib')
    pred_probs = pipeMNB.predict_proba([message])[0]
    max_prob = max(pred_probs)
    if max_prob < .3:  # You can adjust this threshold as needed
        return 'other'
    predMNB = pipeMNB.predict([message])[0]
    return predMNB

if __name__ == '__main__':
    data = pd.read_excel('C:\\Users\\Nick Olsz\\Desktop\\Email_Data.xlsx')
    X = data['Message']
    y = data['Category']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=23)

    pipeMNB = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', MultinomialNB())
    ])

    pipeMNB.fit(X_train, y_train)

    joblib.dump(pipeMNB, 'pipeMNB_model.joblib')

    predictMNB = pipeMNB.predict(X_test)
    print(f'Accuracy: {accuracy_score(y_test, predictMNB)}')
    print(f'Classification Report: \n{classification_report(y_test, predictMNB)}')

    message = "Thank you for your application for Data Management - SQL Developer , job number R1427404 . We look forward to reviewing your qualifications. If you are selected to move forward in the process, a member of our team will contact you. In addition, we invite you to regularly search and apply for additional opportunities. You may also set up a job notification to receive automated updates meeting your specified criteria. Thank you for your interest in the IQVIA family of companies, including Q2 Solutions & Clintec. Sincerely, IQVIA Talent Acquisition Team"
    predicted_category = predict_category1(message)
    
    print(f'The predicted category is: {predicted_category}')
