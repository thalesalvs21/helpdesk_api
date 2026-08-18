from flask import Flask
from database import db
from controllers.usuario_controller import UsuarioController
from controllers.chamado_controller import ChamadoController

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdesk.db"
app.config["SECRET_KEY"] = 'minhachavesupersecretaqueninguemvaidescobrir'

db.init_app(app)



app.add_url_rule('/usuarios', endpoint='usuario_listar', view_func=UsuarioController.listar, methods=['GET'])
app.add_url_rule('/usuarios', endpoint='usuario_cadastrar', view_func=UsuarioController.cadastrar, methods=['POST'])
app.add_url_rule('/usuarios/<int:id>', endpoint='usuario_atualizar', view_func=UsuarioController.atualizar, methods=['PUT'])
app.add_url_rule('/usuarios/<int:id>', endpoint='usuario_excluir', view_func=UsuarioController.excluir, methods=['DELETE'])
app.add_url_rule('/usuarios/<int:id>/chamados', endpoint='usuario_listar_chamados', view_func=UsuarioController.listar_chamados, methods=['GET'])


app.add_url_rule('/chamados', endpoint='chamado_listar', view_func=ChamadoController.listar, methods=['GET'])
app.add_url_rule('/chamados', endpoint='chamado_cadastrar', view_func=ChamadoController.cadastrar, methods=['POST'])
app.add_url_rule('/chamados/<int:id>', endpoint='chamado_atualizar', view_func=ChamadoController.atualizar, methods=['PUT'])
app.add_url_rule('/chamados/<int:id>', endpoint='chamado_excluir', view_func=ChamadoController.excluir, methods=['DELETE'])
app.add_url_rule('/chamados/<int:id>/iniciar', endpoint='chamado_iniciar', view_func=ChamadoController.iniciar, methods=['PATCH'])
app.add_url_rule('/chamados/<int:id>/encerrar', endpoint='chamado_encerrar', view_func=ChamadoController.encerrar, methods=['PATCH'])
app.add_url_rule('/chamados/abertos', endpoint='chamado_listar_abertos', view_func=ChamadoController.listar_abertos, methods=['GET'])
app.add_url_rule('/chamados/prioridade/alta', endpoint='chamado_listar_prioridade_alta', view_func=ChamadoController.listar_prioridade_alta, methods=['GET'])
app.add_url_rule('/estatisticas', endpoint='chamado_estatisticas', view_func=ChamadoController.estatisticas, methods=['GET'])


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)