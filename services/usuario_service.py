from repositories.usuario_repository import UsuarioRepository
from repositories.chamado_repository import ChamadoRepository

class UsuarioServices():
    @staticmethod
    def consulta_usuarios():
        usuarios = UsuarioRepository.consulta_tudo()

        resultado = []
        for usuario in usuarios:
            resultado.append({
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "setor": usuario.setor
            })
        return resultado

    @staticmethod
    def cadastra_usuario(**kwargs):
        usuario = UsuarioRepository.cadastrar_usuario(kwargs)
        return usuario

    @staticmethod
    def consultar_email(email):
        return UsuarioRepository.pesquisa_email(email)

    @staticmethod
    def atualiza_usuario(id, **kwargs):
        usuario = UsuarioRepository.atualizar_usuario(id, kwargs)
        return usuario

    @staticmethod
    def exclui_usuario(id):
        usuario = UsuarioRepository.consulta_um(id)
        if not usuario:
            return None

        chamados = ChamadoRepository.consulta_por_usuario(id)
        if len(chamados) > 0:
            return "possui_chamados"

        UsuarioRepository.excluir_usuario(usuario)
        return usuario

    @staticmethod
    def lista_chamados_do_usuario(id):
        usuario = UsuarioRepository.consulta_um(id)
        if not usuario:
            return None

        chamados = ChamadoRepository.consulta_por_usuario(id)

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
