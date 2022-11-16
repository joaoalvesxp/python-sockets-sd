import socket
import threading
import pickle
import json

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
print('[ SERVER ] Iniciado no endereço: ', f'{SERVER_IP}:{PORT}')
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

socket_enviar_resultado = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_enviar_resultado.bind((socket.gethostbyname(socket.gethostname()), 5151))

print("\u001b[1;32m[INICIANDO] Iniciando VOTAÇÃO\033[0;0m")

# carrega o arquivo usuarios.json e insere na variavel candidatos
with open('candidatos.json', 'r') as candidatos_cadastrados:
    candidados = json.load(candidatos_cadastrados)

# carrega o arquivo usuarios.json e insere na variavel usuários
with open('usuarios.json', 'r') as usuarios_cadastrados:
    usuarios = json.load(usuarios_cadastrados)


def iniciar_autenticacao(login, senha):
    sucesso_autenticacao = False
    
    for usuario in usuarios['usuarios']:
        if login in usuario.values() and senha in usuario.values():
            print(f"[AUTENTICAÇÃO] Usuário: {usuario['nome']} entrou no sistema usando IP: {cliente_socket.getpeername()[0]}")
            sucesso_autenticacao = True
    
    return sucesso_autenticacao

def contabilizar_voto(voto):
    for candidato in candidados['candidatos']:
        if voto[0] in candidato.values() and voto[1] in candidato.values():
            candidato['total_votos'] += 1
            print(f"[VOTAÇÃO] Candidato {candidato['nome']} - {candidato['numero']} recebeu um voto, TOTAL DE VOTOS [ {candidato['total_votos']} ]")


server.listen()

while True:
    cliente_socket, endereco = server.accept()
    data = cliente_socket.recv(4096)
    credenciais = pickle.loads(data)

    if iniciar_autenticacao(credenciais[0], credenciais[1]):
        resposta = b'sucesso'
        cliente_socket.sendto(resposta, endereco)
        lista_para_votacao = []
                    
        for candidato in candidados['candidatos']:
            lista_para_votacao.append(candidato)
                    
        lista_para_votacao = pickle.dumps(lista_para_votacao)

        cliente_socket.sendto(lista_para_votacao, endereco)

        data = cliente_socket.recv(4096)
        voto = pickle.loads(data)
            
        contabilizar_voto(voto)
    
    elif credenciais[0] == 'parar':
        server.close()
        break
    else:
        resposta = b'falha'
        cliente_socket.sendto(resposta, endereco)



lista_de_candidatos = candidados['candidatos']
candidatos_resultado = []

for i in lista_de_candidatos:
    candidatos_resultado.append([i['nome'], i['numero'], i['total_votos']])

maior_resultado = max(maior_resultado[2] for maior_resultado in candidatos_resultado)

teve_empate = 0
total_de_votos = 0

def enviar_resultados(resultado_votacao):
    mensagem, endereco = socket_enviar_resultado.recvfrom(4096)
    print(f'Mensagem UDP recebida do cliente : {mensagem}')
    socket_enviar_resultado.sendto(resultado_votacao.encode(), endereco)
    socket_enviar_resultado.close()

print("\u001b[1;32m[VOTAÇÃO] ✅ VOTAÇÃO ENCERRADA! MOSTRANDO RESULTADO:\033[0;0m\n")

for i in candidatos_resultado:
    total_de_votos += i[2]
    if str(maior_resultado) in str(i[2]):
        nome_ganhador = i[0]
        total_de_votos_ganhador = i[2]
        teve_empate += 1

if teve_empate > 1:
    resultado_votacao = f"🗳️    TOTAL DE VOTOS [ {total_de_votos} ]\n\n"

    for i in candidatos_resultado:
        if str(maior_resultado) in str(i[2]):
            resultado_votacao += f"| {i[0]} - {i[2]} Votos\n"

    resultado_votacao += '\nVOTAÇÃO EMPATADA!\n\n'

    candidatos_resultado = sorted(candidatos_resultado, key=lambda inner_list: inner_list[2], reverse=True)
    for i in candidatos_resultado:
        resultado_votacao += f"[ {i[1]} ] {i[0]} - {i[2]} Votos   {round(((i[2] * 100)/total_de_votos), 2)} % DOS VOTOS TOTAIS.\n"
    
    resultado_votacao += '\n'

    enviar_resultados(resultado_votacao)
    print(resultado_votacao) 
else:
    resultado_votacao = f"🗳️    TOTAL DE VOTOS [ {total_de_votos} ]\n"
    resultado_votacao += f"🏆    {nome_ganhador} GANHOU COM O TOTAL DE {total_de_votos_ganhador} VOTOS!\n\n"
    candidatos_resultado = sorted(candidatos_resultado, key=lambda inner_list: inner_list[2], reverse=True)
    for i in candidatos_resultado:
        resultado_votacao += f"[ {i[1]} ] {i[0]} - {i[2]} Votos   {round(((i[2] * 100)/total_de_votos), 2)} % DOS VOTOS TOTAIS.\n"
    
    resultado_votacao += '\n'
    enviar_resultados(resultado_votacao) 
    print(resultado_votacao)