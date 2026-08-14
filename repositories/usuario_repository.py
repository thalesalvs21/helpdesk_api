from models.usuario import Usuario
from database import db

class UsuarioRepository():
    @staticmethod
    def consulta_tudo():
        return Usuario.query.order_by(Usuario.nome).all()

    @staticmethod
    def consulta_um(id):
        return Usuario.query.filter_by(id=id).first()

    @staticmethod
    def pesquisa_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def cadastrar_usuario(dados):
        usuario = Usuario(
            nome=dados['nome'],
            email=dados['email'],
            setor=dados.get('setor')
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def atualizar_usuario(id, dados):
        usuario = Usuario.query.filter_by(id=id).first()
        if not usuario:
            return None
        usuario.nome = dados['nome']
        usuario.email = dados['email']
        usuario.setor = dados.get('setor')
        db.session.commit()
        return usuario

    @staticmethod
    def excluir_usuario(usuario):
        db.session.delete(usuario)
        db.session.commit()

    @staticmethod
    def conta_total_usuarios():
        return Usuario.query.count()
