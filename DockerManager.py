#!/usr/bin/env python3
import docker
import os
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("### JARVIS: GERENCIADOR DE CONTÊINERES DOCKER ###")
    print("---------------------------------------------------")

def show_running_containers(client):
    print("Status Atual: Contêineres Ativos")
    try:
        running_containers = client.containers.list(filters={"status": "running"})
        if not running_containers:
            print("Nenhum contêiner ativo no momento.")
        else:
            print(f'{"Nº":<4}{"NOME":<30}{"IMAGEM":<45}{"STATUS":<20}')
            for i, c in enumerate(running_containers):
                image_tag = c.image.tags[0] if c.image.tags else 'N/A'
                print(f'[{i+1:<2}] {c.name:<30} {image_tag:<45} {c.status:<20}')
        return running_containers
    except docker.errors.DockerException as e:
        print(f"\nERRO: Não foi possível conectar ao serviço Docker. Ele está em execução?")
        print(f"Detalhe: {e}")
        sys.exit(1)


def start_container(client):
    print_header()
    print("--- INICIAR CONTÊINER ---")
    stopped_containers = client.containers.list(all=True, filters={"status": "exited"})
    if not stopped_containers:
        print("Nenhum contêiner parado para iniciar.")
        time.sleep(2)
        return

    print("Selecione o contêiner para INICIAR:")
    for i, c in enumerate(stopped_containers):
        print(f"  [{i+1}] {c.name}")
    print("  [0] Cancelar")

    try:
        choice = int(input("\nSua escolha: "))
        if 0 < choice <= len(stopped_containers):
            container_to_start = stopped_containers[choice-1]
            print(f"\nIniciando '{container_to_start.name}'...")
            container_to_start.start()
            print("Comando de início enviado com sucesso.")
            time.sleep(2)
        elif choice == 0:
            print("Operação cancelada.")
            time.sleep(1)
        else:
            print("Escolha inválida.")
            time.sleep(1)
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        time.sleep(2)


def stop_container(client, running_containers):
    print_header()
    print("--- PARAR CONTÊINER ---")
    if not running_containers:
        print("Nenhum contêiner ativo para parar.")
        time.sleep(2)
        return

    print("Selecione o contêiner para PARAR:")
    for i, c in enumerate(running_containers):
        print(f"  [{i+1}] {c.name}")
    print("  [0] Cancelar")

    try:
        choice = int(input("\nSua escolha: "))
        if 0 < choice <= len(running_containers):
            container_to_stop = running_containers[choice-1]
            print(f"\nParando '{container_to_stop.name}'... (Aguarde até 10s)")
            container_to_stop.stop()
            print("Contêiner parado com sucesso.")
            time.sleep(2)
        elif choice == 0:
            print("Operação cancelada.")
            time.sleep(1)
        else:
            print("Escolha inválida.")
            time.sleep(1)
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        time.sleep(2)

def list_images(client):
    print_header()
    print("--- IMAGENS DOCKER LOCAIS ---")
    images = client.images.list()
    if not images:
        print("Nenhuma imagem Docker encontrada.")
    else:
        print(f'{"REPOSITÓRIO":<40}{"TAG":<20}{"TAMANHO":<15}')
        for img in images:
            if not img.tags: continue
            size_mb = f"{img.attrs['Size'] / (1024*1024):.2f} MB"
            print(f"{img.tags[0].split(':')[0]:<40}{img.tags[0].split(':')[-1]:<20}{size_mb:<15}")

    input("\nPressione Enter para retornar ao menu...")


def main():
    try:
        client = docker.from_env()
    except docker.errors.DockerException as e:
        print("ERRO CRÍTICO: Não foi possível conectar ao serviço Docker. Ele está em execução?")
        sys.exit(1)

    while True:
        print_header()
        running_containers = show_running_containers(client)
        print("\n--- MENU DE OPÇÕES ---")
        print("[1] Iniciar um contêiner parado")
        print("[2] Parar um contêiner ativo")
        print("[3] Listar todas as imagens locais")
        print("[4] Sair")

        choice = input("\nDigite sua escolha: ")

        if choice == '1':
            start_container(client)
        elif choice == '2':
            stop_container(client, running_containers)
        elif choice == '3':
            list_images(client)
        elif choice == '4':
            print("Encerrando gerenciador...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)

if __name__ == "__main__":
    main()
