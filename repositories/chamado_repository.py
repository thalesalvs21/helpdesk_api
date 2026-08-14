from models.chamado import Chamado
from database import db

class ChamadoRepository():
    @staticmethod
    def consulta_tudo():
        return Chamado.query.order_by(Chamado.id).all()

    @staticmethod
    def consulta_um(id):
        return Chamado.query.filter_by(id=id).first()

    @staticmethod
    def consulta_por_usuario(usuario_id):
        return Chamado.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def consulta_por_status(status):
        return Chamado.query.filter_by(status=status).all()

    @staticmethod
    def consulta_por_prioridade(prioridade):
        return Chamado.query.filter_by(prioridade=prioridade).all()

    @staticmethod
    def conta_nao_encerrados(usuario_id):
        return Chamado.query.filter(
            Chamado.usuario_id == usuario_id,
            Chamado.status != 'Encerrado'
        ).count()

    @staticmethod
    def cadastrar_chamado(dados):
        chamado = Chamado(
            titulo=dados['titulo'],
            descricao=dados['descricao'],
            prioridade=dados['prioridade'],
            status='Aberto',
            tecnico=dados.get('tecnico'),
            usuario_id=dados['usuario_id']
        )
        db.session.add(chamado)
        db.session.commit()
        return chamado

    @staticmethod
    def atualizar_chamado(id, dados):
        chamado = Chamado.query.filter_by(id=id).first()
        if not chamado:
            return None
        chamado.titulo = dados['titulo']
        chamado.descricao = dados['descricao']
        chamado.prioridade = dados['prioridade']
        chamado.tecnico = dados.get('tecnico')
        db.session.commit()
        return chamado

    @staticmethod
    def excluir_chamado(chamado):
        db.session.delete(chamado)
        db.session.commit()

    @staticmethod
    def atualizar_status(chamado, status):
        chamado.status = status
        db.session.commit()
        return chamado

    @staticmethod
    def conta_total():
        return Chamado.query.count()

    @staticmethod
    def conta_por_status(status):
        return Chamado.query.filter_by(status=status).count()
