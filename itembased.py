import pandas as pd
import warnings
warnings.filterwarnings('ignore')
ratingPD = pd.read_csv('ratings.dat',sep='::',names = ['User_ID','Movie_ID','Rating','Timestamp'])
movieNames = pd.read_csv('movies.dat',sep = '::' , names = ['Movie_ID','Title','Genre'])
Dataset = ratingPD.merge(movieNames ,on ='Movie_ID')
Dataset = Dataset.drop(columns = ['Timestamp'])
mean_r = Dataset.groupby('Title').mean()
mean_r['count'] = Dataset.groupby('Title').count()['Rating']
table = pd.pivot_table(Dataset ,values = 'Rating',index=['User_ID'],columns =['Title'] )
def recommend(movie,n):
    movie_name = table[movie]
    corr_movie = table.corrwith(movie_name)
    corr_movie = corr_movie.dropna()
    corr_movie = pd.DataFrame(corr_movie,columns = ['Corr'])
    corr_movie = pd.merge(corr_movie,mean_r, on='Title')
    corr_movie = corr_movie[corr_movie['count']>200].sort_values('Corr',ascending = False)
    movies = corr_movie.drop(columns = ['User_ID','Movie_ID','count','Corr'])
    movies = movies.head(n)
    movies = movies.to_dict()
    return movies

movie = input()
n =int(input())
prediction = recommend(movie,n)
print('Title             Rating')
for p in prediction['Rating']:
    print(p ,end ='  ')
    print('%.02f'%prediction['Rating'][p])
