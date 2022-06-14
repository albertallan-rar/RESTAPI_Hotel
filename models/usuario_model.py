from sql_alchemy import banco

class UsuarioModel(banco.Model):
    __tablename__ = 'usuario'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login_user = banco.Column(banco.String(40))
    senha_user = banco.Column(banco.String(40))
    

    def __init__(self, login_user, senha_user):
        
        self.login_user = login_user
        self.senha_user = senha_user
        

    def json(self):
        return{
            'user_id': self.user_id,
            'login': self.login_user
            
        }

    @classmethod
    def procurar_usuario(cls, user_id):
        usuario_procurado = cls.query.filter_by(user_id=user_id).first()
        #SELECT * FROM usuario WHERE user_id = $user_id
        if usuario_procurado:
            return usuario_procurado
        return None

    @classmethod
    def procurar_login(cls, login_user):
        login_procurado = cls.query.filter_by(login_user=login_user).first()
        #SELECT * FROM usuario WHERE login = $login
        if login_procurado:
            return login_procurado
        return None

    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()      
    
    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()