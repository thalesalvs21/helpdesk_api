from repositories.chamado_repository import ChamadoRepository
from repositories.usuario_repository import UsuarioRepository

PROXIMO_STATUS = {
    "Aberto": "Em atendimento",
    "Em atendimento": "Encerrado",
}

class ChamadoServices():
    @staticmethod
    def consulta_chamados():
        return ChamadoServices._serializa(ChamadoRepository.consulta_tudo())

    @staticmethod
    def consulta_abertos():
        return ChamadoServices._serializa(ChamadoRepository.consulta_por_status("Aberto"))

    @staticmethod
    def consulta_prioridade_alta():
        return ChamadoServices._serializa(ChamadoRepository.consulta_por_prioridade("Alta"))

    @staticmethod
    def cadastra_chamado(**kwargs):
        usuario = UsuarioRepository.consulta_um(kwargs["usuario_id"])
        if not usuario:
            return "usuario_invalido"

        total_abertos = ChamadoRepository.conta_nao_encerrados(kwargs["usuario_id"])
        if total_abertos >= 5:
            return "limite_excedido"

        return ChamadoRepository.cadastrar_chamado(kwargs)

    @staticmethod
    def atualiza_chamado(id, **kwargs):
        return ChamadoRepository.atualizar_chamado(id, kwargs)

    @staticmethod
    def exclui_chamado(id):
        chamado = ChamadoRepository.consulta_um(id)
        if not chamado:
            return None
        ChamadoRepository.excluir_chamado(chamado)
        return chamado

    @staticmethod
    def inicia_chamado(id):
        return ChamadoServices._avanca_status(id, "Aberto")

    @staticmethod
    def encerra_chamado(id):
        return ChamadoServices._avanca_status(id, "Em atendimento")

    @staticmethod
    def _avanca_status(id, status_esperado):
        chamado = ChamadoRepository.consulta_um(id)
        if not chamado:
            return None
        if chamado.status != status_esperado:
            return "status_invalido"
        return ChamadoRepository.atualizar_status(chamado, PROXIMO_STATUS[status_esperado])

    @staticmethod
    def gera_estatisticas():
        return {
            "usuarios": UsuarioRepository.conta_total_usuarios(),
            "chamados": ChamadoRepository.conta_total(),
            "abertos": ChamadoRepository.conta_por_status("Aberto"),
            "em_atendimento": ChamadoRepository.conta_por_status("Em atendimento"),
            "encerrados": ChamadoRepository.conta_por_status("Encerrado")
        }

    @staticmethod
    def _serializa(chamados):
        resultado = []
        for chamado in chamados:
            resultado.append({
                "id": chamado.id,
                "titulo": chamado.titulo,
                "descricao": chamado.descricao,
                "prioridade": chamado.prioridade,
                "status": chamado.status,
                "tecnico": chamado.tecnico,
                "data_abertura": chamado.data_abertura.strftime("%d/%m/%Y %H:%M"),
                "usuario_id": chamado.usuario_id
            })
        return resultado
