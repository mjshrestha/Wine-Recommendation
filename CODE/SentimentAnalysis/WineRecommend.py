import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import NearestNeighbors
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.externals import joblib



class WineRecommender:

    def __init__(self,datafile):
        self.datafile = datafile #
        self.jobfile = 'WineRecommender.mdl'
        self.recommendation_model = NearestNeighbors()

    def set_model_prama(self,n_neighbors,algorithm,metric):
        self.recommendation_model.set_params( **{
            'n_neighbors': n_neighbors,
            'algorithm': algorithm,
            'metric': metric} )

    def datapreparation(self):
        data = pd.read_csv(self.datafile)
        #data=data.iloc[0:1000,]
        #drop duplicates
        data.drop_duplicates()
        #select noy null wine variety
        data[data.variety.notnull()]
        data.dropna(subset=['taster_name'], how='all', inplace = True)

        print( 'Number of varity of wines', data['variety'].nunique() )


        col = ['province','variety','points','designation','taster_name','price']
        datafornn = data[col]
        datafornn = datafornn.drop_duplicates(['province','variety','designation','taster_name','price'])
        datafornn=datafornn[datafornn['points'] >80]
        X= datafornn[['province','variety','designation','taster_name','price']]
        y=datafornn.points;

        datafornn_pivot=pd.pivot_table(datafornn, index= ['variety'],columns=['taster_name'],values='points').fillna(0)
        pivotmatrix = csr_matrix(datafornn_pivot)
        return pivotmatrix,datafornn_pivot,datafornn

    def executemodel(self,numberofrecommend):
        self.set_model_prama( numberofrecommend, 'brute', 'cosine' )
        pivotmatrix, datafornn_pivot, more_data = self.datapreparation()
        fitted_model = self.recommendation_model.fit( pivotmatrix )
        joblib.dump( fitted_model, self.jobfile )

    def make_recommendation(self,winevariety,numberofrecommend):
        fitted_model = joblib.load( self.jobfile )
        _, datafornn_pivot,datafornn = self.datapreparation()
        #result = datafornn.loc[datafornn.variety==str(winevariety)]

        datainpivot = datafornn_pivot.loc[(winevariety)].values.reshape(1,-1)
        fitted_model.n_jobs = 1
        vectordistance, indx = fitted_model.kneighbors(datainpivot,numberofrecommend+1)
        recommendedWine = []
        winedic = {}
        for i in range( 1, len( indx.flatten() ) ):

            #result = datafornn.loc[datafornn.variety == str( winevariety )]
            wine = datafornn_pivot.index[indx.flatten()[i]]
            result = datafornn.loc[datafornn.variety == str(wine)] #result.groupby( ['variety', ] ).mean()['price'].sort_values( ascending=False ).to_frame()
            resultprc = result.groupby( ['variety', ] ).mean()['price'].to_frame()
            resultpoint = result.groupby( ['variety', ] ).mean()['points'].to_frame()

            avgprice = None
            avgpoint = None;
            #recommendedWine.append(round(resultprc['price'],2))
            #recommendedWine.append( resultpoint['points'] )
            for index, row in resultprc.iterrows():
                #winedic.update({wine:recommendedWine})
                #recommendedWine.append(row['price'])
                avgprice = round(row['price'],2)
            for index, row in resultpoint.iterrows():
                #winedic.update({wine:recommendedWine})
                #recommendedWine.append(row['points'])
                avgpoint = round(row['points'],2)
            recommendedWine.append([wine,avgprice,avgpoint]  )
            #recommendedWine.append(result)
        #df = pd.DataFrame.from_dict( winedic, orient='index' )
        #df.columns = ['Avg Price']

        return recommendedWine

    def getDetailsofWine(self,winevariety):
        _, datafornn_pivot, datafornn = self.datapreparation()
        result = datafornn.loc[datafornn.variety == str( winevariety )]
        result = result['winery','prices']
        result = result.groupby('winery')


if __name__ == '__main__':
        filename = './input/winemag-data-130k-v2.csv'
        # filename = './input/winemag-lngs-lats-precip-temp.csv'
        winevariety ='Cabernet Sauvignon'


        recommender = WineRecommender(filename)
        recommender.executemodel(10)

        recommender.make_recommendation(winevariety,10)

 # ref:  https://machinelearningmastery.com/sparse-matrices-for-machine-learning/
        #https: // towardsdatascience.com / collaborative - filtering - and -embeddings - part - 1 - 63b00b9739ce
        #https://pbpython.com/pandas-pivot-table-explained.html
