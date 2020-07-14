import sys
import datetime

from action import ActionAcordo, ActionSolicitacao, ActionVaga, ActionVeiculo, ActionUsuario

USER_CPF = None

def request_int(msg):
    while (True):
        try:
            return int(input(msg))
        except:
            pass

def request_str(msg):
    while (True):
        try:
            return input(msg)
        except:
            pass

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
        selected_mode = request_int(("Digite o código relativo ao perfil que você quer usar: "))

    return "home_proprietario" if selected_mode == 1 else "home_motorista"


def home_motorista_screen():
    global USER_CPF
    selected_action = -1

    future_acordos_details = ActionAcordo.list_future_by_motorista(USER_CPF)

    if future_acordos_details is None:
        print("\nNão conseguimos obter seus acordos futuros")
    elif len(future_acordos_details):
        print("\nSeus acordos futuros:")
        for acordo in future_acordos_details:
            print(acordo)

    while selected_action not in [0, 1, 2, 3, 4, 5, 6]:
        print()
        print("""
        --------------------------------------------------------------------
        | 1 - Inserir um veículo                                           |
        | 2 - Listar minhas solicitações (com e sem resposta)              |
        | 3 - Listar vagas para alugar                                     |
        | 4 - Avaliar proprietários                                        |
        | 5 - Ver minha nota média                                         |
        | 6 - Logout                                                       |
        |                                                                  |
        | 0 - Encerrar o Easy Park                                         |
        --------------------------------------------------------------------
        """)
        selected_action = request_int(("Digite o código relativo à ação que deseja executar: "))

    if selected_action == 0:
        return "exit_system"

    if selected_action == 1:
        modelo =request_str("Modelo: ")
        ano = request_int(("Ano: "))
        cor =request_str("Cor: ")
        placa =request_str("Placa: ")

        if ActionVeiculo.insert(USER_CPF, modelo, ano, cor, placa):
            print("\nVeículo adicionado com sucesso!")
        else:
            print("\nNão conseguimos adicionar este veículo")
    elif selected_action == 2:
        solicitacoes_details = ActionSolicitacao.list_by_motorista(USER_CPF)

        if solicitacoes_details is None:
            print("\nNão conseguimos listar suas solicitações")
        elif len(solicitacoes_details):
            print("\nSuas solicitações:\n")
            for solicitacao in solicitacoes_details:
                print("id:", solicitacao["id_solicitacao"])
                print("id da vaga:", solicitacao["id_vaga"])
                print("início:", solicitacao["inicio"].strftime("%d/%m/%Y, %H:%M"))
                print("fim:", solicitacao["fim"].strftime("%d/%m/%Y, %H:%M"))
                print("resposta:", solicitacao["resposta"])
                print()
        else:
            print("\nNão há solicitações a listar")
    elif selected_action == 3:
        date_fmt = "%d/%m/%Y %H:%M"

        inicio = datetime.datetime.strptime(input("Início do uso (formato dd/mm/aaaa hh:mm): "), date_fmt)
        fim = datetime.datetime.strptime(input("Fim do uso (formato dd/mm/aaaa hh:mm): "), date_fmt)

        latitude = float(input("Latitude desejada: "))
        longitude = float(input("Longitude desejada: "))

        vagas_details, vaga = ActionVaga.list_by_location_and_time(USER_CPF, inicio, fim, latitude, longitude)

        if vagas_details is None:
            print("\nNão conseguimos listar as vagas disponíveis")
        elif vaga:
            print("\nVagas disponíveis:\n")
            for vaga in vagas_details:
                print("id:", vaga["id_vaga"])
                print("latitude:", vaga["latitude"])
                print("longitude:", vaga["longitude"])
                print()

            id_vaga = request_int(("Digite o id da vaga desejada: "))

            if ActionSolicitacao.insert(id_vaga, USER_CPF, inicio, fim):
                print("\nSolicitação realizada com sucesso!")
            else:
                print("\nNão conseguimos realizar a sua solicitação")
        else:
            if len(vagas_details) > 0:
                print("\nNão há vagas disponíveis, mas veja os estacionamentos próximos:\n")
                for e in vagas_details:
                    print("nome:", e["nome"])
                    print("latitude:", e["latitude"])
                    print("longitude:", e["longitude"])
                    print()
            else:
                print("\nNão há vagas nem estacionamentos disponíveis próximos à localização desejada")  
    elif selected_action == 4:
        past_acordos_details = ActionAcordo.list_past_by_motorista(USER_CPF)

        if past_acordos_details is None:
            print("\nNão conseguimos listar seus acordos")
        else:
            for acordo in past_acordos_details:
                print(acordo)
            id_acordo = request_int(("Digite o id do acordo cujo proprietário você deseja avaliar: "))

            nota = 0
            while (nota < 1 or nota > 5):
                nota = request_int(("Avalie com uma nota de 1 a 5: "))

            if ActionAcordo.insert_nota_to_proprietario(id_acordo, nota):
                print("\nNota registrada com sucesso!")
            else:
                print("\nNão conseguimos registrar sua nota")
    elif selected_action == 5:
        nota_media = ActionUsuario.get_nota_media(USER_CPF, "MOTORISTA")
        if nota_media is None:
            print("\nNão conseguimos obter sua nota média")
        elif nota_media != -1:
            print("\nSua nota média é", nota_media)
        else:
            print("\nVocê ainda não recebeu notas")
    elif selected_action == 6:
        USER_CPF = None
        return "initial"

    return "home_motorista"


def home_proprietario_screen():
    global USER_CPF
    selected_action = -1

    future_acordos_details = ActionAcordo.list_future_by_proprietario(USER_CPF)

    if future_acordos_details is None:
        print("\nNão conseguimos obter seus acordos futuros")
    elif len(future_acordos_details):
        print("\nSeus acordos futuros:")
        for acordo in future_acordos_details:
            print(acordo)

    solicitacoes_details = ActionSolicitacao.list_unanswered_by_proprietario(USER_CPF)

    if solicitacoes_details is None:
        print("\nNão conseguimos obter as solicitações para suas vagas")
    elif len(solicitacoes_details):
        print("\nAviso: você tem uma ou mais solicitações de vaga para responder")

    while selected_action not in [0, 1, 2, 3, 4, 5, 6]:
        print()
        print("""
        --------------------------------------------------------------------
        | 1 - Alterar endereço                                             |
        | 2 - Inserir uma vaga                                             |
        | 3 - Listar e responder a solicitações recebidas                  |
        | 4 - Avaliar motoristas                                           |
        | 5 - Ver minha nota média                                         |
        | 6 - Logout                                                       |
        |                                                                  |
        | 0 - Encerrar o Easy Park                                         |
        --------------------------------------------------------------------
        """)
        selected_action = request_int(("Digite o código relativo à ação que deseja executar: "))

    if selected_action == 0:
        return "exit_system"

    if selected_action == 1:
        logradouro =request_str("Novo logradouro do endereço (ex.: Avenida Paulista): ")
        numero =request_str("Novo número do endereço: ")
        complemento =request_str("Novo complemento (pressione enter se não houver): ")
        cep =request_str("Novo CEP (somente dígitos): ")

        if ActionUsuario.update_endereco_proprietario(USER_CPF, logradouro, numero, complemento, cep):
            print("\nEndereço atualizado com sucesso!")
        else:
            print("\nNão conseguimos atualizar o seu endereço")
    elif selected_action == 2: 
        bairro =request_str("Bairro da vaga: ")
        latitude = float(input("Latitude: "))
        longitude = float(input("Longitude: "))
        largura = float(input("Largura: "))
        comprimento = float(input("Comprimento: "))
        preco = float(input("Preço por hora: "))

        if ActionVaga.insert(USER_CPF, bairro, latitude, longitude, largura, comprimento, preco):
            print("\nVaga adicionada com sucesso!")
            print("Lembre-se de que ela só poderá ser disponibilizada após a aprovação de um agente municipal")
        else:
            print("\nNão conseguimos adicionar esta vaga")
    elif selected_action == 3:
        solicitacoes_details = ActionSolicitacao.list_unanswered_by_proprietario(USER_CPF)

        if solicitacoes_details is None:
            print("\nNão conseguimos listar as solicitacoes")
        elif len(solicitacoes_details):
            print("\nSolicitações não respondidas:\n")
            for solicitacao in solicitacoes_details:
                print("id:", solicitacao["id_solicitacao"])
                print("cpf do solicitante:", solicitacao["cpf_motorista"])
                print("id da vaga:", solicitacao["id_vaga"])
                print("início:", solicitacao["inicio"].strftime("%d/%m/%Y, %H:%M"))
                print("fim:", solicitacao["fim"].strftime("%d/%m/%Y, %H:%M"))
                print()

            id_solicitacao = request_int(("Digite o id da solicitação a que deseja responder: "))

            resposta = None
            while resposta is None:
                res =request_str("Solicitação aceita ou recusada (a/r)? ")
                if res == "a":
                    resposta = True
                elif res == "r":
                    resposta = False

            if ActionSolicitacao.update_resposta(id_solicitacao, USER_CPF, resposta):
                print("\nResposta registrada com sucesso!")
            else:
                print("\nNão conseguimos registrar sua resposta")
        else:
            print("\nNão há solicitações a responder")
    elif selected_action == 4:
        past_acordos_details = ActionAcordo.list_past_by_proprietario(USER_CPF)

        if past_acordos_details is None:
            print("\nNão conseguimos listar seus acordos")
        else:
            for acordo in past_acordos_details:
                print(acordo)

            id_acordo = request_int(("Digite o id do acordo cujo motorista você deseja avaliar: "))

            nota = 0
            while (nota < 1 or nota > 5):
                nota = request_int(("Avalie com uma nota de 1 a 5: "))

            if ActionAcordo.insert_nota_to_motorista(id_acordo, nota):
                print("\nNota registrada com sucesso!")
            else:
                print("\nNão conseguimos registrar sua nota")
    elif selected_action == 5:
        nota_media = ActionUsuario.get_nota_media(USER_CPF, "PROPRIETARIO")
        if nota_media is None:
            print("\nNão conseguimos obter sua nota média")
        elif nota_media != -1:
            print("\nSua nota média é", nota_media)
        else:
            print("\nVocê ainda não recebeu notas")
    elif selected_action == 6:
        USER_CPF = None
        return "initial"

    return "home_proprietario"


def home_agente_screen():
    global USER_CPF
    selected_action = -1

    while selected_action not in [0, 1, 2, 3, 4]:
        if ActionUsuario.get_bairro_agente(USER_CPF) is None:
            print("\nNão conseguimos encontrar o bairro de atuação deste agente")
        else:
            print("\nBairro de atuação:", ActionUsuario.get_bairro_agente(USER_CPF))
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
        selected_action = request_int(("Digite o código relativo à ação que deseja executar: " ))

    if selected_action == 0:
        return "exit_system"
    
    if selected_action == 1:
        bairro =request_str("Novo bairro: ")

        if ActionUsuario.update_bairro_agente(USER_CPF, bairro):
            print("\nBairro atualizado com sucesso!")
        else:
            print("\nNão conseguimos atualizar o bairro")
    elif selected_action == 2:
        vagas_details = ActionVaga.list_by_agente_bairro(USER_CPF)

        if vagas_details is None:
            print("\nNão conseguimos listar as vagas")
        elif len(vagas_details) == 0:
            print("\nNão há vagas no bairro deste agente")
        else:
            print("\nVagas no bairro:\n")
            for vaga in vagas_details:
                print("id:", vaga["id_vaga"])
                print("latitude:", vaga["latitude"])
                print("longitude:", vaga["longitude"])
                print()
    elif selected_action == 3:
        id_vaga = request_int(("Selecione a vaga pelo id: "))

        avaliacao = None
        while avaliacao is None:
            res =request_str("Vaga aprovada ou reprovada (a/r)? ")
            if res == "a":
                avaliacao = True
            elif res == "r":
                avaliacao = False

        comentario =request_str("Comentário (pressione enter se não houver): ")

        if ActionVaga.insert_avaliacao(id_vaga, USER_CPF, avaliacao, comentario):
            print("\nAvaliação realizada com sucesso!")
        else:
            print("\nNão conseguimos adicionar esta avaliação")
    elif selected_action == 4:
        USER_CPF = None
        return "initial"

    return "home_agente"


def signup_screen():
    user_type = -1
    date_fmt = "%d/%m/%Y"

    nome =request_str("Nome: ")
    cpf =request_str("CPF: ")
    email =request_str("Email: ")
    senha =request_str("Senha: ")
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
        user_type = request_int(("Digite o código relativo ao tipo do usuário: "))

    if user_type == 1:
        registro_municipal =request_str("Registro municipal: ")
        bairro =request_str("Bairro de atuação: ")

        if ActionUsuario.insert_agente(nome, cpf, email, senha, nascimento, registro_municipal, bairro):
            print("\nAgente cadastrado com sucesso!")
        else:
            print("\nNão conseguimos cadastrar este agente")
    elif user_type == 2:
        logradouro =request_str("Logradouro do endereço (ex.: Avenida Paulista): ")
        numero =request_str("Número do endereço: ")
        complemento =request_str("Complemento (pressione enter se não houver): ")
        cep =request_str("CEP (somente dígitos): ")

        if ActionUsuario.insert_proprietario(nome, cpf, email, senha, nascimento, logradouro, numero, complemento, cep):
            print("\nProprietário cadastrado com sucesso!")
        else:
            print("\nNão conseguimos cadastrar este proprietário")
    elif user_type == 3:
        cnh =request_str("Número da CNH (somente dígitos): ")

        if ActionUsuario.insert_motorista(nome, cpf, email, senha, nascimento, cnh):
            print("\nMotorista cadastrado com sucesso!")
        else:
            print("\nNão conseguimos cadastrar este motorista")
    elif user_type == 4:
        logradouro =request_str("Logradouro do endereço (ex.: Avenida Paulista): ")
        numero =request_str("Número do endereço: ")
        complemento =request_str("Complemento (pressione enter se não houver): ")
        cep =request_str("CEP (somente dígitos): ")
        cnh =request_str("Número da CNH (somente dígitos): ")

        if ActionUsuario.insert_proprietario_motorista(nome, cpf, email, senha, nascimento, logradouro, numero, complemento, cep, cnh):
            print("\nProprietário/motorista cadastrado com sucesso!")
        else:
            print("\nNão conseguimos cadastrar este proprietário/motorista")

    return "initial"


def login_screen():
    global USER_CPF
    email =request_str("Email: ")
    senha =request_str("Senha: ")

    USER_CPF, user_type = ActionUsuario.login(email, senha)
    
    if USER_CPF is None:
        print("\nNão encontramos um usuário com as credenciais fornecidas!")
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
        selected_navigation = request_int(("Digite o código relativo à ação que deseja executar: "))


    if selected_navigation == 0:
        return "exit_system"
    if selected_navigation == 1:
        return "signup"
    return "login"


def main():
    print()
    print("""   
          ███████  █████  ███████ ██    ██ ██████   █████  ██████  ██   ██ 
          ██      ██   ██ ██       ██  ██  ██   ██ ██   ██ ██   ██ ██  ██  
          █████   ███████ ███████   ████   ██████  ███████ ██████  █████   
          ██      ██   ██      ██    ██    ██      ██   ██ ██   ██ ██  ██  
          ███████ ██   ██ ███████    ██    ██      ██   ██ ██   ██ ██   ██             
    """)

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
            print("\nAté mais, e obrigado pelos peixes!")
            sys.exit(0)

main()
