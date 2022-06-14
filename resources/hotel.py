from flask_restful import Resource, reqparse
from models.hotel_model import HotelModel
from resources.filtros import normalizar_path_parametros,consulta_sem_cidade,consulta_com_cidade
from flask_jwt_extended import jwt_required
from models.site_model import SiteModel
import sqlite3

#path /hoteis?cidade=Rio de janeiro&estrelas_min=4&diaria_max=400 é o caminho passado com 
#parametro de filtragem




path_parametros = reqparse.RequestParser()
path_parametros.add_argument('cidade', type=str)
path_parametros.add_argument('estrelas_min', type=float)
path_parametros.add_argument('estrelas_max', type=float)
path_parametros.add_argument('diaria_min', type=float)
path_parametros.add_argument('diaria_max', type=float)
path_parametros.add_argument('limit', type=float)
path_parametros.add_argument('offset', type=float)

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_parametros.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalizar_path_parametros(**dados_validos)

        if not parametros.get('cidade'):     
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:  
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'cidade': linha[2],
            'estrelas': linha[3],
            'diaria': linha[4],
            'site_id': linha[5] 

            })

        return{'Listagem de Hoteis': hoteis}
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help='O campo não pode ficar vazio')
    argumentos.add_argument('cidade', type=str)
    argumentos.add_argument('estrelas', type=float,required=True, help='O campo não pode ficar vazio')
    argumentos.add_argument('diaria', type=float)
    argumentos.add_argument('site_id', type=int, required=True, help='Necessita de um link do site')

    def get(self,hotel_id):
        resultado = HotelModel.procurar_hotel(hotel_id)
        if resultado:
            return resultado.json()
        return {'message':'Hotel não encontrado'},404

    @jwt_required()
    def post(self,hotel_id):

        if HotelModel.procurar_hotel(hotel_id):
            return {"message":"Hotel id '{}' already exist.".format(hotel_id)},400

        dados  = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados['site_id']):
            return {"message":"O hotel precisa estar associado a um site valido"}, 400
        try:
            hotel_objeto.save_hotel()
        except:
            return{'message':'Error saving'},500
        return hotel_objeto.json()
       
    @jwt_required() 
    def put(self,hotel_id):

        dados = Hotel.argumentos.parse_args()
        resultado = HotelModel.procurar_hotel(hotel_id)
        if resultado:
            resultado.update_hotel(**dados)
            resultado.save_hotel()
            return resultado.json(),200 #CODIGO DE SUCESSO
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201 #CODIGO DE CRIADO

    @jwt_required()
    def delete(self,hotel_id):
        hotel = HotelModel.procurar_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return{'message':'Error ocurred trying to delete hotel'}
            return {'message':'Hotel deleted'}
        return{'message':'Hotel not found'},404