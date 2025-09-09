# -*- coding: utf-8 -*-

class No:
    """
    Representa um nó na Árvore AVL.
    Cada nó armazena uma chave, referências para os filhos e sua altura.
    """
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1 # A altura de um novo nó (folha) é sempre 1

class ArvoreAVL:
    """
    Implementa a estrutura e as operações de uma Árvore AVL.
    """
    def __init__(self):
        self.raiz = None

    # ===============================================================
    # TAREFA 0: IMPLEMENTAR MÉTODOS AUXILIARES E ROTAÇÕES
    # ===============================================================

    def obter_altura(self, no):
        if no is None:
            return 0
        return no.altura

    def obter_fator_balanceamento(self, no):
        if no is None:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self.obter_altura(no.esquerda), self.obter_altura(no.direita))

    def obter_no_valor_minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _rotacao_direita(self, no_pivo):
        novo_pivo = no_pivo.esquerda
        no_pivo.esquerda = novo_pivo.direita
        novo_pivo.direita = no_pivo
        self._atualizar_altura(no_pivo)
        self._atualizar_altura(novo_pivo)
        return novo_pivo

    def _rotacao_esquerda(self, no_pivo):
        novo_pivo = no_pivo.direita
        no_pivo.direita = novo_pivo.esquerda
        novo_pivo.esquerda = no_pivo
        self._atualizar_altura(no_pivo)
        self._atualizar_altura(novo_pivo)
        return novo_pivo

    # ===============================================================
    # TAREFA 1: IMPLEMENTAR INSERÇÃO E DELEÇÃO COM BALANCEAMENTO
    # ===============================================================

    def inserir(self, chave):
        self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
        if no_atual is None:
            return No(chave)
        if chave < no_atual.chave:
            no_atual.esquerda = self._inserir_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._inserir_recursivo(no_atual.direita, chave)
        else:
            raise Exception("Chave duplicada não permitida na AVL.")

        self._atualizar_altura(no_atual)
        fator = self.obter_fator_balanceamento(no_atual)

        # Caso 1: Esquerda-Esquerda
        if fator > 1 and chave < no_atual.esquerda.chave:
            return self._rotacao_direita(no_atual)
        # Caso 2: Direita-Direita
        if fator < -1 and chave > no_atual.direita.chave:
            return self._rotacao_esquerda(no_atual)
        # Caso 3: Esquerda-Direita
        if fator > 1 and chave > no_atual.esquerda.chave:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)
        # Caso 4: Direita-Esquerda
        if fator < -1 and chave < no_atual.direita.chave:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    def deletar(self, chave):
        self.raiz = self._deletar_recursivo(self.raiz, chave)

    def _deletar_recursivo(self, no_atual, chave):
        if no_atual is None:
            return no_atual
        if chave < no_atual.chave:
            no_atual.esquerda = self._deletar_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._deletar_recursivo(no_atual.direita, chave)
        else:
            # Nó encontrado
            if no_atual.esquerda is None:
                return no_atual.direita
            elif no_atual.direita is None:
                return no_atual.esquerda
            else:
                sucessor = self.obter_no_valor_minimo(no_atual.direita)
                no_atual.chave = sucessor.chave
                no_atual.direita = self._deletar_recursivo(no_atual.direita, sucessor.chave)

        if no_atual is None:
            return no_atual

        self._atualizar_altura(no_atual)
        fator = self.obter_fator_balanceamento(no_atual)

        # Caso 1: Esquerda-Esquerda
        if fator > 1 and self.obter_fator_balanceamento(no_atual.esquerda) >= 0:
            return self._rotacao_direita(no_atual)
        # Caso 2: Esquerda-Direita
        if fator > 1 and self.obter_fator_balanceamento(no_atual.esquerda) < 0:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)
        # Caso 3: Direita-Direita
        if fator < -1 and self.obter_fator_balanceamento(no_atual.direita) <= 0:
            return self._rotacao_esquerda(no_atual)
        # Caso 4: Direita-Esquerda
        if fator < -1 and self.obter_fator_balanceamento(no_atual.direita) > 0:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    # ===============================================================
    # TAREFA 2 E 3: IMPLEMENTAR BUSCAS
    # ===============================================================

    def encontrar_nos_intervalo(self, chave1, chave2):
        resultado = []
        self._encontrar_nos_intervalo_rec(self.raiz, chave1, chave2, resultado)
        return resultado

    def _encontrar_nos_intervalo_rec(self, no, chave1, chave2, resultado):
        if no is None:
            return
        if chave1 < no.chave:
            self._encontrar_nos_intervalo_rec(no.esquerda, chave1, chave2, resultado)
        if chave1 <= no.chave <= chave2:
            resultado.append(no.chave)
        if chave2 > no.chave:
            self._encontrar_nos_intervalo_rec(no.direita, chave1, chave2, resultado)

    def obter_profundidade_no(self, chave):
        return self._obter_profundidade_no_rec(self.raiz, chave, 0)

    def _obter_profundidade_no_rec(self, no, chave, profundidade):
        if no is None:
            return -1
        if chave == no.chave:
            return profundidade
        elif chave < no.chave:
            return self._obter_profundidade_no_rec(no.esquerda, chave, profundidade + 1)
        else:
            return self._obter_profundidade_no_rec(no.direita, chave, profundidade + 1)

    # Método auxiliar para percorrer em ordem (para depuração)
    def percurso_em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no is not None:
            self._em_ordem(no.esquerda, resultado)
            resultado.append(no.chave)
            self._em_ordem(no.direita, resultado)

# --- Bloco de Teste e Demonstração da Atividade AVL ---
if __name__ == "__main__":
    arvore_avl = ArvoreAVL()

    print("\n--- ATIVIDADE PRÁTICA: ÁRVORE AVL ---")

    print("\n--- 1. Inserindo nós ---")
    chaves_para_inserir = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for chave in chaves_para_inserir:
            arvore_avl.inserir(chave)
        print("Inserção concluída (sem erros).")
        print("Percurso em ordem:", arvore_avl.percurso_em_ordem())
    except Exception as e:
        print(f"\nERRO DURANTE A INSERÇÃO: {e}")

    print("\n--- 2. Deletando nós ---")
    try:
        chaves_para_deletar = [10, 11]
        for chave in chaves_para_deletar:
            arvore_avl.deletar(chave)
        print("Deleção concluída (sem erros).")
        print("Percurso em ordem após deleção:", arvore_avl.percurso_em_ordem())
    except Exception as e:
        print(f"\nERRO DURANTE A DELEÇÃO: {e}")

    print("\n--- 3. Buscando nós no intervalo [1, 9] ---")
    try:
        nos_no_intervalo = arvore_avl.encontrar_nos_intervalo(1, 9)
        if nos_no_intervalo is not None:
            print(f"Nós encontrados: {sorted(nos_no_intervalo)}")
        else:
            print("Método `encontrar_nos_intervalo` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE A BUSCA POR INTERVALO: {e}")

    print("\n--- 4. Calculando profundidade do nó 6 ---")
    try:
        profundidade = arvore_avl.obter_profundidade_no(6)
        if profundidade is not None:
            if profundidade != -1:
                print(f"O nó 6 está no nível/profundidade: {profundidade}")
            else:
                print("O nó 6 não foi encontrado.")
        else:
            print("Método `obter_profundidade_no` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE O CÁLCULO DE PROFUNDIDADE: {e}")

