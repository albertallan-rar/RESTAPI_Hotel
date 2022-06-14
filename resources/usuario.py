from flask_restful import Resource, reqparse
from models.usuario_model import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
#from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login_user', type=str, required=True, help='Esse campo não pode ficar vazio')
atributos.add_argument('senha_user', type=str, required=True, help='Esse campo não pode ficar vazio')

class User(Resource):
    
    def get(self,user_id):
        resultado_usuario = UsuarioModel.procurar_usuario(user_id)
        if resultado_usuario:
            return resultado_usuario.json()
        return {'message':'Usuario não encontrado'},404

    @jwt_required()
    def delete(self,user_id):
        user = UsuarioModel.procurar_usuario(user_id)
        if user:
            try:
                user.delete_usuario()
            except:
                return{'message':'Error ocurred trying to delete User'}
            return {'message':'User deleted'}
        return{'message':'User not found'},404

class UserRegister(Resource):
    #Cadastro

    def post(self):
        
        dados = atributos.parse_args()

        if UsuarioModel.procurar_login(dados['login_user']):
            return{"message":"O login '{}'digitado já existe".format(dados['login_user'])}
        try:
            user= UsuarioModel(**dados)
            user.save_usuario()
            return{"message":"Usuario criado com sucesso !!!"},201 #Criado
        except:
            return{'message':'ERRO'}

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UsuarioModel.procurar_login(dados['login_user'])

        if user and safe_str_cmp(user.senha_user, dados['senha_user']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return{'acess_token': token_de_acesso},200
        return{'message':'O username ou a senha esta incorreto'},401

 #class UserLogout(Resource):

    #@jwt_required
    # def post(self):
    #    jwt_id = get_jwt()['jti']
    #    BLACKLIST.add(jwt_id)
    #    return {'message': 'Você foi deslogado com sucesso!'}, 200