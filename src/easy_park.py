import sys
import datetime

from action import ActionAcordo, ActionSolicitacao, ActionVaga, ActionVeiculo, ActionUsuario

USER_CPF = None

def home_proprietario_motorista_screen():
    selected_mode = -1

    while selected_mode not in [1, 2]:
        print()
        print("""
        --------------------------------------------------------------------
        | 1 - Proprietário                                                 |
        | 2 - Motorista                                                    |
        --------------------------------------------------------------------
        """)
        selected_mode = int(input("Digite o código relativo ao perfil que você quer usar: "))

    return "home_proprietario" if selected_mode == 1 else "home_motorista"


def home_motorista_screen():
    global USER_CPF
    selected_action = -1

    future_acordos_details = ActionAcordo.list_future_by_motorista(USER_CPF)

    if future_acordos_details is None:
        print("Não conseguimos obter seus acordos futuros")
    elif len(future_acordos_details):
        print("Seus acordos futuros:")
        for acordo in future_acordos_details:
            print(acordo)

    while selected_action not in [0, 1, 2, 3, 4, 5, 6]:
        print()
        print("""
        --------------------------------------------------------------------
        | 1 - Inserir um veículo                                           |
        | 2 - Listar minhas solicitações (com e sem resposta)              |
        | 3 - Listar vagas para alugar                                     |
        | 4 - Avaliar proprietários ou fazer denúncias                     |
        | 5 - Ver minha nota média                                         |
        | 6 - Logout                                                       |
        |                                                                  |
        | 0 - Encerrar o Easy Park                                         |
        --------------------------------------------------------------------
        """)
        selected_action = int(input("Digite o código relativo à ação que deseja executar: "))

    if selected_action == 0:
        return "exit_system"

    if selected_action == 1:
        modelo = input("Modelo: ")
        ano = int(input("Ano: "))
        cor = input("Cor: ")
        placa = input("Placa: ")

        if ActionVeiculo.insert(USER_CPF, modelo, ano, cor, placa):
            print("Veículo adicionado com sucesso!")
        else:
            print("Não conseguimos adicionar este veículo")
    elif selected_action == 2:
        solicitacoes_details = ActionSolicitacao.list_by_motorista(USER_CPF)

        if solicitacoes_details is None:
            print("Não conseguimos listar suas solicitações")
        elif len(solicitacoes_details):
            for solicitacao in solicitacoes_details:
                print(solicitacao)
        else:
            print("Não há solicitações a listar")
    elif selected_action == 3:
        date_fmt = "%d/%m/%Y %H:%M"

        inicio = datetime.datetime.strptime(input("Início do uso (formato dd/mm/aaaa hh:mm): "), date_fmt)
        fim = datetime.datetime.strptime(input("Fim do uso (formato dd/mm/aaaa hh:mm): "), date_fmt)

        latitude = float(input("Latitude desejada: "))
        longitude = float(input("Longitude desejada: "))

        vagas_details, vaga = ActionVaga.list_by_location_and_time(USER_CPF, inicio, fim, latitude, longitude)

        if vagas_details is None:
            print("Não conseguimos listar as vagas disponíveis")
        else:
            if not vaga:
                if len(vagas_details) > 0:
                    print("Não há vagas disponíveis, mas veja os estacionamentos próximos:")
                else:
                    print("Não há vagas nem estacionamentos disponíveis próximos à localização desejada")
            
            for vaga in vagas_details:
                print(vaga)

            if len(vagas_details):
                id_vaga = int(input("Digite o id da vaga desejada: "))

                if ActionSolicitacao.insert(id_vaga, USER_CPF, inicio, fim):
                    print("Solicitação realizada com sucesso!")
                else:
                    print("Não conseguimos realizar a sua solicitação")
    elif selected_action == 4:
        past_acordos_details = ActionAcordo.list_past_by_motorista(USER_CPF)

        if past_acordos_details is None:
            print("Não conseguimos listar seus acordos")
        else:
            for acordo in past_acordos_details:
                print(acordo)
            id_acordo = int(input("Digite o id do acordo cujo proprietário você deseja avaliar: "))

            nota = 0
            while (nota < 1 or nota > 5):
                nota = int(input("Avalie com uma nota de 1 a 5: "))

            if ActionAcordo.insert_nota_to_proprietario(id_acordo, nota):
                print("Nota registrada com sucesso!")
            else:
                print("Não conseguimos registrar sua nota")
    elif selected_action == 5:
        nota_media = ActionUsuario.get_nota_media(USER_CPF, "MOTORISTA")
        if nota_media is None:
            print("Não conseguimos obter sua nota média")
        elif nota_media != -1:
            print("Sua nota média é ", nota_media)
        else:
            print("Você ainda não recebeu notas")
    elif selected_action == 6:
        USER_CPF = None
        return "initial"

    return "home_motorista"


def home_proprietario_screen():
    global USER_CPF
    selected_action = -1

    future_acordos_details = ActionAcordo.list_future_by_proprietario(USER_CPF)

    if future_acordos_details is None:
        print("Não conseguimos obter seus acordos futuros")
    elif len(future_acordos_details):
        print("Seus acordos futuros:")
        for acordo in future_acordos_details:
            print(acordo)

    solicitacoes_details = ActionSolicitacao.list_unanswered_by_proprietario(USER_CPF)

    if solicitacoes_details is None:
        print("Não conseguimos obter as solicitações para suas vagas")
    elif len(solicitacoes_details):
        print("Você tem uma ou mais solicitações de vaga para responder")

    while selected_action not in [0, 1, 2, 3, 4, 5, 6]:
        print()
        print("""
        --------------------------------------------------------------------
        | 1 - Alterar endereço                                             |
        | 2 - Inserir uma vaga                                             |
        | 3 - Responder a uma solicitação de uso de vaga                   |
        | 4 - Avaliar motoristas ou fazer denúncias                        |
        | 5 - Ver minha nota média                                         |
        | 6 - Logout                                                       |
        |                                                                  |
        | 0 - Encerrar o Easy Park                                         |
        --------------------------------------------------------------------
        """)
        selected_action = int(input("Digite o código relativo à ação que deseja executar: "))

    if selected_action == 0:
        return "exit_system"

    if selected_action == 1:
        logradouro = input("Novo logradouro do endereço (ex.: Avenida Paulista): ")
        numero = input("Novo número do endereço: ")
        complemento = input("Novo complemento (pressione enter se não houver): ")
        cep = input("Novo CEP (somente dígitos): ")

        if ActionUsuario.update_endereco_proprietario(USER_CPF, logradouro, numero, complemento, cep):
            print("Endereço atualizado com sucesso!")
        else:
            print("Não conseguimos atualizar o seu endereço")
    elif selected_action == 2: 
        bairro = input("Bairro da vaga: ")
        latitude = float(input("Latitude: "))
        longitude = float(input("Longitude: "))
        largura = float(input("Largura: "))
        comprimento = float(input("Comprimento: "))
        preco = float(input("Preço por hora: "))

        if ActionVaga.insert(USER_CPF, bairro, latitude, longitude, largura, comprimento, preco):
            print("Vaga adicionada com sucesso!")
            print("Lembre-se de que ela só poderá ser disponibilizada após a aprovação de um agente municipal")
        else:
            print("Não conseguimos adicionar esta vaga")
    elif selected_action == 3:
        solicitacoes_details = ActionSolicitacao.list_unanswered_by_proprietario(USER_CPF)

        if solicitacoes_details is None:
            print("Não conseguimos listar as solicitacoes")
        else:
            for solicitacao in solicitacoes_details:
                print(solicitacao)
            id_solicitacao = int(input("Digite o id da solicitação a que deseja responder: "))

            resposta = None
            while resposta is None:
                res = input("Solicitação aceita ou recusada (a/r)? ")
                if res == "a":
                    resposta = True
                elif res == "r":
                    resposta = False

            if ActionSolicitacao.update_resposta(id_solicitacao, USER_CPF, resposta):
                print("Resposta registrada com sucesso!")
            else:
                print("Não conseguimos registrar sua resposta")
    elif selected_action == 4:
        past_acordos_details = ActionAcordo.list_past_by_proprietario(USER_CPF)

        if past_acordos_details is None:
            print("Não conseguimos listar seus acordos")
        else:
            for acordo in past_acordos_details:
                print(acordo)

            id_acordo = int(input("Digite o id do acordo cujo motorista você deseja avaliar: "))

            nota = 0
            while (nota < 1 or nota > 5):
                nota = int(input("Avalie com uma nota de 1 a 5: "))

            if ActionAcordo.insert_nota_to_motorista(id_acordo, nota):
                print("Nota registrada com sucesso!")
            else:
                print("Não conseguimos registrar sua nota")
    elif selected_action == 5:
        nota_media = ActionUsuario.get_nota_media(USER_CPF, "PROPRIETARIO")
        if nota_media is None:
            print("Não conseguimos obter sua nota média")
        elif nota_media != -1:
            print("Sua nota média é ", nota_media)
        else:
            print("Você ainda não recebeu notas")
    elif selected_action == 6:
        USER_CPF = None
        return "initial"

    return "home_proprietario"


def home_agente_screen():
    global USER_CPF
    selected_action = -1

    while selected_action not in [0, 1, 2, 3, 4]:
        print()
        print("""
        --------------------------------------------------------------------
        | 1 - Alterar bairro de atuação                                    |
        | 2 - Listar vagas no bairro de atuação                            |
        | 3 - Avaliar uma vaga                                             |
        | 4 - Logout                                                       |
        |                                                                  |
        | 0 - Encerrar o Easy Park                                         |
        --------------------------------------------------------------------
        """)
        selected_action = int(input("Digite o código relativo à ação que deseja executar: " ))

    if selected_action == 0:
        return "exit_system"
    
    if selected_action == 1:
        bairro = input("Novo bairro: ")

        if ActionUsuario.update_bairro_agente(USER_CPF, bairro):
            print("Bairro atualizado com sucesso!")
        else:
            print("Não conseguimos atualizar o bairro")
    elif selected_action == 2:
        vagas_details = ActionVaga.list_by_agente_bairro(USER_CPF)

        if vagas_details is None:
            print("Não conseguimos listar as vagas")
        elif len(vagas_details) == 0:
            print("Não há vagas no bairro deste agente")
        else:
            for vaga in vagas_details:
                print(vaga)
    elif selected_action == 3:
        id_vaga = int(input("Selecione a vaga pelo id: "))

        avaliacao = None
        while avaliacao is None:
            res = input("Vaga aprovada ou reprovada (a/r)? ")
            if res == "a":
                avaliacao = True
            elif res == "r":
                avaliacao = False

        comentario = input("Comentário (pressione enter se não houver): ")

        if ActionVaga.insert_avaliacao(id_vaga, USER_CPF, avaliacao, comentario):
            print("Avaliação realizada com sucesso!")
        else:
            print("Não conseguimos adicionar esta avaliação")
    elif selected_action == 4:
        USER_CPF = None
        return "initial"

    return "home_agente"


def signup_screen():
    user_type = -1
    date_fmt = "%d/%m/%Y"

    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    senha = input("Senha: ")
    nascimento = datetime.datetime.strptime(input("Data de nascimento (formato dd/mm/aaaa): "), date_fmt)

    while user_type not in [1, 2, 3, 4]:
        print()
        print("""
        --------------------------------------------------------------------
        | 1 - Agente municipal                                             |
        | 2 - Proprietário                                                 |
        | 3 - Motorista                                                    |
        | 4 - Proprietário e motorista                                     |
        --------------------------------------------------------------------
        """)
        user_type = int(input("Digite o código relativo ao tipo do usuário: "))

    if user_type == 1:
        registro_municipal = input("Registro municipal: ")
        bairro = input("Bairro de atuação: ")

        if ActionUsuario.insert_agente(nome, cpf, email, senha, nascimento, registro_municipal, bairro):
            print("Agente cadastrado com sucesso!")
        else:
            print("Não conseguimos cadastrar este agente")
    elif user_type == 2:
        logradouro = input("Logradouro do endereço (ex.: Avenida Paulista): ")
        numero = input("Número do endereço: ")
        complemento = input("Complemento (pressione enter se não houver): ")
        cep = input("CEP (somente dígitos): ")

        if ActionUsuario.insert_proprietario(nome, cpf, email, senha, nascimento, logradouro, numero, complemento, cep):
            print("Proprietário cadastrado com sucesso!")
        else:
            print("Não conseguimos cadastrar este proprietário")
    elif user_type == 3:
        cnh = input("Número da CNH (somente dígitos): ")

        if ActionUsuario.insert_motorista(nome, cpf, email, senha, nascimento, cnh):
            print("Motorista cadastrado com sucesso!")
        else:
            print("Não conseguimos cadastrar este motorista")
    elif user_type == 4:
        logradouro = input("Logradouro do endereço (ex.: Avenida Paulista): ")
        numero = input("Número do endereço: ")
        complemento = input("Complemento (pressione enter se não houver): ")
        cep = input("CEP (somente dígitos): ")
        cnh = input("Número da CNH (somente dígitos): ")

        if ActionUsuario.insert_proprietario_motorista(nome, cpf, email, senha, nascimento, logradouro, numero, complemento, cep, cnh):
            print("Proprietário/motorista cadastrado com sucesso!")
        else:
            print("Não conseguimos cadastrar este proprietário/motorista")

    return "initial"


def login_screen():
    global USER_CPF
    email = input("Email: ")
    senha = input("Senha: ")

    USER_CPF, user_type = ActionUsuario.login(email, senha)
    
    if USER_CPF is None:
        print("Não encontramos um usuário com as credenciais fornecidas!")
        return "initial"

    return "home_" + user_type


def initial_screen():
    selected_navigation = -1

    while selected_navigation not in [0, 1, 2]:
        print()
        print("""
        --------------------------------------------------------------------
        | 1 - Cadastro de usuário                                          |
        | 2 - Login                                                        |
        |                                                                  |
        | 0 - Encerrar o Easy Park                                         |
        --------------------------------------------------------------------
        """)
        selected_navigation = int(input("Digite o código relativo à ação que deseja executar: "))

    if selected_navigation == 0:
        return "exit_system"
    if selected_navigation == 1:
        return "signup"
    return "login"


def main():
    navigation = "initial"

    while (True):
        if navigation == "initial":
            navigation = initial_screen()
        elif navigation == "signup":
            navigation = signup_screen()
        elif navigation == "login":
            navigation = login_screen()
        elif navigation == "home_agente":
            navigation = home_agente_screen()
        elif navigation == "home_proprietario":
            navigation = home_proprietario_screen()
        elif navigation == "home_motorista":
            navigation = home_motorista_screen()
        elif navigation == "home_proprietario_motorista":
            navigation = home_proprietario_motorista_screen()
        elif navigation == "exit_system":
            print("Até mais, e obrigado pelos peixes!")
            sys.exit(0)

main()
