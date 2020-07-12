from modelo.relacional import Agente, Motorista, Proprietario, Usuario
from modelo.documentos import Usuario as UsuarioDoc
from modelo.grafos import Agente as AgenteGrafos
from bd.documentos import UsuarioDAO as UsuarioDAODoc
from bd.documentos import AcordoDAO as AcordoDAODoc
from bd.grafos import AgenteDAO as AgenteDAOGrafos
from bd.relacional import UsuarioDAO, MotoristaDAO, ProprietarioDAO, AgenteDAO, VagaDAO
from bd.relacional import AcordoDAO, SolicitacaoDAO

import datetime

class ActionUsuario:

    @staticmethod
    def insert_proprietario(nome, cpf, email, senha, nascimento, logradouro, numero, complemento, cep):
        usuario = Usuario()
        usuarioDao = UsuarioDAO()

        usuario.set_cpf(cpf)
        usuario.set_nome(nome)
        usuario.set_email(email)
        usuario.set_senha(senha)
        usuario.set_nascimento(nascimento)

        usuarioDAODoc = UsuarioDAODoc()
        usuarioDoc = UsuarioDoc()
        usuarioDoc.set_cpf(cpf)

        try:
            usuarioDao.insert(usuario)
            usuarioDAODoc.insert(usuarioDoc)
        except:
            return False

        proprietario = Proprietario()
        proprietarioDao = ProprietarioDAO()

        proprietario.set_cpf_usuario(cpf)
        proprietario.set_logradouro(logradouro)
        proprietario.set_numero(numero)
        proprietario.set_complemento(complemento)
        proprietario.set_cep(cep)

        try:
            proprietarioDao.insert(proprietario)
        except:
            usuarioDao.remove(cpf)
            return False
        else:
            return True

    @staticmethod
    def insert_motorista(nome, cpf, email, senha, nascimento, cnh):
        usuario = Usuario()
        usuarioDao = UsuarioDAO()

        usuario.set_cpf(cpf)
        usuario.set_nome(nome)
        usuario.set_email(email)
        usuario.set_senha(senha)
        usuario.set_nascimento(nascimento)

        usuarioDAODoc = UsuarioDAODoc()
        usuarioDoc = UsuarioDoc()
        usuarioDoc.set_cpf(cpf)

        try:
            usuarioDao.insert(usuario)
            usuarioDAODoc.insert(usuarioDoc)
        except:
            return False

        motorista = Motorista()
        motoristaDao = MotoristaDAO()

        motorista.set_cpf_usuario(cpf)
        motorista.set_cnh(cnh)

        try:
            motoristaDao.insert(motorista)
        except:
            usuarioDao.remove(cpf)
            return False
        else:
            return True

    @staticmethod
    def insert_proprietario_motorista(nome, cpf, email, senha, nascimento, logradouro, numero, complemento, cep, cnh):
        usuario = Usuario()
        usuarioDao = UsuarioDAO()

        usuario.set_cpf(cpf)
        usuario.set_nome(nome)
        usuario.set_email(email)
        usuario.set_senha(senha)
        usuario.set_nascimento(nascimento)

        usuarioDAODoc = UsuarioDAODoc()
        usuarioDoc = UsuarioDoc()
        usuarioDoc.set_cpf(cpf)

        try:
            usuarioDao.insert(usuario)
            usuarioDAODoc.insert(usuarioDoc)
        except:
            return False

        proprietario = Proprietario()
        proprietarioDao = ProprietarioDAO()

        proprietario.set_cpf_usuario(cpf)
        proprietario.set_logradouro(logradouro)
        proprietario.set_numero(numero)
        proprietario.set_complemento(complemento)
        proprietario.set_cep(cep)

        try:
            proprietarioDao.insert(proprietario)
        except:
            usuarioDao.remove(cpf)
            return False

        motorista = Motorista()
        motoristaDao = MotoristaDAO()

        motorista.set_cpf_usuario(cpf)
        motorista.set_cnh(cnh)

        try:
            motoristaDao.insert(motorista)
        except:
            motoristaDao.remove(cpf)
            usuarioDao.remove(cpf)
            return False
        else:
            return True

    @staticmethod
    def insert_agente(nome, cpf, email, senha, nascimento, registro_municipal, bairro):
        usuario = Usuario()
        usuarioDao = UsuarioDAO()

        usuario.set_cpf(cpf)
        usuario.set_nome(nome)
        usuario.set_email(email)
        usuario.set_senha(senha)
        usuario.set_nascimento(nascimento)

        agenteDAOGrafos = AgenteDAOGrafos()
        agenteGrafos = AgenteGrafos()
        agenteGrafos.set_cpf(cpf)
        agenteGrafos.set_bairro(bairro)

        try:
            usuarioDao.insert(usuario)
            agenteDAOGrafos.insert(agenteGrafos)
        except:
            return False

        agente = Agente()
        agenteDao = AgenteDAO()

        agente.set_cpf_usuario(cpf)
        agente.set_registro_municipal(registro_municipal)

        try:
            agenteDao.insert(agente)
        except:
            usuarioDao.remove(cpf)
            return False
        else:
            return True

    @staticmethod
    def login(email, senha):
        usuarioDao = UsuarioDAO()
        agenteDao = AgenteDAO()
        proprietarioDao = ProprietarioDAO()
        motoristaDao = MotoristaDAO()

        try:
            usuario = usuarioDao.get(email, senha)
            if usuario is not None:
                cpf = usuario.get_cpf()

                if agenteDao.get(cpf) is not None:
                    return cpf, "agente"
                if proprietarioDao.get(cpf) is not None:
                    if motoristaDao.get(cpf) is not None:
                        return cpf, "proprietario_motorista"
                    return cpf, "proprietario"
                if motoristaDao.get(cpf) is not None:
                    return cpf, "motorista"
            
            return None, None
        except:
            return None, None
    
    @staticmethod
    def get_nota_media(cpf, tipo_usuario):
        acordoDao = AcordoDAO()
        solicitacaoDao = SolicitacaoDAO()
        acordoDAODoc = AcordoDAODoc()

        soma_nota = 0
        qtde_notas = 0

        if tipo_usuario == "MOTORISTA":
            try:
                acordos = acordoDao.list()
                
                for a in acordos:
                    s = solicitacaoDao.get(a.get_id_solicitacao())

                    now = datetime.datetime.now()
                    if s.get_cpf_motorista() == cpf and s.getFim() < now:
                        nota = acordoDAODoc.get(a.get_id_acordo()).get_nota_PM()
                        if nota is not None:
                            soma_nota += nota
                            qtde_notas += 1
            except:
                return None
        elif tipo_usuario == "PROPRIETARIO":
            try:
                acordos = acordoDao.list()
                vagaDao = VagaDAO()
                
                for a in acordos:
                    s = solicitacaoDao.get(a.get_id_solicitacao())
                    v = vagaDao.get(s.get_id_vaga())

                    now = datetime.datetime.now()
                    if v.get_cpf_proprietario() == cpf and s.getFim() < now:
                        nota = acordoDAODoc.get(a.get_id_acordo()).get_nota_MP()
                        if nota is not None:
                            soma_nota += nota
                            qtde_notas += 1
            except:
                return None
        
        if qtde_notas:
            return soma_nota / qtde_notas
        else:
            return -1

    @staticmethod
    def update_endereco_proprietario(cpf, logradouro, numero, complemento, cep):
        proprietarioDAO = ProprietarioDAO()

        try:
            proprietario = proprietarioDAO.get(cpf)
            proprietario.set_logradouro(logradouro)
            proprietario.set_numero(numero)
            proprietario.set_complemento(complemento)
            proprietario.set_cep(cep)

            proprietarioDAO.update(proprietario)
        except:
            return False
        else:
            return True

    @staticmethod
    def update_bairro_agente(cpf, bairro):
        agenteDAOGrafos = AgenteDAOGrafos()

        try:
            agenteGrafos = agenteDAOGrafos.get(cpf)
            agenteGrafos.set_bairro(bairro)
            agenteDAOGrafos.update(agenteGrafos)
        except:
            return False
        else:
            return True
