class Fornecedor:
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email
    
    def visualizar(self):
        print(
            'Nome:\t\t', self.nome,
            '\nTelefone:\t', self.telefone,
            '\nE-mail:\t\t', self.email,
            '\n'
        )

    def __iter__(self):
        yield self.nome
        yield self.telefone
        yield self.email

class SistemaFornecedor:
    def __init__(self):
        self.fornecedores = []
        self.arquivo_padrao = 'contatos.csv'

    def validar_nome(self, nome):
        """
        Verficar se o a string enviada é um nome válido.
        Parameters:
            nome (str): A string que será verificada.
        Returns:
            sucesso (bool): Verdadeiro se nome for válido, falso se inválido.
        """
        # se nome contem apenas letras do alfabeto é um nome valido
        if (nome.isalpha()) and nome != '':
            return True
        else:
            return False

    def validar_telefone(self, telefone):
        """
        Verficar se o a string enviada é um telefone válido.
        Parameters:
            telefone (str): A string que será verificada.
        Returns:
            sucesso (bool): Verdadeiro se telefone for válido, falso se inválido.
        """
        telefone_valido = True
        # Um telefone válido é composto apenas de dígitos, e possui entre 8 e 13 digitos
        if not(telefone.isdigit() and  (len(telefone) >= 8 and len(telefone) <= 13)):
            telefone_valido = False
        return telefone_valido

    def validar_email(self, email):
        """
        Verficar se o a string enviada é um email válido.
        Parameters:
            email (str): A string que será verificada.
        Returns:
            sucesso (bool): Verdadeiro se email for válido, falso se inválido.
        """
        import re
        # usando expressões regulares obtida na internet para validar email
        r = re.compile(r'^[\w\.-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
        
        email_valido = True
        # se o e-mail não corresponder a expressão regular não é válido
        if not(r.match(email)):
            email_valido = False
        return email_valido
        
    def visualizar_fornecedores(self):
        """
        Imprimir lista de fornecedores.
        Parameters:
            Nenhum.
        Returns:
            Nenhum.
        """
        for fornecedor in self.fornecedores:
            fornecedor.visualizar()
    
    def buscar_fornecedor(self, valor):
        """
        Percorre a lista de fornecedores verificando se qualquer campo do Fornecedor é igual ao paramentro da função.
        Parameters:
            valor (str): O valor que será checada em cada campo de cada Fornecedor na lista de fornecedores.
        Returns:
            O índice (int) onde o valor é igual a algum campo ou falso (bool) caso não encontre.
        """
        for indice, fornecedor in enumerate(self.fornecedores):
            if (fornecedor.nome == valor or fornecedor.telefone == valor or fornecedor.email == valor):
                # confirma se fornecedor é o fornecedor desejado (caso possua múltiplos com mesmo valor)
                fornecedor.visualizar()
                # é necessário caso tenha dois contatos com o mesmo valor
                confirma = input('Favor confirmar se este é o contato buscado (digite \'S\' para confirmar): ').lower()
                if confirma == 's':
                    return  indice
        return False
    
    def adicionar_fornecedor(self, nome, telefone, email):
        """
        Adiciona um novo fornecedor a lista de fornecedores.
        Parameters:
            nome (str): nome do novo fornecedor
            telefone (int): telefone do novo fornecedor
            email (str): email do novo fornecedor
        Returns:
            indice (int): índice do novo fornecedor
        """
        self.fornecedores.append(Fornecedor(nome, telefone, email))
        return len(self.fornecedores)-1
    
    def remover_fornecedor(self, indice):
        """
        Remove fornecedor com índice do parametro.
        Parameters:
            indice (int): Índice do fornecedor a ser removido
        Returns:
            bool: True ou False dependendo se fornecedor foi removido com sucesso.
        """
        if (indice >= 0):
            self.fornecedores.pop(indice)
            return True
        return False

    def verificar_lista(self, lista_listas):
        """
        Verifica cada campo na lista de listas adiconando-o a sua respectiva lista (nome, telefone, email)
        Parameters:
            lista de listas: lista de listas que será verificada
        Returns:
            lista de fornecedores: retorna uma lista de fornecedores corretamente ordenada
        """
        lista_nomes = []
        lista_telefones = []
        lista_emails = []
        # para cada linha na lista de listas
        for linha in lista_listas:
            # para cada item
            for item in linha:
                # se for composto apenas de letras do alfabeto é um nome -> adicona a lista de nomes
                if item.isalpha():
                    lista_nomes.append(item)
                # se for composto apenas de digitos é um telefone -> adicona a lista de telefones
                elif item.isdigit():
                    lista_telefones.append(item)
                # se tiver @ no texto é um email -> adicona a lista de emails
                elif '@' in item:
                    lista_emails.append(item)
        # retorna uma lista de fornecedores corretamente ordenada
        return [Fornecedor(lista_nomes[x], lista_telefones[x], lista_emails[x]) for x in range(len(lista_nomes))]
                
    def carregar_arquivo(self, nome):
        """
        Carrega o arquivo e parseia o texto separando em uma lista de listas com um usuario por lista
        Parameters:
            nome (string): arquivo a ser carregado (opcional), caso '' usar 'contatos.csv'
        Returns:
            quantidade (int): retorna o número de fornecedores validados/carregados
        """
        if nome == '':
            nome = 'contatos.csv'
        # abre arquivo e carrega em texto (str)
        with open(nome, 'r') as arquivo:
            texto = arquivo.read()
        # separa cada linha em uma única string
        texto = texto.split('\n')
        # cria uma lista de listas separando cada string por ; o que acaba separando cada usuario por lista
        lista_fornecedor = [string.split(';') for string in texto]
        # envia a lista de listas para a funçao de verificação
        self.fornecedores = self.verificar_lista(lista_fornecedor)
        return len(self.fornecedores)
    
    def gravar_arquivo(self, nome_arquivo):
        """
        Grava a base de fornecedores no arquivo nome (ou 'contatos.csv' caso nome seja '')
        Parameters:
            nome (string): arquivo a ser carregado (opcional), caso '' usar 'contatos.csv'
        Returns:
            quantidade (int): retorna o número de fornecedores gravados
        """
        import csv
        # caso não tenha sido passado um nome usar padrão (contantos.csv)
        if nome_arquivo == '':
            nome_arquivo = 'contatos.csv'
        # abre arquivo para gravação
        arquivo = open(nome_arquivo, 'w')
        # utiliza separador ; e terminador de linha \n
        escritor = csv.writer(arquivo, delimiter=';', lineterminator='\n')        
        escritor.writerows(self.fornecedores)
        arquivo.close()
        return len(self.fornecedores)

    def menu_principal(self):
        """
        Imprime menu principal
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        print('=== Bem Vindo ao Sistema de Cadastro de Fornecedores ===')
        print('\nEscolha uma das opções abaixo.')
        print('1. Visualizar fornecedores')
        print('2. Busca fornecedores')
        print('3. Adicionar fornecedor')
        print('4. Remover fornecedor')
        print('5. Carregar arquivo de contato')
        print('6. Gravar arquivo de contato')
        print('7. Sair')
        
    def run(self):
        """
        Roda o programa principal em loop até selecionar opção de sair
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        self.menu_principal()
        # Carrega arquivo padrão
        contatos = self.carregar_arquivo('')
        print(f'\n{contatos} contatos carregados!')
        acao = int(input("\nO que deseja fazer? "))
        while acao != 7:                
            if acao == 1:
                print('===Visualização dos Fornecedores===\n')
                self.visualizar_fornecedores()
                print('\n===Fim da visualização===\n')

            elif acao == 2:
                print('===Busca de Fornecedores===\n')
                valor = input("Digite algum dado do fornecedor buscado: ")
                retorno = self.buscar_fornecedor(valor)
                # Se retorno for diferente de falso, mostrar fornecedor
                if retorno:
                    self.fornecedores[retorno].visualizar()
                else:
                    print('Fornecedor não encontrado!')
                print('\n===Fim da visualização===\n')

            elif acao == 3:
                print('===Adicionar Fornecedor===\n')
                
                nome = input("Digite o nome do contato do fornecedor: ")
                # Validar nome até obter input válido
                while not(self.validar_nome(nome.replace(' ', ''))):
                    print('O nome deve conter apenas letras e espaço.')
                    nome = input("Digite o nome do contato do fornecedor: ")
                
                telefone = input("Digite o telefone (ex: 551193218433) do contato do fornecedor: ")
                # Validar telefone até obter input válido
                while not(self.validar_telefone(telefone)):
                    print('O telefone deve conter apenas numeros (de 8 a 13 digitos cada).')
                    telefone = input("Digite o telefone (ex: 551193218433) do contato do fornecedor: ")

                email = input("Digite o email do contato do fornecedor: ")
                # Validar email até obter input válido
                while not(self.validar_email(email)):
                    print('E-mail inválido! Digite um e-mail válido.')
                    email = input("Digite o email do contato do cliente: ") 
                    
                # Adicionar fornecedor
                retorno = self.adicionar_fornecedor(nome.title(), telefone, email)
                print('\nContato adicionado:')
                # Visualizar fornecedor adicionado
                self.fornecedores[retorno].visualizar()
                print('\n===Fim da adição===\n')            

            elif acao == 4:
                print('===Remover Fornecedor===\n')
                confirma = ''
                retorno = False
                valor = input("Digite algum dado do fornecedor a ser removido: ")
                # Buscar dado digitado na lista de fornecedores
                retorno = self.buscar_fornecedor(valor)
                # Se fornecedor encontrado
                if retorno:
                    self.fornecedores[retorno].visualizar()
                    confirma = input('Deseja apagar contato (digite \'S\' para confirmar): ').lower()
                    if confirma == 's':
                        #  Remover fornecedor e confirmar se removido com sucesso.
                        if (self.remover_fornecedor(retorno)):
                            print('\nContato removido:')
                    else:
                        print('Remoção cancelada.')
                else:
                    print('Fornecedor não encontrado!')
                # Porque está aqui???
                # self.remover_fornecedor(valor)
                print('\n===Fim da remoção===\n')                
                
            elif acao == 5:                
                print("===Carregar arquivo===\n")
                arquivo = input("Digite o caminho do arquivo (deixe em branco para usar {}): ".format(self.arquivo_padrao))
                contatos = self.carregar_arquivo(arquivo)
                print(f'{contatos} contatos carregados!')
                print(f'\n===Fim do carregamento do arquivo===\n')                
                
            elif acao == 6:
                print("===Gravar arquivo===\n")
                arquivo = input("Digite o caminho do arquivo (deixe em branco para usar {}): ".format(self.arquivo_padrao))
                contatos = self.gravar_arquivo(arquivo)
                print(f'{contatos} contatos gravados!')
                print(f'\n===Fim da gravação do arquivo===\n')                
                
            self.menu_principal()
            acao = int(input("\nO que deseja fazer? "))
        print('===Fim===')

class Cliente:
    def __init__(self, nome, sobrenome, tel_list, email_list, empresa=''):
        self.ID = None
        self.nome = nome
        self.sobrenome = sobrenome
        self.tel_list = tel_list
        self.email_list = email_list
        self.empresa = empresa

    def visualizar(self):
        """
        Imprime os dados básicos do cliente
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        print(
            'ID:\t\t\t', self.ID,
            '\nNome:\t\t\t', self.nome,
            '\nSobrenome:\t\t', self.sobrenome,
            '\n'
        )
        
    def visualizar_completo(self):
        """
        Imprime os dados completos do cliente
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        print(
            'ID:\t\t\t', self.ID,
            '\nNome:\t\t\t', self.nome,
            '\nSobrenome:\t\t', self.sobrenome
        )
        for indice, telefone in enumerate(self.tel_list):
            print(f'Telefone {indice+1}:\t\t', telefone)
        for indice, email in enumerate(self.email_list):
            print(f'E-mail {indice+1}:\t\t', email)
        print('Empresa:\t\t', self.empresa)
    
    def __iter__(self):
        yield self.nome
        yield self.sobrenome
        yield self.tel_list
        yield self.email_list
        yield self.empresa

class SistemaCliente:
    def __init__(self):
        self.clientes = []
        # lista dos is criados. A medida que criamos novos usuários verificamos se o id já existe na lista.
        self.lista_id = []
        # dicionário que permite o agrupamento de contatos. Dicionário de lista de ids dos contatos.
        self.dicionario_grupos = {}

    def listar_grupos(self):
        """
        Lista os grupos cadastrados no dicionário de grupos.
        Parameters:
            Nenhum
        Returns:
            (bool): True se existem grupos cadastrados, False caso não haja nenhum grupo cadastrado
        """        
        if len(self.dicionario_grupos) == 0:
            return False
        else:
            print('Lista de grupos cadastrados:')
            for grupo in self.dicionario_grupos:
                print(grupo)
            return True
    
    def criar_grupo(self, nome_grupo):
        """
        Adiciona o grupo ao dicionário de grupos
        Parameters:
            nome_brupo (str): grupo que deve ser criado caso não exista.
        Returns:
            (bool): True caso grupo seja criado, False se grupo já existir.
        """
        if nome_grupo not in self.dicionario_grupos:
            self.dicionario_grupos[nome_grupo] = []
            print(f'Chave: {nome_grupo}, Valor: {self.dicionario_grupos[nome_grupo]}')
            return True
        else:
            print('Grupo já existe! Criação cancelada.')
            return False
    
    def remover_grupo(self, nome_grupo):
        """
        Remove o grupo do dicionário de grupos caso exista.
        Parameters:
            nome_grupo (str): nome do grupo que deve ser removido
        Returns:
            (bool): True se remover grupo, False se grupo não existir
        """
        if nome_grupo in self.dicionario_grupos:
            self.dicionario_grupos.pop(nome_grupo)
            print(f'Grupo {nome_grupo} removido com sucesso')
            return True
        else:
            print('Grupo não existe! Remoção cancelada.')
            return False
        
    def adicionar_ao_grupo(self, id_contato, nome_grupo):
        """
        Adiciona id do contato a lista do grupo em questão
        Parameters:
            id_contato (str): id do contato a adicionar
            nome_grupo (str): nome do grupo onde o contato será inserido
        Returns:
            (bool): True se adicionar contato, False se usuário já se encontra no grupo ou grupo não existir
        """ 
        # se grupo existir e id_contato não fizer parte da lista do grupo
        if nome_grupo in self.dicionario_grupos:
            if id_contato not in self.dicionario_grupos[nome_grupo]:
                # adicionar a lista
                self.dicionario_grupos[nome_grupo].append(id_contato)            
                print(f'Chave: {nome_grupo}, Valor: {self.dicionario_grupos[nome_grupo]}')
                return True
            else:
                print('Usuário já está no grupo. Adição a grupo cancelada.')
                return False
        else:
            print('Grupo não existe! Adição a grupo cancelada.')
            return False
    
    def remover_do_grupo(self, id_contato, nome_grupo):
        """
        Remove contato do usuário da lista do grupo
        Parameters:
            id_contato (str): id do contato a remover
            nome_grupo (str): nome do grupo de onde o contato será removido
        Returns:
            (bool): True se remover contato, False se usuário não estava no grupo ou grupo não existir
        """
        # Grupo existe?
        if nome_grupo in self.dicionario_grupos:
            # Usuário está no grupo?
            if id_contato in self.dicionario_grupos[nome_grupo]:
                tmp = self.dicionario_grupos[nome_grupo].remove(id_contato)            
                print(f'Chave: {nome_grupo}, Valor: {tmp}')
                return True
            else:
                print('Usuário não está no grupo. Remoção do grupo cancelada.')
                return False
        else:
            print('Grupo não existe! Adição a grupo cancelada.')
            return False
    
    def visualizar_grupo(self, nome_grupo):
        """
        Imprime contatos que fazem parte do grupo
        Parameters:
            nome_grupo (str): nome do grupo cujos contatos devem ser impressos
        Returns:
            Nenhum
        """
        if nome_grupo in self.dicionario_grupos:
            for id_contato in self.dicionario_grupos[nome_grupo]:
                for cliente in self.clientes:
                    if cliente.ID == id_contato:
                        print('\n')
                        cliente.visualizar_completo()
                                
    def visualizar_clientes(self):
        """
        Imprime visualização básica de todos os clientes do cadastro
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        for cliente in self.clientes:
            cliente.visualizar()
            
    def listar_empresas(self):
        """ Não usado no momento.
        Retorna uma lista contendo todas as empresas cadastradas nos contatos.
        Parameters:
            Nenhum.
        Returns:
            (list): uma lista contendo todas as empresas que fazem parte do cadastro de cliente.
        """
        return list(set([cliente.empresa for cliente in self.clientes]))

    def visualizar_empresa(self, empresa):
        """ Não usado no momento.
        Imprime o cadastro completo de todos os contatos empresa com valor igual ao parametro passado.
        Parameters:
            empresa (str): nome da empresa que deseja imprimir o cliente.
        Returns:
            (bool): True se empresa existir em algum cliente do cadastro, False se não existir.
        """
        empresa_encontrada = False
        # para cada cliente
        for cliente in self.clientes:
            # se cliente.empresa for igual ao parametro imprime cadastro completo
            if cliente.empresa == empresa:
                empresa_encontrada = True
                cliente.visualizar_completo()
        if empresa_encontrada == False:
            print('Cliente não encontrado.')
        return empresa_encontrada
            
    def validar_nome(self, nome):
        """
        Valida nome inputado pelo cliente. De conter apenas letras do alfabeto e não conter espaço.
        Parameters:
            nome (str): nome a ser validado.
        Returns:
            (bool): True se nome for válido, False se não for.
        """
        if (nome.isalpha()) and nome != '':
            return True
        else:
            return False
    
    def validar_telefones(self, tel_list):
        """
        Valida lista de telefones enviada como parametro. Deve conter de 8 a 13 digitos.
        Parameters:
            tel_list (list of str): lista de telefones a serem validados.
        Returns:
            (bool): True se telefones forem válidos, False se não forem.
        """
        # inicia considerando telefones válidos
        telefones_validos = True
        # para cada item na lista
        for tel in tel_list:
            # valida critérios
            if not(tel.isdigit() and  (len(tel) >= 8 and len(tel) <= 13)):
                telefones_validos = False
        return telefones_validos

    def validar_emails(self, email_list):
        """
        Valida lista de emails enviada como parametro. Utilizamos expressão regular indicada em sites na internet.
        Parameters:
            email_list (list of str): lista de emails a serem validados.
        Returns:
            (bool): True se emails forem válidos, False se não forem.
        """
        import re
        r = re.compile(r'^[\w\.-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
        # inicia considerando válido
        emails_validos = True
        # para cada item da lista
        for email in email_list:
            # se não vaidar com a expressão regular é inválido
            if not(r.match(email)):
                emails_validos = False
        return emails_validos
    
    def busca_contato(self, item):
        """
        Busca pelo paramentro enviado em qualquer campo da lista de contatos
        Parameters:
            item (str): valor que será buscado em todos os campos do cliente.
        Returns:
            Posição (int) onde o item foi encontrado, None se não encontrar
        """
        self.item = item
        indice = None
        # para cada item em clientes
        for x, cliente in enumerate(self.clientes):
            # Verifica id
            if cliente.ID == item:
                indice = x
                cliente.visualizar_completo()
                # é necessário checar caso item seja duplicado em diferentes clientes e este não seja o desejado
                encontrado = input('Este é o cadastro procurado (\'S\' para confirmar)? ').lower()
                if encontrado == 's':
                    return indice
            # Verifica nome
            elif cliente.nome == item:
                indice = x
                cliente.visualizar_completo()
                # é necessário checar caso item seja duplicado em diferentes clientes e este não seja o desejado
                encontrado = input('Este é o cadastro procurado (\'S\' para confirmar)? ').lower()
                if encontrado == 's':
                    return indice
            # Verifica sobrenome
            elif cliente.sobrenome == item:
                indice = x
                cliente.visualizar_completo()
                # é necessário checar caso item seja duplicado em diferentes clientes e este não seja o desejado
                encontrado = input('Este é o cadastro procurado (\'S\' para confirmar)? ').lower()
                if encontrado == 's':
                    return indice
            # Verifica lista de telefone
            elif item in cliente.tel_list:
                indice = x
                cliente.visualizar_completo()
                # é necessário checar caso item seja duplicado em diferentes clientes e este não seja o desejado
                encontrado = input('Este é o cadastro procurado (\'S\' para confirmar)? ').lower()
                if encontrado == 's':
                    return indice
            # Verifica lista de emails
            elif item in cliente.email_list:
                indice = x
                cliente.visualizar_completo()
                # é necessário checar caso item seja duplicado em diferentes clientes e este não seja o desejado
                encontrado = input('Este é o cadastro procurado (\'S\' para confirmar)? ').lower()
                if encontrado == 's':
                    return indice
            # Verifica empresa
            elif cliente.empresa == item:
                indice = x
                cliente.visualizar_completo()
                # é necessário checar caso item seja duplicado em diferentes clientes e este não seja o desejado
                encontrado = input('Este é o cadastro procurado (\'S\' para confirmar)? ').lower()
                if encontrado == 's':
                    return indice
        # se não encontrar retorna o None
        return indice

    def gerar_ID(self):
        """
        Gera um id único ainda não inserido na lista de IDs
        Parameters:
            Nenhum
        Returns:
            random_number (str): string de número único gerado para o ID
        """
        import random
        # cria uma stringo baseada em um inteiro randomico de 3 digitos
        random_number = str(random.randint(100, 999))
        # Vai gerando um novo id até a straing não estar contida na lista
        while random_number in self.lista_id:
            random_number = str(random.randint(100, 999))
        # Adiciona inteiro a lista de Ids usados
        self.lista_id.append(random_number)
        return random_number
            
    def adicionar_cliente(self, nome, sobrenome, tel_list, email_list, empresa=''):
        """
        Adiciona cliente a lista de clientes
        Parameters:
            nome (str): nome do cliente
            sobrenome (str): sobrenome do cliente
            tel_list (list of str): Lista de telefones do cliente
            email_list (list of str): Lista de emails do cliente
            empresa: empresa do cliente
        Returns:
            (int): representando o índice do cliente adicionado ou False se já possui 75 clientes cadastrados
        """
        if len(self.clientes) < 75:
            # Cria cliente e adiciona a lista
            self.clientes.append(Cliente(nome, sobrenome, tel_list, email_list, empresa))
            # Cria ID único do cliente
            self.clientes[len(self.clientes)-1].ID=self.gerar_ID()
            return len(self.clientes)-1
        return False       
    
    def alterar_cliente(self, ID, nome, sobrenome, tel_list, email_list, empresa):
        """
        Altera dados dos clientes caso diferente de '' em caso de string e tamanho > 0 em caso de lista
        Parameters:
            nome (str): nome do cliente
            sobrenome (str): sobrenome do cliente
            tel_list (list of str): Lista de telefones do cliente
            email_list (list of str): Lista de emails do cliente
            empresa: empresa do cliente
        Returns:
            Nenhum
        """
        if nome != '':
            print(f'Alterando nome para {nome}')
            self.clientes[ID].nome = nome.title()
        elif sobrenome != '':
            print(f'Alterando sobrenome para {sobrenome}')
            self.clientes[ID].sobrenome = sobrenome.title()
        elif len(tel_list) > 0:
            print(f'Alterando telefones para {tel_list}')
            self.clientes[ID].tel_list = tel_list
        elif len(email_list) > 0:
            print(f'Alterando email para {email_list}')
            self.clientes[ID].email_list = email_list
        elif empresa != '':
            print(f'Alterando empresa para {empresa}')
            self.clientes[ID].empresa = empresa.title()

    def carregar_contatos(self):
        """
        Carrega contatos do exercidio anterior como base de testes
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        self.clientes = []
        fornecedor = SistemaFornecedor()
        fornecedor.carregar_arquivo('')
        for contato in fornecedor.fornecedores:
            self.adicionar_cliente(contato.nome, '', [contato.telefone], [contato.email], empresa='')
        return len(self.clientes)
        
    def menu_principal(self):
        """
        Imprime menu principal do programa
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        print('=== Bem Vindo ao Sistema de Cadastro de Clientes ===')
        print('\nEscolha uma das opções abaixo.')
        print('1. Visualizar contatos')
        print('2. Busca contatos')
        print('3. Adicionar contato')
        print('4. Remover contato')
        print('5. Alterar contato')
        print('6. Carregar lista Parte I')        
        print('7. Visualizar grupo')
        print('8. Gestão de grupos')
        print('9. Sair')

    def menu_grupos(self):
        """
        Imprime sub-menu de gerenciamento de grupos
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        print('=== Gestão de grupos ===')
        print('\nEscolha uma das opções abaixo.')
        print('1. Listar grupo')
        print('2. Criar grupo')
        print('3. Remover grupo')
        print('4. Adicionar contato a grupo')
        print('5. Remover contato de grupo')
        print('6. Voltar')
       
    def run(self):
        """
        Programa principal
        Parameters:
            Nenhum
        Returns:
            Nenhum
        """
        self.menu_principal()
        acao = int(input("\nO que deseja fazer? "))
        while acao != 9:
            if acao == 1:
                print('===Visualização dos Clientes===\n')
                self.visualizar_clientes()
                print('\n===Fim da visualização===\n')
                
            elif acao == 2:
                print('===Busca de Clientes ===\n')
                item = input('Digite um item para busca: ')
                try:
                    self.busca_contato(item.title())
                except:
                    print('contato não encontrado')
                
                print('\n===Fim da busca===\n')
                
            elif acao == 3:
                print('===Adicionar Cliente===\n')
                nome = input("Digite o nome do contato do cliente: ")
                # Valida o nome enviado pelo cliente removendo o espaço entre os diferentes nomes
                while not(self.validar_nome(nome.replace(' ', ''))):
                    print('O nome deve conter apenas letras e espaço.')
                    nome = input("Digite o nome do contato do cliente: ")
                    
                sobrenome = input("Digite o sobrenome do contato do cliente: ")
                # Sobreome é válido se for letra do alfabeto ou for vazio, senão solicita novo sobrenome.
                while (not(sobrenome.isalpha()) and sobrenome != ''):
                    print('O sobrenome deve ser único e conter apenas letras.')
                    sobrenome = input("Digite o sobrenome do contato do cliente: ")

                telefones = input("Digite os telefones (ex: 551193218433) do contato do cliente (separados por espaço): ")
                # Separa string de telefones em uma lista de strings de telefones
                tel_list = telefones.split(' ')
                # enquanto telefone não for valido solicita novo telefone
                while not(self.validar_telefones(tel_list)):
                    print('O telefone deve conter apenas numeros (de 8 a 13 digitos cada).')
                    telefones = input("Digite os telefones (ex: 551193218433) do contato do cliente (separados por espaço): ")
                    tel_list = telefones.split(' ')
                
                email = input("Digite os emails do contato do cliente (separados por espaço): ")
                # Separa string de emails em uma lista de strings de telefones
                email_list = email.split(' ')
                while not(self.validar_emails(email_list)):
                    print('E-mail inválido! Digite um e-mail válido.')
                    email = input("Digite os emails do contato do cliente (separados por espaço): ")                
                    email_list = email.split(' ')
                    
                empresa = input("Digite o nome da empresa onde o contato trabalha: ")
                
                # Caso todos intens sejam validos adicionar a cadastro
                retorno = self.adicionar_cliente(nome.title(), sobrenome, tel_list, email_list, empresa.title())                
                if retorno != False:
                    print('\nContato adicionado:')
                    self.clientes[retorno].visualizar_completo()
                else:
                    print('Limite atingido, remova um contato antes de tentar novamente.')
                print('\n===Fim da adição===\n')
                
            elif acao == 4:
                print('===Remover Cliente===\n')                
                item = input("Digite o id do contato a ser removido: ")
                # Verifica se id existe na lista de clientes
                indice = self.busca_contato(item.title())
                if indice != False:
                    if (indice <= len(self.clientes) and indice >= 1):
                        confirma = input('Deseja realmente remover o contato acima (S/N): ')
                        if (confirma.lower() == 's'):
                            print(f'Removendo contato {indice}')
                            self.clientes.pop(indice)
                            print('\nContato removido:')                        
                        else:
                            print('Remoção cancelada!')
                print('\n===Fim da remoção===\n')

            elif acao == 5:
                print('===Alterar Cliente===\n')
                valor = input("Digite o id do contato a ser alterado: ")
                # Verifica se id existe na lista de clientes
                indice = self.busca_contato(valor.title())
                if indice != False:                
                    if (indice <= len(self.clientes) and indice >= 1):
                        # Qual campo deve ser alterado?
                        campo = input('Qual campo você deseja alterar (nome, sobrenome, telefone, e-mail, empresa): ').lower()
                        while campo == 'nome' or campo == 'sobrenome' or campo == 'telefone' or campo == 'e-mail' or campo == 'empresa':
                            try:
                                if campo == 'nome':
                                    # Valida o nome enviado pelo cliente removendo o espaço entre os diferentes nomes
                                    nome = input("Digite o nome do contato do cliente: ")
                                    while not(self.validar_nome(nome.replace(' ', ''))):
                                        print('O nome deve conter apenas letras e espaço.')
                                        nome = input("Digite o nome do contato do cliente: ")
                                    # Envia para alteração deixando outros campos vazios '' ou []
                                    self.alterar_cliente(indice, nome, '', [], [], '')
                                elif campo == 'sobrenome':
                                    sobrenome = input("Digite o sobrenome do contato do cliente: ")
                                    # Sobreome é válido se for letra do alfabeto ou for vazio, senão solicita novo sobrenome.
                                    if sobrenome != '':
                                        while not(sobrenome.isalpha()):
                                            print('O sobrenome deve ser único e conter apenas letras.')
                                            sobrenome = input("Digite o sobrenome do contato do cliente: ")
                                    # Envia para alteração deixando outros campos vazios '' ou []
                                    self.alterar_cliente(indice, '', sobrenome, [], [], '')
                                elif campo == 'telefone':                                    
                                    telefones = input("Digite os telefones (ex: 551193218433) do contato do cliente (separados por espaço): ")
                                    # Separa string de telefones em uma lista de strings de telefones
                                    tel_list = telefones.split(' ')
                                    # enquanto telefone não for valido solicita novo telefone
                                    while not(self.validar_telefones(tel_list)):
                                        print('O telefone deve conter apenas numeros (de 8 a 13 digitos cada).')
                                        telefones = input("Digite os telefones (ex: 551193218433) do contato do cliente (separados por espaço): ")
                                        tel_list = telefones.split(' ')
                                    # Envia para alteração deixando outros campos vazios '' ou []
                                    self.alterar_cliente(indice, '', '', tel_list, [], '')
                                elif campo == 'e-mail':
                                    email = input("Digite os emails do contato do cliente (separados por espaço): ")
                                    # Separa string de emails em uma lista de strings de telefones
                                    email_list = email.split(' ')
                                    # Enquanto lista de email não for valida solicita novo(s) email(s)
                                    while not(self.validar_emails(email_list)):
                                        print('E-mail inválido! Digite um e-mail válido.')
                                        email = input("Digite os emails do contato do cliente (separados por espaço): ")                
                                        email_list = email.split(' ')
                                    # Envia para alteração deixando outros campos vazios '' ou []
                                    self.alterar_cliente(indice, '', '', [], email_list, '')                        
                                elif campo == 'empresa':
                                    empresa = input("Digite o nome da empresa onde o contato trabalha: ")
                                    # Envia para alteração deixando outros campos vazios '' ou []
                                    self.alterar_cliente(indice, '', '', [], [], empresa)
                                self.clientes[indice].visualizar_completo()
                            except ValueError:
                                print('id')
                            campo = input('Qual campo você deseja alterar (nome, sobrenome, telefone, e-mail, empresa): ').lower()
                else:
                    print('Id inválido.')
                print('\n===Fim da alteração===\n')

            elif acao == 6:
                print('===Carregar Fornecedores===\n')
                print(f'{self.carregar_contatos()} clientes carregados!')
                print('\n===Fim do carregamento===\n')
            
            elif acao == 7:
                print('===Visualizar grupo===\n')
                # Se grupo existir lista grupos solicita grupo para visualizar
                if (self.listar_grupos()):
                    nome_grupo = input("Digite o nome do grupo que deseja visualizar (em branco para cancelar): ")
                    # enquanto grupo não estiver no dicionario ou for vazio solicita grupo valido
                    while ((nome_grupo not in self.dicionario_grupos) and nome_grupo != ''):
                        print('Grupo não existe na lista de grupos.')
                        nome_grupo = input("Digite o nome do grupo que deseja visualizar (em branco para cancelar): ")
                    # Se grupo não for '' imprime grupo
                    if nome_grupo != '':
                        self.visualizar_grupo(nome_grupo)
                    else:
                        print('Visualização cancelada.')
                else:
                    print('Não existem grupos cadastrados.')
                print('\n===Fim da visualização de grupo===\n')
            
            elif acao == 8:
                self.menu_grupos()
                acao_grupo = int(input("\nO que deseja fazer? "))
                while acao_grupo != 6:
                    if acao_grupo == 1:
                        print('===Listar grupo===\n')
                        if (self.listar_grupos()==False):
                            print('Não existem grupos cadastrados.')
                        print('\n===Fim da listagem de grupo===\n')

                    elif acao_grupo == 2:
                        print('===Criar grupo===\n')
                        self.listar_grupos()                        
                        nome_grupo = input("Digite o nome do grupo que seja criar (em branco para cancelar): ")
                        # enquanto grupo não for letra do alfabeto ou vazio, solicita novo nome do grupo
                        while (not(nome_grupo.isalpha()) and nome_grupo != ''):
                            print('O nome do grupo deve ser único e conter apenas letras.')
                            nome_grupo = input("Digite o nome do grupo que seja criar (em branco para cancelar): ")
                        if nome_grupo != '':
                            self.criar_grupo(nome_grupo)
                        else:
                            print('Criação de grupo cancelada.')
                        print('\n===Fim da criação de grupo===\n')
                        
                    elif acao_grupo == 3:
                        print('===Remover grupo===\n')
                        if (self.listar_grupos()):
                            nome_grupo = input("Digite o nome do grupo que seja remover (em branco para cancelar): ")
                            if nome_grupo != '':
                                self.remover_grupo(nome_grupo)
                            else:
                                print('Remoção de grupo cancelada.')
                        else:
                            print('Não existem grupos para remover.')
                        print('\n===Fim da remoção de grupo===\n')
                        
                    elif acao_grupo == 4:
                        print('===Adicionar contato a grupo===\n')
                        if (self.listar_grupos()):
                            nome_grupo = input("Digite o nome do grupo ao qual deseja adicionar o contato (em branco para cancelar): ")
                            # Garante que nome do grupo é válido ou vazio
                            while ((nome_grupo not in self.dicionario_grupos) and (nome_grupo != '')):
                                print('Grupo não existe na lista de grupos.')
                                nome_grupo = input("Digite o nome do grupo ao qual deseja adicionar o contato (em branco para cancelar): ")
                            id_contato = input("Digite o id do contato a ser adicionado ao grupo (em branco para cancelar): ")
                            # Se o contato for '' não executar busca
                            if (id_contato != ''):
                                indice = self.busca_contato(id_contato)
                                while ((indice==None) and (nome_grupo != '')):
                                    id_contato = input("Digite o id do contato a ser adicionado ao grupo (em branco para cancelar): ")
                                    # Se o contato for '' não executar busca
                                    if (id_contato != ''):
                                        indice = self.busca_contato(id_contato)
                                confirma = input(f'Deseja adicionar contato {id_contato} ao grupo {nome_grupo} (\'S\' para confirmar): ').lower()
                                if confirma == 's':
                                    if (self.adicionar_ao_grupo(id_contato, nome_grupo)):
                                        print('Contato adicionado!')                                    
                        else:
                            print('Não existem grupos na lista. Favor criar o grupo antes de tentar adiconar o contato a ele.')
                
                        print('\n===Fim da adição de contatos a grupo===\n')
                        
                    elif acao_grupo == 5:
                        print('===Remover contato a grupo===\n')
                        if (self.listar_grupos()):
                            nome_grupo = input("Digite o nome do grupo do qual deseja remover o contato (em branco para cancelar): ")
                            # Garante que nome do grupo é válido ou vazio
                            while ((nome_grupo not in self.dicionario_grupos) and (nome_grupo != '')):
                                print('Grupo não existe na lista de grupos.')
                                nome_grupo = input("Digite o nome do grupo ao qual deseja adicionar o contato (em branco para cancelar): ")
                            id_contato = input("Digite o id do contato a ser removido do grupo (em branco para cancelar): ")
                            # Se o contato for '' não executar busca
                            if (id_contato != ''):
                                indice = self.busca_contato(id_contato)
                                while ((indice==None) and (nome_grupo != '')):
                                    id_contato = input("Digite o id do contato a ser removido do grupo (em branco para cancelar): ")
                                    # Se o contato for '' não executar busca
                                    if (id_contato != ''):
                                        indice = self.busca_contato(id_contato)
                                confirma = input(f'Deseja remover contato {id_contato} ao grupo {nome_grupo} (\'S\' para confirmar): ').lower()
                                if confirma == 's':
                                    print('Removendo...')
                                    self.remover_do_grupo(id_contato, nome_grupo)
                        else:
                            print('Não existem grupos na lista.')
                        print('\n===Fim da remoção de contatos a grupo===\n')
                        
                    self.menu_grupos()
                    acao_grupo = int(input("\nO que deseja fazer? "))                    
            else:
                print('Opção invalida')

            self.menu_principal()
            acao = int(input("\nO que deseja fazer? "))
        print('===Fim===')
