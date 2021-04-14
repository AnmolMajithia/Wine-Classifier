import os
import joblib
import nltk
import re
from nltk.corpus import stopwords
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

        # Assuming single input
        return output_variety[0]
    
class PlotHelper:
    def __init__(self, data_dir="./data/"):
        req_cols = ['country', 'designation', 'points', 'price', 'province', 'region_1', 'region_2', 'title','variety', 'winery']
        self.df = pd.read_csv(os.path.join(data_dir, "winemag-data-130k-v2.csv"), index_col=[0], usecols=req_cols)
        self.template = 'plotly_dark'

    def _transparent_fig(self, fig):
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                            plot_bgcolor="rgba(0, 0, 0, 0)",
                            paper_bgcolor="rgba(0, 0, 0, 0)",
                            geo_bgcolor="rgba(0, 0, 0, 0)")
        return fig
    
    def get_map(self, variety):
        df_filtered = self.df[self.df['variety']==variety]
        df_countries = df_filtered.groupby('country')['points'].mean().to_frame().reset_index()

        fig = px.choropleth(data_frame=df_countries,
                        locations='country',
                        locationmode='country names',
                        color='points',
                        color_continuous_scale='ice',
                        template=self.template)

        fig.update_geos(projection_type="natural earth")
        

        return self._transparent_fig(fig)
    
    def get_price_point_distribution(self, variety):
        df_filtered = self.df[self.df['variety']==variety]
        df_plot = df_filtered.reset_index()[['country', 'price', 'points', 'winery']].dropna()
        fig = px.scatter(data_frame=df_plot, 
                    x='price', 
                    y='points', 
                    color='country', 
                    hover_data=['winery'], 
                    template=self.template)
        fig.update_xaxes(side="top")
        return self._transparent_fig(fig)
    
    def get_price_point_bar(self, variety):
        df_filtered = self.df[self.df['variety']==variety]
        df_wineries = df_filtered.groupby('winery').mean().sort_values("points", ascending=False).dropna()[:10].reset_index()
        fig = px.bar(data_frame=df_wineries, 
                orientation='h',
                y='winery', 
                x='price', 
                hover_data=['points'], 
                color='points', 
                color_continuous_scale='ice', 
                template='plotly_dark')
        fig.update_xaxes(side="top")
                
        return self._transparent_fig(fig)

if __name__=="__main__":
    pred_helper = PredHelper()
    output = pred_helper.get_variety(
        "Blackberry and raspberry aromas show a typical Navarran whiff of green herbs and, in this case, horseradish. In the mouth, this is fairly full bodied, with tomatoey acidity. Spicy, herbal flavors complement dark plum fruit, while the finish is fresh but grabby."
        )
    print(output)