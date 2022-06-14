from flask_restful import Resource
from models.site_model import SiteModel

class Sites(Resource):
    def get(self):
        return{'sites':[site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self,url):
        site = SiteModel.procurar_site(url)
        if site:
            return site.json()
        return {'message':'Site não existe'},404
    def post(self,url):
        if SiteModel.procurar_site(url):
            return{"message":"O Site '{}' ja existe".format(url)},400
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {"message":"Um erro interno ocorreu na criação"}
        return site.json()    

    def delete(self,url):
        site = SiteModel.procurar_site(url)
        if site:
            site.delete_site()
            return {'message':'Site deletado'}
        return {'message':'ERRO'}