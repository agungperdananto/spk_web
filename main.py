from http import HTTPStatus

from flask import Flask, request, abort
from flask_restful import Resource, Api 

from models import Movie as MovieModel

app = Flask(__name__)
api = Api(app)        


class Movie(Resource):

    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page<page_count:
            next = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next=None
        if page>1:
            prev = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev = None
        
        if page > page_count or page < 1:
            abort(404, description = f'Halaman {page} tidak ditemukan.') 
        return  {
            'page': page, 
            'page_size': page_size,
            'next': next, 
            'prev': prev,
            'Results': list[start:end]
        }

    def get(self):
        movie = MovieModel()
        return self.get_paginated_result('movies/', movie.film_data, request.args), HTTPStatus.OK.value



class Recommendation(Resource):

    def post(self):
        data = request.get_json()
        movie_id = data.get('movie_id')
        length = data.get('length', 10)
        movie = MovieModel()
        
        if not movie_id:
            return 'movie_id is empty', HTTPStatus.BAD_REQUEST.value
        
        if not movie.film_data_dict.get(movie_id):
            return 'movie_id is not found', HTTPStatus.NOT_FOUND.value

        
        recommendations = movie.get_recs(movie_id, int(length))
        results = [{'movie_id': int(rec[0]),'movie_title': movie.film_data_dict[int(rec[0])], 'score': round(rec[1] * 100, 2)} for rec in recommendations]

        return {
            'movie_id': int(movie_id),
            'movie_title': movie.film_data_dict[movie_id],
            'recommendations': results
        }, HTTPStatus.OK.value

class SAW(Resource):

    def post(self):
        return {4: 0.71, 2: 0.74, 3: 0.76, 1: 0.82, 5: 0.82, 6: 0.84}

api.add_resource(Movie, '/movies')
api.add_resource(Recommendation, '/recommendation')
api.add_resource(SAW, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)