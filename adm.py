import socket
import json
import time
import pickle

candidato = dict()
candidatos = []
usuario = dict()
usuarios = []

def cadastrar_candidato():
    candidato.clear()
    while True:
        print('=======  CADASTRANDO CANDIDATO  =======\n')
        candidato['nome'] = str(input('Nome: ')).upper()
        
        while True:
            try:
                candidato['numero'] = int(input('Numéro: '))
                break
            except:
                print('ERRO! Digite apenas NÚMEROS!')

        candidato['total_votos'] = 0
        candidatos.append(candidato.copy())

        candidatos_salve_json = { "candidatos" : candidatos }

        with open('candidatos.json', 'w', encoding='utf-8') as candidatos_json:
            json.dump(candidatos_salve_json, candidatos_json, indent=4, ensure_ascii=False)

        while True:
            resposta = str(input('Quer continuar adicionando Candidato? [S/N]')).upper()[0]
            if resposta in 'SN':
                break
            print('ERRO! Digite apenas S ou N.')

        if resposta == 'N':
            break

def cadastrar_usuario():
    usuario.clear()

    while True:
        print('=======  CADASTRANDO USUÁRIO  =======\n')
        
        usuario['nome'] = str(input('Nome: '))
        usuario['login'] = str(input('Login: ')).lower()
        usuario['senha'] = str(input('Senha: '))
 
        usuarios.append(usuario.copy())
        print(usuarios)
        usuarios_salve_json = { "usuarios" : usuarios }

        with open('usuarios.json', 'w', encoding='utf-8') as usuarios_json:
            json.dump(usuarios_salve_json, usuarios_json, indent=4, ensure_ascii=False)

        while True:
            resposta = str(input('Quer continuar adicionando USUÁRIO? [S/N]')).upper()[0]
            if resposta in 'SN':
                break
            print('ERRO! Digite apenas S ou N.')

        if resposta == 'N':
            break

def iniciar_votacao():
    duracao_em_minutos = int(input('Duração da Votação em Mintos: '))
    print(f'TEMPO DE VOTÇÃO {duracao_em_minutos} min.\nAGUARDANDO...')
    time.sleep(duracao_em_minutos)
    parar_votacao()
    print('VOTAÇÃO FINALIZADA!')
    

def parar_votacao():
    credenciais = ['parar', '']
    credenciais = pickle.dumps(credenciais)

    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect(ADDR)
    client.send(credenciais)
    client.close()

tela_menu_cadastro = """
[          MENU CADASTRO          ]
|                                 |
|     1 - CADASTRAR CANDIDATO     |
|     2 - CADASTRAR USUÁRIO       |
|     3 - VOLTAR                  |
|                                 |
+---------------------------------+
Selecione: """

tela_menu_principal = """
[          MENU PRINCIPAL          ]
|                                  |
|     1 - INICIAR VOTAÇÃO          |      
|     2 - CADASTRAR ou EXCLUIR     |
|     3 - SAIR                     |
+----------------------------------+
Selecione: """

def menu_cadastro():
    while True:
        try:
            
            opcao = int(input(tela_menu_cadastro))
            if opcao == 1:
                cadastrar_candidato()
                break
            elif opcao == 2:
                cadastrar_usuario()
                break
            elif opcao == 3:
                menu_principal()
                break
            else:
                print('OPÇÃO NÃO ENCONTRADA, OPÇÕES DISPONÍVEIS [ 1, 2 ou 3 ]')
        except:
            print('DIGITE APENAS NÚMEROS!')

def menu_principal():
    while True:
        try:
            
            opcao = int(input(tela_menu_principal))
            if opcao == 1:
                iniciar_votacao()
                break
            elif opcao == 2:
                menu_cadastro()
                break
            elif opcao == 3:
                break
            else:
                print('OPÇÃO NÃO ENCONTRADA, OPÇÕES DISPONÍVEIS [ 1, 2 ou 3 ]')
        except:
            print('DIGITE APENAS NÚMEROS!')

menu_principal()