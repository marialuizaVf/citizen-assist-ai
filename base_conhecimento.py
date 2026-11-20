import json

ACENTOS = {
    "á": "a", "à": "a", "ã": "a", "â": "a",
    "é": "e", "ê": "e", "í": "i",
    "ó": "o", "õ": "o", "ô": "o",
    "ú": "u", "ç": "c"
}


def normalizar(texto):
    texto = texto.lower().strip()

    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)

    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")

    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        from orientacao import Orientacao

        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.orientacoes = []

            for item in dados:
                orientacao = Orientacao(item)
                self.orientacoes.append(orientacao)

        except (FileNotFoundError, json.JSONDecodeError):
            print("Erro ao carregar a base de conhecimento.")
            self.orientacoes = []

    def categorias(self):
        lista = []

        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)

        return lista

    def por_categoria(self, categoria):
        lista = []

        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                lista.append(orientacao)

        return lista

    def pontuar(self, pergunta, orientacao):
        pergunta = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)

        pontos = 0

        for palavra_chave in orientacao.palavras_chave:
            palavra = normalizar(palavra_chave)

            if palavra in pergunta:
                pontos += 3

        palavras = pergunta.split()

        for palavra in palavras:
            if len(palavra) >= 4 and palavra in titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []

        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)

            if pontos > 0:
                resultados.append((pontos, orientacao))

        for i in range(len(resultados)):
            for j in range(i + 1, len(resultados)):
                if resultados[i][0] < resultados[j][0]:
                    troca = resultados[i]
                    resultados[i] = resultados[j]
                    resultados[j] = troca

        return resultados
