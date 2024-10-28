from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime 
import textwrap 

class Cliente:

    def __init__(self, endereco: str) -> None:

        self.endereco: str = endereco 
        self.contas: list = []


    def realizar_transacao(self, conta: int, transacao: object) -> None:

        transacao.registrar(conta)


    def adicionar_conta(self, conta) -> None:
        
        self.contas.append(conta)
    

class PessoaFisica(Cliente):

    def __init__(self, nome: str, data_nascimento: datetime, cpf: str, endereco: str) -> None: 

        super().__init__(endereco)
        self.nome: str = nome 
        self.data_nascimento: datetime = data_nascimento 
        self.cpf: str = cpf 


class Transacao(ABC):

    @property
    @abstractproperty
    def valor(self):
        pass 


    @classmethod
    def registrar(self, conta):
        pass 


class Historico:

    def __init__(self) -> None: 

        self._transacoes: list = [] 
    

    @property 
    def transacoes(self) -> list:

        return self._transacoes 
    

    def adicionar_transacoes(self, transacao: Transacao) -> dict:

        self._transacoes.append({
            "tipo": transacao.__class__.__name__, 
            "valor": transacao.valor, 
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class Conta:

    def __init__(self:object, numero: int, cliente: object) -> None:

        self._saldo: float = 0.0
        self._numero: int = numero 
        self._agencia: str = '0001'
        self._cliente: Cliente = cliente 
        self._historico: Historico = Historico()
    

    @classmethod
    def nova_conta(cls: object, cliente: Cliente, numero) -> object:
        
        return cls(numero, cliente)
    

    @property
    def saldo(self) -> float:

        return self._saldo
    

    @property 
    def numero(self) -> int:

        return self._numero 
    

    @property 
    def agencia(self) -> str:

        return self._agencia
    

    @property 
    def cliente(self) -> Cliente:
        
        return self._cliente 
    

    @property
    def historico(self) -> Historico:

        return self._historico 
    

    def sacar(self, valor: float) -> bool: 

        saldo = self.saldo 
        excedeu_saldo = valor > saldo 

        if excedeu_saldo:

            print("\n@@@ Operação falhou! Você não tem saldo suficiente.@@@")

        elif valor > 0:

            self._saldo -= valor 
            print("\n=== Saque realizado com sucesso! ===")
            return True 
        
        else:

            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False 
    

    def depositar(self, valor: float) -> bool: 

        if valor > 0: 

            self._saldo += valor 
            print("\n=== Depósito realizado com sucesso! ===")

        else:

            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False 
        
        return True 
    

class ContaCorrente(Conta):
    
    def __init__(self, numero: int, cliente: Cliente, limite: float=500, limite_saques: int=3) -> None:

        super().__init__(numero, cliente)
        self.limite: float = limite 
        self.limite_saques: int = limite_saques
    

    def sacar(self, valor: float) -> bool:

        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        excedeu_limite = valor > self.limite 
        excedeu_saques = numero_saques >= self.limite_saques 

        if excedeu_limite:

            print('\n@@@ Operação falhou! O valor do saque excede o limite. @@@')

        elif excedeu_saques:

            print('\n@@@ Operação falhou! Número máximo de saques excedido. @@@')
        
        else:

            return super().sacar(valor)
        
        return False 
    

    def __str__(self) -> None:

        return f""" \
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Saque(Transacao):
    
    def __init__(self, valor: float) -> None:
        self._valor: float = valor 

    
    @property
    def valor(self):

        return self._valor
    

    def registrar(self, conta: Conta): 

        sucesso_transacao: bool = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacoes(self)


class Deposito(Transacao):

    def __init__(self, valor: float):

        self._valor: float = valor 
    

    @property
    def valor(self):

        return self._valor 
    
    def registrar(self, conta: Conta):

        sucesso_transacao: bool = conta.depositar(self.valor)

        if sucesso_transacao: 

            conta.historico.adicionar_transacoes(self)


def menu():
    
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair

    Banco Virtual

    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf: str, clientes: list):
    
    clientes_filtrados: list = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None 


def recuperar_conta_cliente(cliente: Cliente):
    
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return 
    
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def sacar(clientes: list):

    cpf: str = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return 
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)

    if not conta: 
        return 

    cliente.realizar_transacao(conta, transacao)


def depositar(clientes: list):

    cpf = input('Informe o CPF do cliente: ')
    cliente: Cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return 
    
    valor = float(input('Informe o valor do depósito: '))
    transacao: Deposito = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta: 
        return 
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes: list):

    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if  not cliente:

        print('\n@@@ Cliente não encontrado! @@@')
        return 

    conta: Conta = recuperar_conta_cliente(cliente)
    
    if not conta:
        return
    
    print('\n=================== EXTRATO ===================')
    transacoes = conta.historico.transacoes 
    extrato = ''
    
    if not transacoes:
        extrato = 'Não foram realizadas movimentações.'
    
    else:

        for transacao in transacoes:
            extrato += f'\n{transacao["tipo"]}:\n\tR${transacao["valor"]:.2f}'
        
        print(extrato)
        print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
        print('\n===============================================')


def criar_conta(numero_conta: int, clientes: list, contas: list):
    
    cpf = input('Informe o CPF do cliente: ')
    cliente: Cliente | None = filtrar_cliente(cpf, clientes)

    if not cliente: 

        print('\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@')
        return 
    
    conta: Conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n=== Conta criada com sucesso! ===')


def listar_contas(contas):

    for conta in contas:
        print('=' * 100)
        print(textwrap.dedent(str(conta))) # Interessante a função de casting (conversora) str(conta), 
        # ela força a classe a passar seu atributo __str__.


def criar_clientes(clientes: list):
    
    cpf = input('Informe o CPF (somente número): ')
    cliente: Cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('\n@@@ Já existe cliente com esse CPF! @@@')
        return 
    
    nome: str = input('Informe o nome completo: ')
    data_nascimento: str = input('Infomre a data de nascimento (dd-mm-aaaa): ')
    endereco: str = input('Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ')

    cliente: Cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento,cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('\n=== Cliente criado com sucesso! ===')


def main():
    
    clientes = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_clientes(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
            
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()


if __name__ == '__main__':

    main()