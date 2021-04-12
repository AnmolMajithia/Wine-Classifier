import os
import joblib
import nltk
import re
from nltk.corpus import stopwords


class PredHelper:
    def __init__(self, models_dir="./models", model_name="logistic_regression_88.77.joblib"):
        self.model = joblib.load(os.path.join(models_dir, model_name))
        self.vectorizer = joblib.load(os.path.join(models_dir, "count_vectorizer.joblib"))
        self.encoder = joblib.load(os.path.join(models_dir, "label_encoder.joblib"))
        self._initialize_nlp()
    
    def _initialize_nlp(self):
        self.stopwords = set(stopwords.words("english"))
        self.lemmatizer = nltk.WordNetLemmatizer()

    def _preprocess_text(self, input_text):
        input_text = re.sub("[^a-zA-Z]"," ",input_text)
        input_text = input_text.lower()
        input_text = nltk.word_tokenize(input_text)
        input_text = [i for i in input_text if not i in self.stopwords]
        input_text = [self.lemmatizer.lemmatize(i)for i in input_text]

        return " ".join(input_text) 

    def get_variety(self, input_text):
        input_text = self._preprocess_text(input_text)
        input_X = self.vectorizer.transform([input_text]).toarray()
        output_variety = self.model.predict(input_X)
        output_variety = self.encoder.inverse_transform(output_variety)
        return output_variety

if __name__=="__main__":
    pred_helper = PredHelper()
    output = pred_helper.get_variety(
        "Blackberry and raspberry aromas show a typical Navarran whiff of green herbs and, in this case, horseradish. In the mouth, this is fairly full bodied, with tomatoey acidity. Spicy, herbal flavors complement dark plum fruit, while the finish is fresh but grabby."
        )
    print(output)