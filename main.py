import os
from base_conhecimento import BaseConhecimento
from assistente import Assistente


if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists("data/historico.json"):
    with open("data/historico.json", "w", encoding="utf-8") as arquivo:
        arquivo.write("[]")

base = BaseConhecimento("data/base_conhecimento.json")
base.carregar()

assistente = Assistente("Citizen Assist AI", base)

if len(base.orientacoes) == 0:
    print("Não foi possível carregar a base.")

else:
    while True:
        print("\n===== CITIZEN ASSIST AI =====")
        print("1 - Fazer uma pergunta")
        print("2 - Navegar por categorias")
        print("3 - Ver indicadores")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            assistente.perguntar()

        elif opcao == "2":
            assistente.navegar()

        elif opcao == "3":
            assistente.indicadores()

        elif opcao == "0":
            assistente.nota_facilidade()
            assistente.indicadores()
            assistente.exportar_csv()

            print("\nObrigado por utilizar o Citizen Assist AI!")
            break

        else:
            print("Opção inválida.")
