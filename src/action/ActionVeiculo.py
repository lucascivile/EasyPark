from modelo.relacional import Veiculo
from bd.relacional import VeiculoDAO

class ActionVeiculo:

    @staticmethod
    def insert(cpf, modelo, ano, cor, placa):
        veiculo = Veiculo()

        veiculo.set_cpf_motorista(cpf)
        veiculo.set_modelo(modelo)
        veiculo.set_ano(ano)
        veiculo.set_cor(cor)
        veiculo.set_placa(placa)

        veiculoDAO = VeiculoDAO()

        try:
            veiculoDAO.insert(veiculo)
        except:
            return False
        else:
            return True
