import json
import csv
import time


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.facilidade = []

    def perguntar(self):
        pergunta = input("\nDigite sua dúvida (0 para voltar): ")

        if pergunta == "0":
            return

        quantidade_digitos = 0

        for caractere in pergunta:
            if caractere.isdigit():
                quantidade_digitos += 1

        if "@" in pergunta or quantidade_digitos >= 8:
            print("Não digite CPF, telefone ou e-mail.")
            print("Reescreva sua pergunta.")
            return

        inicio = time.time()
        resultados = self.base.buscar(pergunta)
        tempo = round(time.time() - inicio, 1)

        encontrou = False
        id_orientacao = None

        if resultados and resultados[0][0] >= 3:
            pontos = resultados[0][0]
            orientacao = resultados[0][1]

            if pontos >= 6:
                confianca = "ALTA"
            else:
                confianca = "MEDIA"

            print("\nConfiança:", confianca, "-", pontos, "pontos")
            orientacao.exibir()

            encontrou = True
            id_orientacao = orientacao.id

            contador = 0

            print("\nOutras orientações:")

            for resultado in resultados:
                if resultado[1].id != orientacao.id and contador < 2:
                    print("-", resultado[1].titulo)
                    contador += 1

        else:
            print("\nNão encontrei uma orientação.")
            print("Tente outras palavras ou navegue pelas categorias.")

        ajudou = self.perguntar_sim_nao(
            "\nEssa orientação respondeu sua dúvida? (s/n): "
        )

        registro = {
            "data": time.time(),
            "origem": "pergunta",
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": 1,
            "tempo": tempo
        }

        self.registrar(registro)

    def navegar(self):
        categorias = self.base.categorias()

        while True:
            print("\n--- CATEGORIAS ---")

            for i in range(len(categorias)):
                print(i + 1, "-", categorias[i])

            print("0 - Voltar")

            escolha = input("Escolha uma categoria: ")

            if escolha == "0":
                return

            if not escolha.isdigit():
                print("Digite um número.")
                continue

            escolha = int(escolha)

            if escolha < 1 or escolha > len(categorias):
                print("Opção inválida.")
                continue

            categoria = categorias[escolha - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print("\n---", categoria, "---")

                for i in range(len(orientacoes)):
                    print(i + 1, "-", orientacoes[i].titulo)

                print("0 - Voltar")

                escolha_orientacao = input("Escolha uma orientação: ")

                if escolha_orientacao == "0":
                    break

                if not escolha_orientacao.isdigit():
                    print("Digite um número.")
                    continue

                escolha_orientacao = int(escolha_orientacao)

                if escolha_orientacao < 1 or escolha_orientacao > len(orientacoes):
                    print("Opção inválida.")
                    continue

                orientacao = orientacoes[escolha_orientacao - 1]

                inicio = time.time()
                orientacao.exibir()
                tempo = round(time.time() - inicio, 1)

                ajudou = self.perguntar_sim_nao(
                    "\nEssa orientação respondeu sua dúvida? (s/n): "
                )

                registro = {
                    "data": time.time(),
                    "origem": "categoria",
                    "pergunta": orientacao.titulo,
                    "id_orientacao": orientacao.id,
                    "encontrou": True,
                    "ajudou": ajudou,
                    "tentativas": 1,
                    "tempo": tempo
                }

                self.registrar(registro)

    def perguntar_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).lower()

            if resposta == "s":
                return True

            elif resposta == "n":
                return False

            else:
                print("Digite s ou n.")

    def registrar(self, registro):
        self.historico.append(registro)

        try:
            with open("data/historico.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

        except (FileNotFoundError, json.JSONDecodeError):
            dados = []

        dados.append(registro)

        with open("data/historico.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def indicadores(self):
        try:
            with open("data/historico.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

        except (FileNotFoundError, json.JSONDecodeError):
            dados = []

        total = len(dados)

        if total == 0:
            print("Não existem atendimentos.")
            return

        encontrados = 0
        ajudaram = 0
        tempo_total = 0
        tentativas_total = 0
        sem_solucao = []

        for registro in dados:
            if registro["encontrou"]:
                encontrados += 1

            if registro["ajudou"]:
                ajudaram += 1
            else:
                sem_solucao.append(registro["pergunta"])

            tempo_total += registro["tempo"]
            tentativas_total += registro["tentativas"]

        print("\n--- INDICADORES ---")
        print("Total:", total)

        print("Respostas encontradas:",
              round(encontrados / total * 100, 1), "%")

        print("Taxa de acerto:",
              round(ajudaram / total * 100, 1), "%")

        print("Tempo médio:",
              round(tempo_total / total, 1), "segundos")

        print("Tentativas por atendimento:",
              round(tentativas_total / total, 1))

        print("\nDúvidas sem solução:")

        if len(sem_solucao) == 0:
            print("Nenhuma.")
        else:
            for pergunta in sem_solucao:
                print("-", pergunta)

        if len(self.facilidade) > 0:
            media = sum(self.facilidade) / len(self.facilidade)
            print("Facilidade:", round(media, 1), "de 5")

    def exportar_csv(self):
        try:
            with open("data/historico.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

        except (FileNotFoundError, json.JSONDecodeError):
            dados = []

        campos = [
            "data", "origem", "pergunta", "id_orientacao",
            "encontrou", "ajudou", "tentativas", "tempo"
        ]

        with open("data/atendimentos.csv", "w",
                  newline="", encoding="utf-8") as arquivo:

            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(dados)

        print("CSV exportado.")

    def nota_facilidade(self):
        while True:
            nota = input("Avalie a facilidade de 1 a 5: ")

            if nota.isdigit():
                nota = int(nota)

                if nota >= 1 and nota <= 5:
                    self.facilidade.append(nota)
                    return

            print("Digite uma nota de 1 a 5.")
