import socket
import threading
import json
import time



candidato = dict()
candidatos = []

usuario = dict()
usuarios = []

def cadastrar_candidato():
    candidato.clear()
    while True:
        print('=-=-=CADASTRANDO CANDIDATO=-=-=')
        candidato['nome'] = str(input('Nome: '))
        
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
            json.dump(candidatos_salve_json, candidatos_json, indent=4, sort_keys=True, ensure_ascii=False)

        while True:
            resposta = str(input('Quer continuar adicionando Candidato? [S/N]')).upper()[0]
            if resposta in 'SN':
                break
            print('ERRO! Digite apenas S ou N.')

        if resposta == 'N':
            break

def listar_candidatos():
    for i in candidatos:
        print(i.candidato['nome'])

def cadastrar_usuario():
    usuario.clear()

    while True:
        print('=-=-=CADASTRANDO USUÁRIO=-=-=')
        
        usuario['nome'] = str(input('Nome: '))
        usuario['login'] = str(input('Login: '))
        usuario['senha'] = str(input('Senha: '))
 
        usuarios.append(usuario.copy())
        usuarios_salve_json = { "candidatos" : usuarios }

        with open('usuarios.json', 'w', encoding='utf-8') as usuarios_json:
            json.dump(usuarios_salve_json, usuarios_json, indent=4, sort_keys=True, ensure_ascii=False)


        while True:
            resposta = str(input('Quer continuar adicionando USUÁRIO? [S/N]')).upper()[0]
            if resposta in 'SN':
                break
            print('ERRO! Digite apenas S ou N.')

        if resposta == 'N':
            break

def iniciar_eleicao():
    duracao_em_minutos = int(input('Duração da Votação em Mintos: '))
    
    print(f'TEMPO DE VOTÇÃO {duracao_em_minutos} min')
    print('CANDIDATOS DISPONÍVEIS')

    listar_candidatos()

def menu_cadastro():
    while True:
        try:
            opcao = int(input('\n\n1 - CADASTRAR CANDIDATO\n2 - CADASTRAR USUÁRIO\n3 - VOLTAR\n\nSelecione:'))
            if opcao == 1:
                cadastrar_candidato()
                break
            elif opcao == 2:
                cadastrar_usuario()
                break
            elif opcao == 3:
                break
            else:
                print('OPÇÃO NÃO ENCONTRADA, OPÇÕES DISPONÍVEIS [ 1, 2 ou 3 ]')
                time.sleep(2)
        except:
            print('DIGITE APENAS NÚMEROS!')
            time.sleep(2)

menu_cadastro()