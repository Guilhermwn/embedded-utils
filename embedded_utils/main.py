
# ====================================================
# IMPORTAÇÕES
# ====================================================
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import time
import typer
from tabulate import tabulate
from typing import Optional
from typing_extensions import Annotated
from rich.progress import Progress, SpinnerColumn, TextColumn

from __init__ import __version__
from microcontroladores import mcus
from functions import serial_ports
from functions import ensure_folder_name
from functions import criar_pasta
from functions import MCU_autocompletion_helper

# ====================================================
# CONSTANTES
# ====================================================

microcontroladores = mcus

# ====================================================
# DECLARAÇÃO DO APP CLI
# ====================================================

app = typer.Typer()


# ====================================================
# COMANDOS CLI
# ====================================================

def version_callback(value: bool):
    if value:
        typer.echo(f"Embedded Utils Version: {__version__}")
        raise typer.Exit()
    
@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    pass

# ====================================================
# COMANDO CLI "INFORMATIONS"
@app.command()
def informations():
     typer.clear()
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