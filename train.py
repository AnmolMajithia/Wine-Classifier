import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv('data/winemag-data-130k-v2.csv', index_col = 0)
data = data[['variety', 'description', 'title']]
data = data.dropna()
data = data.reset_index()

descriptionList = pd.read_csv('data/description_list_title_desc_NA_dropped.csv', index_col=[0])["0"].tolist()

max_features = 1500
count_vectorizer = CountVectorizer(max_features=max_features)

x = count_vectorizer.fit_transform(descriptionList).toarray()

le = LabelEncoder()
y = le.fit_transform(data['variety'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 42)

regressor = LogisticRegression(verbose=1, n_jobs=16)
regressor.fit(x_train, y_train)

y_pred = regressor.predict(x_test)
#print(classification_report(y_test, y_pred))
accuracy = accuracy_score(y_test, y_pred)*100
print("Accuracy: {:.2f}%".format(accuracy))

joblib.dump(count_vectorizer, "count_vectorizer.joblib")
joblib.dump(le, "label_encoder.joblib")
joblib.dump(regressor, "logistic_regression_%.2f.joblib"%(accuracy))
