import os
import maceio_data
import coruripe_data
import piranhas_data

#fluxo: acessar->selecionar municipio (maceio, coruripe ou piranhas)->escolher gráfico (precipitações ou temperatura)->podendo voltar ou encerrar o programa.
while True:
    print("\nSelecione o município:")
    print("1 - Maceió")
    print("2 - Coruripe")
    print("3 - Piranhas")
    print("0 - Sair")
    
    try:
        municipio = int(input("Digite o número do município: "))
        os.system('cls')
    except ValueError:
        print("Opção inválida! Digite um número válido.")
        continue

    if municipio == 0:
        print("Encerrando o programa...")
        break

    if municipio == 1:
        caminho_arquivo = os.path.join("C:\\", "Users", "Emmanuel", "Desktop", "SI - CESMAC", "QUARTO_PERIODO", "proj_mat_computacional", "dados", "dados_A303_D_2025-01-01_2025-02-24.csv")
        modulo = maceio_data
    elif municipio == 2:
        caminho_arquivo = os.path.join("C:\\", "Users", "Emmanuel", "Desktop", "SI - CESMAC", "QUARTO_PERIODO", "proj_mat_computacional", "dados", "dados_A355_D_2025-01-01_2025-02-24.csv")
        modulo = coruripe_data
    elif municipio == 3:
        caminho_arquivo = os.path.join("C:\\", "Users", "Emmanuel", "Desktop", "SI - CESMAC", "QUARTO_PERIODO", "proj_mat_computacional", "dados", "dados_A371_D_2025-01-01_2025-02-24.csv")
        modulo = piranhas_data
    else:
        print("Opção inválida! Escolha um município válido.")
        continue

    dados = modulo.carrega_dados(caminho_arquivo)
    estatisticas_temp = modulo.calcula_infos(dados)
    estatisticas_precipitacao = modulo.calcular_estatisticas_precipitacao(dados)

    while True:
        print("\nSelecione o gráfico:")
        print("1 - Temperaturas Máxima e Mínima")
        print("2 - Precipitação Total Diária")
        print("0 - Voltar ao menu principal")

        try:
            grafico = int(input("Digite a opção: "))
        except ValueError:
            print("Opção inválida! Digite um número válido.")
            continue

        if grafico == 1:
            modulo.gera_grafico_temperaturas(dados, estatisticas_temp)
            os.system('cls')
        elif grafico == 2:
            modulo.gerar_grafico_precipitacao(dados, estatisticas_precipitacao)
            os.system('cls')
        elif grafico == 0:
            os.system('cls')
            break
        else:
            print("Opção inválida! Escolha um gráfico válido.")
