import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import collections
from sklearn import (feature_extraction,linear_model,model_selection,datasets,pipeline)
from sklearn import metrics
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics.pairwise import linear_kernel
from sklearn.model_selection import cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
from sklearn.ensemble import RandomForestClassifier

class SentimentAnalysis:
    def __init__(self,filepath):
        self.filepath=filepath
        self.jobfile= 'sa.mdl'
        self.nltk_stop_words = nltk.corpus.stopwords.words( "english" )
        self.white_list = ['Aromas','includes','overly','medium','soft','freshness'
            'what', 'but', 'if', 'because', 'as', 'until', 'against',
            'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'why', 'how', 'all', 'any',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'can', 'will', 'just', 'don', 'should']


    def datapreparation(self,forvarity,forregion=False):
        data = pd.read_csv(self.filepath )

        data.drop_duplicates()
        data[data.variety.notnull()]
        data.dropna()

        #data = data.iloc[0:10000, ]
        datashape = data.shape
        print( 'shape of wine data set', datashape )
        # print('pre processing head',data.head())

        dup_description = sum( data.duplicated( 'description' ) )
        dup_title = sum( data.duplicated( 'title' ) )
        print( 'duplicate description in data',dup_description )
        print( 'duplicate title in data',dup_title )

        if forvarity :
            data = data.drop_duplicates(['description','variety'])

            print( 'shape of wine data set', data.shape )

            print('each variety of wine',data['variety'].value_counts())

            data = data.groupby( 'variety' ).filter( lambda x: len( x ) > 100 )
            data['variety'] = data['variety'].astype( 'category' )
            print('uniqe wine class**', len( data['variety'] ) )
        if forregion :
            data = data.drop_duplicates( ['description', 'region_1'] )
            data['region_1'] = data['region_1'].astype( 'category' )

        return data

    def createmodel(self,X,Y):

        #self.createword_cloud( data )
        X_test, X_train, gsmodel, y_test, y_train = self.createpipleine( X, Y)

        gsmodel.fit( X_train, y_train )
        print( 'Model performance: {}'.format( gsmodel.score( X_test, y_test ) ) )

        y_pred = gsmodel.predict( X_test )

        print( 'best param', gsmodel.best_params_ )
        print( 'best score', gsmodel.best_score_ )

        print( 'cv_results', (pd.DataFrame( gsmodel.cv_results_ )) )

        print( "Accuracy:", metrics.accuracy_score( y_test, y_pred ) )

        joblib.dump( gsmodel, self.jobfile )

    def createpipleine(self, X,Y ):
        stop_words = [sw for sw in self.nltk_stop_words if sw not in self.white_list]
        X_train, X_test, y_train, y_test = model_selection.train_test_split(
            X, Y, test_size=0.20, random_state=42 )
        model = pipeline.Pipeline( [
            ('counts', feature_extraction.text.CountVectorizer(
                lowercase=True,
                tokenizer=nltk.word_tokenize,
                min_df=100,
                ngram_range=(1, 2),
                stop_words=stop_words
            )),
            ('tfidf', feature_extraction.text.TfidfTransformer()),
            ('svm', svm.SVC()),
        ] )
        kernels = ['linear', 'rbf']
        c = [0.1, 1, 100]
        #param_grid = {'n_estimators': [100, 200, 300, 1000], 'max_depth': [80, 90, 100, 110]}
        gsmodel = GridSearchCV(
            model,
            {
                'counts__ngram_range': [(1, 2)],
                'svm__kernel': kernels,
                'svm__C': c
            },
            n_jobs=-1,
            cv=5
        )
        return X_test, X_train, gsmodel, y_test, y_train

    def createword_cloud(self, data):
        plt.figure( figsize=(16, 8) )
        plt.title( 'Cloud of Review text' )
        wc = WordCloud( max_words=1000, max_font_size=40, background_color='black', stopwords=STOPWORDS,
                        colormap='Set1' )
        wc.generate( ' '.join( data['description'] ) )
        plt.imshow( wc, interpolation="bilinear" )
        plt.axis( 'off' )
        plt.show()
        plt.savefig( 'wclould.png' )




    def performsentimentAnlysis(self,inputtextArr):
        jobl_model = joblib.load( self.jobfile )
        ypredict = jobl_model.predict( inputtextArr )

        print( "predicted", ypredict )
        return ypredict


if __name__ == '__main__':
    filename = './input/winemag-data-130k-v2.csv'
    sa = SentimentAnalysis(filename)
    data = sa.datapreparation(True)
    sa.createmodel(data['description'],data['variety'])
    inputtext = ["Aromas include tropical fruit, broom, brimstone and dried herb. The palate isn\'t overly expressive, offering unripened apple, citrus and dried sage alongside brisk acidity."]
    prediction = sa.performsentimentAnlysis(inputtext)
    print("predicted variety of wi.ne is" ,prediction)