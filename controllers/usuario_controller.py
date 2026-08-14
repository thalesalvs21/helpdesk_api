from flask import jsonify, request
from services.usuario_service import UsuarioServices

class UsuarioController():

    @staticmethod
    def valida_dados(dados):
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        if not dados.get("nome"):
            return jsonify({"erro": "Nome é obrigatório"}), 400
        if not dados.get("email"):
            return jsonify({"erro": "Email é obrigatório"}), 400
        return True

    @staticmethod
    def listar():
        resultado = UsuarioServices.consulta_usuarios()
        return jsonify(resultado)

    @staticmethod
    def cadastrar():
        dados = request.json
        valida_dados = UsuarioController.valida_dados(dados)
        if valida_dados is not True:
            return valida_dados

        if UsuarioServices.consultar_email(dados["email"]):
            return jsonify({"erro": "Já existe um usuário com esse email"}), 409

        usuario = UsuarioServices.cadastra_usuario(
            nome=dados["nome"],
            email=dados["email"],
            setor=dados.get("setor")
        )

        return jsonify({
            "mensagem": "Usuário cadastrado",
            "id": usuario.id
        }), 201

    @staticmethod
    def atualizar(id):
        dados = request.json
        valida_dados = UsuarioController.valida_dados(dados)
        if valida_dados is not True:
            return valida_dados

        existente = UsuarioServices.consultar_email(dados["email"])
        if existente and existente.id != id:
            return jsonify({"erro": "Já existe um usuário com esse email"}), 409

        usuario = UsuarioServices.atualiza_usuario(
            id=id,
            nome=dados["nome"],
            email=dados["email"],
            setor=dados.get("setor")
        )

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        return jsonify({
            "mensagem": "Usuário atualizado",
            "id": usuario.id
        })

    @staticmethod
    def excluir(id):
        resultado = UsuarioServices.exclui_usuario(id)

        if resultado is None:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        if resultado == "possui_chamados":
            return jsonify({"erro": "Não é possível excluir um usuário que possui chamados"}), 409

        return jsonify({
            "mensagem": "Usuário excluído",
            "id": resultado.id
        })

    @staticmethod
    def listar_chamados(id):
        chamados = UsuarioServices.lista_chamados_do_usuario(id)

        if chamados is None:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        return jsonify(chamados)
