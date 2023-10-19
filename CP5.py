# Importando as bibliotecas utilizadas
import datetime
import time

# Inicialização de classes
# Classe Tarefas
class Tarefa:
    def __init__(self, descricao, data_inicial, data_final, completude_real, completude_planejada, responsavel):
        self.descricao = descricao
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.completude_real = completude_real
        self.completude_planejada = completude_planejada
        self.responsavel = responsavel
        self.plano_atraso = ""

    # Faz a verificação se a tarefa cadastrada está atrasada e caso esteja pede um plano de ação para a resolução
    def verificar_atraso(self):
        if self.completude_real < self.completude_planejada:
            self.plano_atraso = input(f"Por favor, forneça um plano de ação para a tarefa '{self.descricao}': ")

    # Faz o print do resumo de todas as tarefas desenvolvidas
    def __str__(self):
        return f"{self.descricao} - {self.data_inicial} até {self.data_final} - {self.completude_real}% realizado - {self.completude_planejada}% planejado - Responsável: {self.responsavel}"

# Classe de Estoque e Pedidos
class EstoquePedidos:
    def __init__(self):
        self.estoque = {'rolhas': 50, 'garrafas': 50, 'rotulos': 50, 'caixas': 50}
        self.precos = {'garrafa': 15, 'caixa6': 80, 'caixa12': 150}
        self.pedidos_clientes = {}

    # Faz o calculo do frete a partir do pedido que foi feito
    def calcular_frete(self, total_pedido, quantidade):
        taxa_preparacao = total_pedido * 0.1
        preco_frete = (quantidade * 10.0) + taxa_preparacao + 10.0
        return preco_frete

    # Verifica se pedido não execede a quantidade de itens no estoque
    def estoque_suficiente(self, item, quantidade):
        if item == 'garrafa':
            return self.estoque['garrafas'] >= quantidade and self.estoque['rotulos'] >= quantidade and self.estoque['rolhas'] >= quantidade
        elif item == 'caixa6':
            return self.estoque['garrafas'] >= quantidade * 6 and self.estoque['rotulos'] >= quantidade * 6 and self.estoque['rolhas'] >= quantidade * 6
        elif item == 'caixa12':
            return self.estoque['garrafas'] >= quantidade * 12 and self.estoque['rotulos'] >= quantidade * 12 and self.estoque['rolhas'] >= quantidade * 12
        return False

    # Faz a adição de um novo item a partir da quantidade escolhida
    def adicionar_ao_estoque(self, item, quantidade):
        self.estoque[item] += quantidade

    # Faz o registro do pedido a partir das informações que são exigidas
    def registrar_pedido(self, nome_cliente, item, quantidade):
        if self.estoque_suficiente(item, quantidade):
            total_pedido = self.precos[item] * quantidade
            frete = self.calcular_frete(total_pedido, quantidade)
            self.pedidos_clientes[nome_cliente] = {'item': item, 'quantidade': quantidade, 'total': total_pedido, 'frete': frete}
            return total_pedido, frete
        else:
            return None, None

# Classe Principal do Sistema
class SistemaVinheria:
    def __init__(self):
        self.tarefas = []
        self.estoque_pedidos = EstoquePedidos()

    # Faz a verificação se a data corresponde ao formato exigido
    def ler_data(self, mensagem):
        while True:
            data_str = input(mensagem)
            try:
                data = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
                return data
            except ValueError:
                print("Formato de data inválido. Use DD/MM/AAAA.")

    # Faz a verificação se a porcentagem de completude está entre 0 e 100
    def ler_porcentagem(self, mensagem):
        while True:
            try:
                porcentagem = float(input(mensagem))
                if 0 <= porcentagem <= 100:
                    return porcentagem
                else:
                    print("A porcentagem deve estar entre 0 e 100.")
            except ValueError:
                print("Por favor, insira um número válido.")

    # Menu principal da aplicação
    def menu(self):
        opcao = 0
        while opcao != 7:
            print('\n----------------------------------------------')
            print('   Bem vindo ao sistema da Vinheria Agnello')
            print('----------------------------------------------')
            print('\n[ 1 ] Gerenciar Tarefas')
            print('[ 2 ] Adicionar itens ao estoque')
            print('[ 3 ] Registrar pedido')
            print('[ 4 ] Exibir resumo de pedidos e estoque')
            print('[ 5 ] Exibir resumo de tarefas')
            print('[ 6 ] Limpar console')
            print('[ 7 ] Fechar o programa')

            try:
                opcao = int(input('\nDigite qual a opção desejada: '))
                if opcao == 1:
                    self.gerenciar_tarefas()
                elif opcao == 2:
                    self.adicionar_itens_estoque()
                elif opcao == 3:
                    self.registrar_pedido_cliente()
                elif opcao == 4:
                    self.exibir_resumo_pedidos_estoque()
                    time.sleep(5)
                elif opcao == 5:
                    self.exibir_resumo_tarefas()
                    time.sleep(5)
                elif opcao == 6:
                    self.limpar_console()
                elif opcao == 7:
                    print('\nEncerrando o programa.')
                else:
                    print('\nOpção inválida. Por favor, escolha uma opção válida.')
            except ValueError:
                print("\nEntrada inválida. Por favor, digite um número válido para a opção.")

    # Pega os inputs de tarefa comprime em uma variável e faz a adição na lista de tarefas
    def gerenciar_tarefas(self):
        descricao = input("Descrição da tarefa: ")
        data_inicial = self.ler_data("Data inicial (DD/MM/AAAA): ")
        data_final = self.ler_data("Data final (DD/MM/AAAA): ")
        completude_real = self.ler_porcentagem("Completude real (%): ")
        completude_planejada = self.ler_porcentagem("Completude planejada (%): ")
        responsavel = input("Responsável pela tarefa: ")

        tarefa = Tarefa(descricao, data_inicial, data_final, completude_real, completude_planejada, responsavel)
        tarefa.verificar_atraso()
        self.tarefas.append(tarefa)
        print("Tarefa adicionada com sucesso!")

    # Faz a adição do item e da quantidade do item no estoque
    def adicionar_itens_estoque(self):
        while True:
            item = input('\nDigite o item do pedido (rolhas, garrafas, rotulos, caixas) ou "sair" para encerrar: ').lower()
            if item == 'sair':
                break

            if item in self.estoque_pedidos.estoque.keys():
                quantidade = int(input('Digite a quantidade: '))
                self.estoque_pedidos.adicionar_ao_estoque(item, quantidade)
                print('Produto adicionado com sucesso!')
            else:
                print('Digite um item válido!!')

    # Pede as informações necessárias para o registro de um novo pedido e adiciona na lista de pedidos
    def registrar_pedido_cliente(self):
        nome_cliente = input("\nNome do cliente: ")
        item = input("Digite o item do pedido (garrafa, caixa6, caixa12): ").lower()
        quantidade = int(input("Digite a quantidade: "))

        total_pedido, frete = self.estoque_pedidos.registrar_pedido(nome_cliente, item, quantidade)
        if total_pedido is not None:
            print(f"\nTotal do pedido: {total_pedido}\nValor do frete: {frete}\nTotal a pagar: {total_pedido + frete}")
        else:
            print("\nDesculpe, não temos estoque suficiente para este pedido.")

    # Faz a exibição do do estoque e de todos os pedidos registrados no sistema
    def exibir_resumo_pedidos_estoque(self):
        print("\nEstoque atual:")
        for chave, valor in self.estoque_pedidos.estoque.items():
            print(f"{chave.capitalize()}: {valor}")

        print("\nHistórico de pedidos:")
        for cliente, pedido in self.estoque_pedidos.pedidos_clientes.items():
            print(f"Cliente: {cliente}, Item: {pedido['item'].capitalize()}, Quantidade: {pedido['quantidade']}, Total: {pedido['total']}, Frete: {pedido['frete']}")

    # Faz a exibição de todas as tarefas registradas no sistema
    def exibir_resumo_tarefas(self):
        print("\nTarefas: ")
        for t in self.tarefas:
            print(t)
            if t.plano_atraso:
                print(f"Plano de Ação: {t.plano_atraso}")

    # Limpa o console para uma melhor vizualização do usuário
    def limpar_console(self):
        for _ in range(50):
            print()

# Inicia a aplicação
if __name__ == "__main__":
    sistema = SistemaVinheria()
    sistema.menu()
