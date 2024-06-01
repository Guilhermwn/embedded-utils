# ====================================================
# IMPORTAÇÕES
# ====================================================
import os # Impora o módulo os
import sys  # Importa o módulo sys para acessar informações do sistema operacional
import glob  # Importa o módulo glob para buscar arquivos/padrões de nome de arquivo
import typer #  Importta o módulo typer
import serial  # Importa o módulo serial para comunicação serial
from pathlib import Path
from tabulate import tabulate
from typing_extensions import Annotated
from rich.progress import Progress, SpinnerColumn, TextColumn

from microcontroladores import mcus

# ====================================================
# FUNÇÕES UTILITÁRIAS
# ====================================================

# ====================================================
# DETECTOR DE PORTAS CONECTADAS
def serial_ports():
    """ Lista o nome das portas atualmente conectadas

    :raises EnvironmentError:
        Sistema operacional ou plataforma não suportada
    :returns:
        Uma lista com as portas seriais atualmente conectadas
    """
    if sys.platform.startswith('win'):  # Verifica se o sistema operacional é Windows
        ports = ['COM%s' % (i + 1) for i in range(256)]  # Lista de portas COM no Windows
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):  # Verifica se o sistema operacional é Linux ou Cygwin
        # Lista todas as portas seriais no sistema Linux ou Cygwin, excluindo o terminal atual
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):  # Verifica se o sistema operacional é macOS
        # Lista todas as portas seriais no sistema macOS
        ports = glob.glob('/dev/tty.*')
    else:  # Se o sistema operacional não for suportado, levanta um erro
        raise EnvironmentError('Unsupported platform')

    result = []  # Inicializa uma lista para armazenar as portas seriais disponíveis
    for port in ports:  # Itera sobre todas as portas seriais encontradas
        try:  # Tenta abrir a porta serial
            s = serial.Serial(port)
            s.close()  # Fecha a porta serial
            result.append(port)  # Adiciona a porta à lista de portas disponíveis se abrir e fechar com sucesso
        except (OSError, serial.SerialException):  # Captura exceções que podem ocorrer ao abrir a porta serial
            pass  # Não faz nada se ocorrer uma exceção e continua para a próxima porta
    if result == []:
        return False
    else:
        return result  # Retorna a lista de portas seriais disponíveis
    
# ====================================================
# ANALISADOR DE NOME DE PASTA
# DECLARAÇÃO DE FUNÇÃO QUE ANALISA CARACTERES QUE NÃO PODEM SER USADOS NA CRIAÇÃO DE UMA PASTA 
def ensure_folder_name(palavra):
    """
    Verifica se uma palavra contém caracteres proibidos para nomes de pastas.

    Esta função recebe uma string `palavra` e verifica se ela contém algum dos
    caracteres que são proibidos em nomes de pastas no sistema de arquivos. Os
    caracteres proibidos são: '\\', '/', '*', ':', '?', '<', '>', '|', e '.'.
    Se algum desses caracteres estiver presente na string, a função retorna 
    `True`, indicando que a palavra contém caracteres proibidos. Caso contrário, 
    retorna `False`.

    Parameters:
    palavra (str): A string que representa o nome da pasta a ser verificado.

    Returns:
    bool: `True` se a palavra contiver caracteres proibidos, caso contrário `False`.
    """
    folder_forbidden = ['\\', '/', '*', ':', '?', '<', '>', '|', '.']
    return any(caracter in palavra for caracter in folder_forbidden)

# ====================================================
# LISTA COM NOMES DISPONÍVEIS DE MICROCONTROLADORES
# FUNÇÃO ABRE E ADICIONA EM UMA LISTA OS NOMES DOS MCU
def microcontroladores_disponiveis(microcontroladores):
    try:
        with open(microcontroladores, 'r') as file:
            linhas = file.readlines()
            mcus = [linha.split(",") for linha in linhas]
        return mcus[0]
    except FileNotFoundError:
        typer.secho(f"Arquivo {microcontroladores} não encontrado",
                    fg="red")
    except Exception as e:
        typer.secho(f"Ocorreu um erro {e}", fg="red")

    # for value in microcontroladores_disponiveis(microcontroladores):
# ====================================================
# ASSISTENTE DE AUTO-COMPLETION DO TERMINAL
def MCU_autocompletion_helper(incomplete: str):
    # microcontroladores 
    completion = []
    for value in mcus:
        if value.startswith(incomplete):
            completion.append(value)
    return completion


# ====================================================
# FUNÇÃO QUE CRIA A PASTA COM BASE NO INPUT DO USUÁRIO
def criar_pasta(nome):
    try:
        # verifica se o nome da pasta já existe no diretório
        if not os.path.exists(nome):
            os.makedirs(nome)
            typer.secho("Pasta criada com sucesso!", fg="green")
        else:
            typer.secho(f"Pasta {nome} já existe", fg="red")
    except Exception as e:
        typer.secho(f"Erro ao criar a pasta:\n{e}", fg="red")
