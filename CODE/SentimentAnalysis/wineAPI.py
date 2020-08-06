
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from SentimentAnalysis import SentimentAnalysis
from WineRecommend import WineRecommender
import json
import pandas as pd

app = Flask(__name__)
api = Api(app)


class WineApi(Resource):
    def get(self):
        args = request.args
        inputtext = args.get('inputtext')
        print("prediction for",inputtext)
        # recommendation=['a','b']

        sa = SentimentAnalysis( 'sa.mdl' )
        prediction = sa.performsentimentAnlysis( [inputtext] )
        # dic = {'prediction': prediction[0]}

        wr = WineRecommender('./input/winemag-data-130k-v2.csv')
        recommendation = wr.make_recommendation(prediction[0],10)
        # winedic = {}
        # winedic = {'wines': [i for i in recommendation]}

        # for i in range(len(recommendation)):
        #   winedic.update({i:recommendation[i]})

        # for index, row in df.iterrows():

        # df = pd.DataFrame.from_dict( winedic,orient='index' )
        # df.columns = [ 'Recommendation']
        # for index, row in recommendation.iterrows():
        #  winedic.update( {index: row[i]} )
        # data = {"payload":recommendation.to_json(orient="index")}

        #data = pd.DataFrame(list(recommendation.items()), columns=['Wine', 'Avg Price','Points'])
        data = pd.DataFrame( recommendation, columns=['Wine', 'Avg Price', 'Points'] )
        # data.sort_values( by=['Avg Price'] )
        data = data.to_json(orient="records")

        # print(data)
        return data

#class


api.add_resource( WineApi, '/wine/' )

if __name__ == '__main__':
    app.run(port='5002')

    # w = WineApi()
    # d = w.get()

