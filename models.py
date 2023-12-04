import numpy as np
import pandas as pd


class Movie():

    def __init__(self) -> None:
        self.movies = pd.read_csv('ml-latest-small/movies.csv')
        self.matrix = pd.read_csv('ml-latest-small/matrix_by_id.csv')
        self.films = np.array(self.movies)

    @property
    def film_data(self):
        data = []
        for film in self.films:
            data.append({'movie_id': film[0],'movie_title': film[1]})
        return data

    @property
    def film_data_dict(self):
        data = {}
        for film in self.films:
            data[film[0]] = film[1] 
        return data
    
    def pearson(self, s1, s2):
        s1_c = s1-s1.mean()
        s2_c = s2-s2.mean()
        return np.sum(s1_c*s2_c)/np.sqrt(np.sum(s1_c**2)*np.sum(s2_c**2))
    
    def get_recs(self, movie_id, num):
        reviews = []
        movie_id = str(movie_id)
        for id in self.matrix.columns:
            if id == movie_id:
                continue
            cor = self.pearson(self.matrix[movie_id], self.matrix[id])
            if np.isnan(cor):
                continue
            else:
                reviews.append((id, cor))
            reviews.sort(key=lambda tup: tup[1], reverse=True)
        return reviews[:num]