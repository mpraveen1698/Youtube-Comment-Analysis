import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
import joblib
import os
import warnings

def load_model_safely(model_path, model_name):
    """
    Safely load a model with version compatibility handling.
    """
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            model = joblib.load(model_path)
        print(f"Successfully loaded {model_name}")
        return model
    except Exception as e:
        print(f"Error loading {model_name}: {str(e)}")
        raise Exception(f"Failed to load {model_name}. Please retrain the models using retrain_models.py")

def analyze_comments(df):
    l_com = list(df['comments'])
    comments_df = pd.DataFrame()
    comments_df['comments'] = l_com

    stops = set(stopwords.words('english'))
    stops.add("'")
    stops.add("<br>")
    stops.add("<br />")

    comments_without_sw = []
   
    for i in l_com:
        val=""
        for v in i.split():
            v=v.lower()
            if v not in stops:
                val=val+" "+v
        comments_without_sw.append(val)

    cleaned_comments=[]
    for w in comments_without_sw:
        w=re.sub('[^a-zA-Z ]',' ',w)
        cleaned_comments.append(w)

    comments_df['originalComments'] = comments_df.comments
    comments_df.comments = cleaned_comments
    comments_df['like_count'] = list(df.like_count)

    try:
        vectorizer = load_model_safely('vectorized.pkl', 'TF-IDF Vectorizer')
        X = vectorizer.transform(cleaned_comments).toarray()
        print(X)
        
        model = load_model_safely("random_forest.pkl", 'Random Forest Model')
        y_predict = model.predict(X)
    except Exception as e:
        print(f"Model loading error: {str(e)}")
        print("Please run 'python retrain_models.py' to retrain the models with the current scikit-learn version.")
        raise

    comments_df['sentiment'] = y_predict
    
    pos_most_liked = comments_df[comments_df.sentiment == 1.0].sort_values('like_count', ascending=False).head(5)[['originalComments', 'like_count']]
    neu_most_liked = comments_df[comments_df.sentiment == 0.0].sort_values('like_count', ascending=False).head(5)[['originalComments', 'like_count']]
    neg_most_liked = comments_df[comments_df.sentiment == -1.0].sort_values('like_count', ascending=False).head(5)[['originalComments', 'like_count']]

    return comments_df, pos_most_liked, neu_most_liked, neg_most_liked
    

if __name__ == "__main__":
    analyze_comments()