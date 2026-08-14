from flask import jsonify, request
from services.chamado_service import ChamadoServices

class ChamadoController():

    @staticmethod
    def valida_dados(dados):
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        if len(dados.get("titulo", "")) < 5:
            return jsonify({"erro": "Título deve ter pelo menos 5 caracteres"}), 400
        if len(dados.get("descricao", "")) < 10:
            return jsonify({"erro": "Descrição deve ter pelo menos 10 caracteres"}), 400
        if dados.get("prioridade") not in ["Baixa", "Média", "Alta"]:
            return jsonify({"erro": "Prioridade deve ser Baixa, Média ou Alta"}), 400
        return True

    @staticmethod
    def listar():
        resultado = ChamadoServices.consulta_chamados()
        return jsonify(resultado)

    @staticmethod
    def listar_abertos():
        resultado = ChamadoServices.consulta_abertos()
        return jsonify(resultado)

    @staticmethod
    def listar_prioridade_alta():
        resultado = ChamadoServices.consulta_prioridade_alta()
        return jsonify(resultado)

    @staticmethod
    def cadastrar():
        dados = request.json
        valida_dados = ChamadoController.valida_dados(dados)
        if valida_dados is not True:
            return valida_dados

        if not dados.get("usuario_id"):
            return jsonify({"erro": "usuario_id é obrigatório"}), 400

        resultado = ChamadoServices.cadastra_chamado(
            titulo=dados["titulo"],
            descricao=dados["descricao"],
            prioridade=dados["prioridade"],
            usuario_id=dados["usuario_id"],
            tecnico=dados.get("tecnico")
        )

        if resultado == "usuario_invalido":
            return jsonify({"erro": "Usuário informado não existe"}), 400

        if resultado == "limite_excedido":
            return jsonify({"erro": "Usuário já possui 5 chamados não encerrados"}), 409

        return jsonify({
            "mensagem": "Chamado cadastrado",
            "id": resultado.id
        }), 201

    @staticmethod
    def atualizar(id):
        dados = request.json
        valida_dados = ChamadoController.valida_dados(dados)
        if valida_dados is not True:
            return valida_dados

        chamado = ChamadoServices.atualiza_chamado(
            id=id,
            titulo=dados["titulo"],
            descricao=dados["descricao"],
            prioridade=dados["prioridade"],
            tecnico=dados.get("tecnico")
        )

        if not chamado:
            return jsonify({"erro": "Chamado não encontrado"}), 404

        return jsonify({
            "mensagem": "Chamado atualizado",
            "id": chamado.id
        })

    @staticmethod
    def excluir(id):
        chamado = ChamadoServices.exclui_chamado(id)
        if not chamado:
            return jsonify({"erro": "Chamado não encontrado"}), 404
        return jsonify({
            "mensagem": "Chamado excluído",
            "id": chamado.id
        })

    @staticmethod
    def iniciar(id):
        resultado = ChamadoServices.inicia_chamado(id)

        if resultado is None:
            return jsonify({"erro": "Chamado não encontrado"}), 404

        if resultado == "status_invalido":
            return jsonify({"erro": "Não é possível iniciar esse chamado"}), 409

        return jsonify({
            "mensagem": "Chamado iniciado",
            "id": resultado.id
        })

    @staticmethod
    def encerrar(id):
        resultado = ChamadoServices.encerra_chamado(id)

        if resultado is None:
            return jsonify({"erro": "Chamado não encontrado"}), 404

        if resultado == "status_invalido":
            return jsonify({"erro": "Não é possível encerrar esse chamado"}), 409

        return jsonify({
            "mensagem": "Chamado encerrado",
            "id": resultado.id
        })

    @staticmethod
    def estatisticas():
        resultado = ChamadoServices.gera_estatisticas()
        return jsonify(resultado)
