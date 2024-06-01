# ====================================================
# IMPORTAÇÕES
# ====================================================
import os # Impora o módulo os
import sys  # Importa o módulo sys para acessar informações do sistema operacional
import time
import glob  # Importa o módulo glob para buscar arquivos/padrões de nome de arquivo
import typer #  Importta o módulo typer
import serial  # Importa o módulo serial para comunicação serial
from pathlib import Path
from tabulate import tabulate
from typing_extensions import Annotated
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from microcontroladores import mcus

# ====================================================
# CONSTANTES
# ====================================================

# microcontroladores = "microcontroladores.txt"
microcontroladores = mcus

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
    microcontroladores 
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

# ====================================================
# FUNÇÕES UTILITÁRIAS
# ====================================================


# ====================================================
# DECLARAÇÃO DO APP CLI
# ====================================================

app = typer.Typer()


# ====================================================
# COMANDOS CLI
# ====================================================

# ====================================================
# COMANDO CLI "INFORMATIONS"
@app.command()
def informations():
     os.system("cls")
     message = "Seja bem vindo ao programa "+ typer.style("Embedded Utils", fg=typer.colors.RED, bold=True) + " by " + typer.style("Guilhermwn", fg=typer.colors.GREEN, bold=True) 
     typer.echo(message)

# ====================================================
# COMANDO CLI "SHOWPORTS"
@app.command()
def showports(show_ports:bool = True):
        typer.clear()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,) as progress:
            progress.add_task(description="Procurando por portas...", total=None)
            ports = serial_ports() 
        
        if ports == False:
             print("Portas não encontradas")
        else:
            print("Portas encontradas:")
            time.sleep(0.5)
            dados = [(i, porta) for i, porta in enumerate(ports)]
            tabela = tabulate(dados, 
                              headers=["Index", "Porta"], 
                              tablefmt="pretty")
            print(tabela)

# ====================================================
# COMANDO CLI "MIKROC-SETUP"
proj_name_text = "Nome do projeto no MikroC"
@app.command()
def mikroc_setup(project_name: Annotated[str,typer.Option(help=proj_name_text)]):
    # LIMPA  O TERMINAL
    typer.clear()

    # NOME DO MCU
    mcu_name = typer.prompt("Insira o nome do Microcontrolador usado no projeto").upper()

    # DETECTA CASO O NOME DO PROJETO SEJA UM NOME INADEQUADO
    while ensure_folder_name(project_name):
        typer.secho(f"O nome [ {project_name} ] não pode conter nenhum dos caracteres a seguir: \n[ \\ ,/ ,* ,: ,? ,< ,> ,| ] \nEscolha outro nome:", 
                    fg='red',
                    bold=True)
        project_name = typer.prompt("Insira um nome válido para o projeto")
    
    # DETECTA CASO O NOME DO MCU INSERIDO NÃO EXISTE NA LISTA DO MIKROC
    while mcu_name not in microcontroladores:
        typer.secho(f"O microcontrolador [ {mcu_name} ] não está disponível.", 
                    fg='red',
                    bold=True)
        mcu_name = typer.prompt("Insira um nome válido de microcontrolador").upper()
    
    # CLOCK DO MCU
    clock = typer.prompt(f"Insira a frequência do {mcu_name}")

    # DETECTA CASO JÁ EXISTA UMA PASTA COM O MESMO NOME DO PROJETO ATUAL
    while os.path.exists(project_name):
        if os.path.exists(project_name):
            typer.secho(f"Uma pasta com o nome [ {project_name} ] já existe, escolha outro nome", fg="red")
        project_name = typer.prompt("Novo nome do projeto")
    
    # NOMENCLATURA DO PROJETO MCPPI
    nome_arquivo = f"{project_name}.mcppi"
    arquivo_mcppi = f"{project_name}/{nome_arquivo}"

    # NOMENCLATURA DO ARQUIVO C
    arquivo_c = f"{project_name}.c"
    arquivo_c_caminho = f"{project_name}/{arquivo_c}"
    
    criar_pasta(project_name)

    # CRIAÇÃO DO ARQUIVO MCPPI 
    with open(arquivo_mcppi, 'w') as arquivo:
        arquivo.write(f"""[DEVICE]
Name={mcu_name}
Clock={clock}
[FILES]
File0={arquivo_c}
Count=1
[BINARIES]
Count=0
[IMAGES]
Count=0
ActiveImageIndex=-1
[OPENED_FILES]
File0={arquivo_c}
Count=1
[EEPROM]
Count=0
[ACTIVE_COMMENTS_FILES]
Count=0
[OTHER_FILES]
Count=0
[SEARCH_PATH]
Count=0
[HEADER_PATH]
Count=0
[HEADERS]
Count=0
[PLDS]
Count=0
[Useses]
Count=0
[MEMORY_MODEL]
Value=0
[BUILD_TYPE]
Value=0
[ACTIVE_TAB]
Value={arquivo_c}
[USE_EEPROM]
Value=0
[USE_HEAP]
Value=0
[HEAP_SIZE]
Value=0
[EEPROM_DEFINITION]
Value=
[EXPANDED_NODES]
Count=0
[LIB_EXPANDED_NODES]
Count=0""")

    # CRIAÇÃO DO ARQUIVO FIRMWARE C 
    with open(arquivo_c_caminho, "w") as arquivoc:
        arquivoc.write("""void main() {

}""")
    typer.secho("Projeto criado com sucesso!", fg="green")

# ====================================================
# COMANDO CLI "PIC-MCUS"
# FUNCIONA COMO UMA PESQUISA, INSERINDO UM NOME COMPLETO OU INCOMPLETO DE UM MCU PIC
pic_mcus_help = "O nome do MCU a ser pesquisado"
@app.command()
def pic_mcus(name:Annotated[str, typer.Option(help=pic_mcus_help)]):
    typer.clear()
    name = name.upper()
    searched_pic = typer.style(f"{name}", fg="green")
    msg = f"PIC pesquisado: {searched_pic}"
    mcu_names = MCU_autocompletion_helper(name)
    
    print(msg)
    print("Microcontroladores PIC correspondentes disponíveis: ")
    print(mcu_names)

if __name__ == '__main__':
    app()