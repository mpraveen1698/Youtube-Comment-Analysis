from flask import Flask
from flask import render_template, request, jsonify
from urllib.parse import unquote
import pandas as pd
import youtube_scrapper
import comment_analysis

app = Flask(__name__)

@app.route('/')
def get_comments():
    data = {"ytURL":"",
        "views": "",
        "likes": "",
        "dislikes": ""}

    return render_template("index.html", data=data)

@app.route('/results', methods=['GET', 'POST'])
def get_comments_again():
    ytURL = request.form.get('youtubeURL', "")
    print(ytURL)   
    ytURL = unquote(ytURL)
    print(ytURL)
    data = dict()
    if ytURL!="":
        try:
            video_id = ytURL.split("=")[1]
            ytURL = "https://www.youtube.com/embed/"+video_id
            views, likes, dislikes, comments_df  = youtube_scrapper.main(video_id)
        except Exception as e:
            print(f"Error fetching YouTube data: {str(e)}")
            # Return error page with meaningful message
            data = {"ytURL":"",
                "views": "",
                "likes": "",
                "dislikes": "",
                "error": f"Failed to fetch YouTube data: {str(e)}"}
            return render_template("error.html", data=data)
        data = {"ytURL":ytURL,
            "views": views,
            "likes": likes,
            "dislikes": dislikes}
        
        classified_comments, pos_most_liked, neu_most_liked, neg_most_liked = comment_analysis.analyze_comments(comments_df)
        
        positive_comments = " ".join(" ".join(x.split()) for x in classified_comments[classified_comments.sentiment == 1.0]['comments'])    
        neutral_comments = " ".join(" ".join(x.split()) for x in classified_comments[classified_comments.sentiment == 0.0]['comments'])
        negative_comments = " ".join(" ".join(x.split()) for x in classified_comments[classified_comments.sentiment == -1.0]['comments'])

        classification_counts = classified_comments['sentiment'].value_counts().sort_index().tolist()
        print(classification_counts)
        data['Positive'] = classification_counts[2]
        data['Neutral'] = classification_counts[1]
        data['Negative'] = classification_counts[0]
        data['PosComments'] = positive_comments
        data['NeutComments'] = neutral_comments
        data['NegComments'] = negative_comments
        data['Positive5'] = pos_most_liked
        data['Neutral5'] = neu_most_liked
        data['Negative5'] = neg_most_liked
    
    else:
        data = {"ytURL":"",
            "views": 0,
            "likes": 0,
            "dislikes": 0}
        data['Positive'] = 0
        data['Netural'] = 0
        data['Negative'] = 0
        data['PosComments'] = ""
        data['NeutComments'] = ""
        data['NegComments'] = ""
        data['Positive5'] = pd.DataFrame()
        data['Neutral5'] = pd.DataFrame()
        data['Negative5'] = pd.DataFrame()

    return render_template("results.html", data=data)

@app.errorhandler(500)  
def invalid_youtubeId(e):
    data = {"ytURL":"",
        "views": "",
        "likes": "",
        "dislikes": ""}

    return render_template("error.html", data=data) 

def main():
    app.run( port=3333, debug=True)


if __name__ == '__main__':
    main()
