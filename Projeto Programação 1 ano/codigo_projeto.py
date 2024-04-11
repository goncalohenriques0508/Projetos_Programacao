import math as mt
import matplotlib.pyplot as plt
    
#criação da classe Espécies
class Species:
    
    def __init__(self, nome_especie, tipo_folhagem, fruto, tipo_planta, raio_maximo_especie, idade_media_especie):
        folhagem = ('persistente','caduca','semicaduca')
        tipo = ('arvore','arbusto')
        if fruto == 'True':
            fruto = True
        elif fruto == 'False':
            fruto = False
        assert len(nome_especie)!=0
        assert len(tipo_folhagem)!=0 and tipo_folhagem in folhagem 
        assert type(fruto) is bool
        assert len(tipo_planta)!=0 and tipo_planta in tipo
        assert type(raio_maximo_especie) is float and raio_maximo_especie>0
        assert type(idade_media_especie) is int and idade_media_especie>0
        self.__especie = nome_especie
        self.__folhagem = tipo_folhagem
        self.__fruto = fruto
        self.__tipo = tipo_planta
        self.__raio_maximo = raio_maximo_especie
        self.__idade_media = idade_media_especie
        
    @property
    def especie(self):
        return self.__especie
    @property
    def folhagem(self):
        return self.__folhagem
    @property
    def fruto(self):
        return self.__fruto
    @property
    def tipo(self):
        return self.__tipo
    @property
    def raio_maximo(self):
        return self.__raio_maximo
    @property
    def idade_media(self):
        return self.__idade_media
    
    def area_planta(self):     
        return round(mt.pi*self.__raio_maximo**2,3)
    
    def __str__(self):
        return f"""Nome: {self.__especie}
Tipo de Folhagem: {self.__folhagem}
Produz Fruto: {self.__fruto}
Tipo de Planta: {self.__tipo}
Raio Máximo: {self.__raio_maximo} metros quadrados
Idade Média da Espécie: {self.__idade_media} anos"""
    
    def __eq__(self, other_specie):
        if not isinstance(other_specie, self.__class__):
            return False
        return self.__especie == other_specie.__especie

# TESTS
#s1 = Species('castanheiro','caduca',True,'arvore',8.1,100)  
#s2 = Species('cedro','persistente',False,'arvore',6.0,80)
#s3 = Species('pinheiro-manso','persistente',True,'arvore',3.0,100)
#s4 = Species('loureiro','persistente',False,'arbusto',3.0,40)
#s5 = Species('sobreiro','caduca',False,'arvore',5.0,40)


#criação da classe Planta
class Plant:
    
    def __init__(self, especie, localizacao_gps, ano_plantacao):
        assert type(localizacao_gps[0]) is float and type(localizacao_gps[1]) is float  
        assert type(ano_plantacao) is int and ano_plantacao>0
        self.__especie = especie
        self.__gps = localizacao_gps
        self.__ano = ano_plantacao
        
    @property
    def especie_pertencente(self):
        return self.__especie
    
    @property
    def parametros_especie(self):
        return str(self.__especie)
    
    @property
    def localizacao(self):
        return self.__gps
    
    @property
    def ano_plantacao(self):
        return self.__ano
    
    def area_planta(self):
        return self.especie_pertencente.area_planta()
    
    #calcula a idade da planta, e no caso em que o ano inserido como parametro for inferior ao ano em que a planta foi plantada entao retorna-se -1
    def age(self, random_year=2023):
        if random_year<self.ano_plantacao:
            return -1
        idade = random_year - self.__ano
        return idade
    
    #permite calcular a distancia entre a localizaçao de duas plantas 
    def distance_between_plants(self, loc1, loc2):
        return ((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)**0.5
    
    #calcula a distancia entre uma planta e uma localizaçao e se esta distancia for menor ou igual ao raio da planta entao encontra-se dentro
    def location(self, random_location):
        if ((random_location[0]-self.__gps[0])**2+(random_location[1]-self.__gps[1])**2)**0.5 <= self.__especie.raio_maximo:
            return True
        return False
    
    def __str__(self):
        return f"""{self.__especie}
Coordenadas: {self.__gps}
Ano Plantação: {self.__ano}
        """
    def __str_to_file__(self):
        return f"{self.especie_pertencente.especie},{self.localizacao[0]},{self.localizacao[1]},{self.ano_plantacao}\n"

# TESTS
#p1 = Plant(s2, (25.0,25.0), 2009)
#p2 = Plant(s5, (20.0,10.0), 2011)
#p3 = Plant(s3, (40.0,20.0), 2009)
#p4 = Plant(s1, (9.0,9.0), 2010)

#criação da classe Parque
class Park:
    
    def __init__(self, nome_park, medidas):
        assert type(medidas[0] and medidas[1]) is float and medidas[0]*medidas[1]>0 
        self.__nome_park = nome_park
        self.__medidas = medidas
        self.__list_plant_park = []
    
    #obtem-se o nome do parque
    @property
    def park(self):
        return self.__nome_park
    
    #permite obter as medidas do parque: comprimento e largura 
    @property
    def medidas(self):
        return self.__medidas
    
    #permite listar as plantas do parque consoante as funções "str" criadas nas classes acima
    @property 
    def lista_plantas(self):
        return self.__list_plant_park
              
    #calcula a area do parque tendo em conta as medidas do mesmo
    def area_park(self):
        return self.medidas[0]*self.medidas[1]
    
    #verifica se a planta que recebe como parametro esta dentro dos limites do parque
    #".localizacao[i]" permite obter a primeira e segunda coordenada da localizacao da planta
    #".especie_pertencente.raio_maximo" vai buscar o raio dessa planta
    #"self.medidas[i]" busca as coordenadas "x" e "y" 
    def is_inside_limits(self, plant):
        if plant.localizacao[0]-plant.especie_pertencente.raio_maximo<0:
            return False
        elif plant.localizacao[1]-plant.especie_pertencente.raio_maximo<0:
            return False
        elif plant.localizacao[0]+plant.especie_pertencente.raio_maximo>self.medidas[0]:
            return False
        elif plant.localizacao[1]+plant.especie_pertencente.raio_maximo>self.medidas[1]:
            return False
        return True
    
    def is_inside_limits_given_location(self, localizacao):
        return localizacao[0]<self.medidas[0] and localizacao[1]<self.medidas[1] and localizacao[0]>0 and localizacao[1]>0  
    
    #verifica dentro das condiçoes se e possivel adicionar uma planta com x coordenadas e se for possivel adiciona       
    def add_plant_park(self, plant):
        assert isinstance(plant, Plant)
        # Primeiramente verificas se a area disponivel no parque e maior que a area da planta 
        if self.free_area() >= plant.area_planta():
            #verifica se esta dentro dos limites do parque
            if not self.is_inside_limits(plant):
                raise ValueError("\nA planta não se encontra nos limites do parque!\n")
            #verifica se ainda nao existe nenhuma planta no parque se esta estiver dentro dos limites
            if len(self.__list_plant_park)==0:
                self.__list_plant_park.append(plant)
                return True
            # Verifica se a nova planta está dentro do somatório dos raios de qualquer planta existente
            for p in self.__list_plant_park:
                if isinstance(p, Plant) and plant.distance_between_plants(plant.localizacao, p.localizacao) <= (plant.especie_pertencente.raio_maximo + p.especie_pertencente.raio_maximo):
                    raise ValueError("\nA localização inserida coincide com a área de uma outra Planta\n")
            # Adiciona a nova planta ao parque caso as condiçoes anteriores nao se verifiquem
            self.__list_plant_park.append(plant)
            return True
        raise ValueError("\nNão existe área disponível para a plantar!\n")
        
    #remove uma planta tendo em conta uma localizaçao e se esta estiver dentro da area da planta, a planta e removida 
    def remove_plant_park(self, plant_localizacao):
        i = 0
        for p in self.__list_plant_park:
            if p.location(plant_localizacao):
                del self.__list_plant_park[i]
                return True         
            i+=1
        return False
    
    #o mesmo criterio que a anterior mas so e visto se a localizaçao encontra-se dentro de uma planta da lista
    def exist_plant(self, localizacao):  
        for p in self.__list_plant_park:
            if p.location(localizacao):
                return True
        return False
    
    def area_ocupada(self):
        soma_area=0
        for p in self.__list_plant_park:
            soma_area += p.area_planta()
        return soma_area
    
    def free_area(self):
        return self.area_park()-self.area_ocupada()
    
    #verifica se será possivel adicionar, e como chama a funçao de add plantas entao depois é necessario remove-la
    def there_is_space(self, plant):    
        print(self.free_area())
        print(plant.area_planta())        
        if self.add_plant_park(plant):
            del self.__list_plant_park[-1]
            return True
        return False
    
    def average_age_plants(self, random_year):
        soma_idades = 0
        total_plantas = 0
        no_plant = True
        for e in self.__list_plant_park:
            if e.age(random_year) >= 0:
                total_plantas+=1
                no_plant = False
        for e in self.__list_plant_park:
            soma_idades += e.age(random_year)
        if total_plantas > 0:
            return soma_idades/total_plantas 
        elif no_plant:
            return -1
    
    def how_many_species(self):
        if len(self.__list_plant_park)!=0:
            count_species=[]
            for plant in self.__list_plant_park:
                if plant.especie_pertencente.especie not in count_species:
                    count_species.append(plant.especie_pertencente.especie)
            return len(count_species)
        return 0
    
    def list_species(self):
        name_species=[]
        for p in self.__list_plant_park:
            if p.especie_pertencente.especie not in name_species:
                name_species.append(p.especie_pertencente.especie)
        return name_species
    
    def show_plants(self):
        for p in self.__list_plant_park:
                print(f"{p.parametros_especie}")
                print(f"Localização: {p.localizacao}")
                print(f"Ano Plantação: {p.ano_plantacao}\n")
    
    def show_plants_by_species(self): 
        result = ""              
        for e in self.list_species():
            for p in self.__list_plant_park:
                if p.especie_pertencente.especie == e:
                    result += f"\n{p.parametros_especie}\n"
                    result += f"Localização: {p.localizacao}\n"
                    result += f"Ano Plantação: {p.ano_plantacao}\n"
        return result
        
    def show_plants_by_plantation_year(self):
        list_species_by_year = []
        result = ""
        for p in self.__list_plant_park:
            if p.ano_plantacao not in list_species_by_year:
                list_species_by_year.append(p.ano_plantacao)
        mini=sorted(list_species_by_year)
        for e in mini:
            for p in self.__list_plant_park:
                if p.ano_plantacao==e:
                    result += f"\n{p.parametros_especie}\n"
                    result += f"Localização: {p.localizacao}\n"
                    result += f"Ano Plantação: {p.ano_plantacao}\n"
        return result
   
    def list_plants_above_average_age(self, year=2023):
        result = []
        for plant in self.__list_plant_park:
            if plant.age(year)>=plant.especie_pertencente.idade_media:
               result.append(plant)
        return result
    
    def mapa(self):
        fig, ax = plt.subplots()
        ax.set_xlim((0, self.medidas[0]))
        ax.set_ylim((0, self.medidas[1]))
        ax.set_box_aspect(1)
        loc = []
        raio = []
        for i in self.__list_plant_park: 
            loc.append(i.localizacao)
            raio.append(i.especie_pertencente.raio_maximo)
        for i in range(len(loc)):
            circle = plt.Circle(loc[i], raio[i], color='g', alpha=0.4)
            ax.add_patch(circle)
            ax.text(loc[i][0], loc[i][1], s="x", horizontalalignment='center', verticalalignment='center')
        plt.show()
        

def read_from():
    f = open("species.txt",'r')
    especies = dict()
    for species in f:
        nome_especie, tipo_folhagem, produz_fruto, tipo_planta, raio_maximo, idade_media_especie = species.split(',')
        especies[nome_especie] = Species(nome_especie, tipo_folhagem, produz_fruto, tipo_planta, float(raio_maximo), int(idade_media_especie))
    f.close()
    return especies
lista_especies = read_from()

def verificar_string_vazia(variavel):
    if variavel == "":
        return True
    return False

def verificar_string_to_float(variavel):
    numbers = ['1','2','3','4','5','6','7','8','9','0','.']
    contador_ponto_decimal = variavel.count('.')
    if contador_ponto_decimal > 1:
            return False
    for i in variavel:
        if i not in numbers:
            return False
    return True

def verificar_string_to_int(variavel):
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    for i in variavel:
        if i not in numbers:
            return False
    return True

parque = Park("Jamor", (80., 80.))
#park = Park("Parque verde", (120.,120.))

lista_1menu = ["Adicionar Planta", "Remover Planta", "Listar plantas existentes no parque", "Mostrar a área ocupada", "Mostrar a área disponível para plantação", "Mostrar o mapa do parque", "Estatísticas e informações", "Guardar o parque num ficheiro", "Sair"]  
i = 0
while i != 9:
    print(f"--------Gestao do Parque {parque.park}--------")
    w=1
    for element in lista_1menu:
        print(f"{w}. {element}")
        w+=1
    i = input(" > ")
    while not i.isdigit() or not 1 <= int(i) <= 9:
        i = input(" > ")
    i = int(i)
    if i == 1:
        try:
            print("\n---Espécies existentes---")
            for name in lista_especies:
                print(f"-> {name}")
            nome=input("\nEspécie pertencente: ")
            while verificar_string_vazia(nome) or nome not in lista_especies:
                print("Opção inválida!\n")
                nome=input("Espécie pertencente: ")
            if nome in lista_especies:
                loc_x=input("Eixo do x: ")
                while verificar_string_vazia(loc_x) or not verificar_string_to_float(loc_x):
                    print("Opção inválida!\n")
                    loc_x=input("Eixo do x: ")
                loc_x = float(loc_x)
                loc_y=input("Eixo do y: ")
                while verificar_string_vazia(loc_y) or not verificar_string_to_float(loc_y):
                    print("Opção inválida!\n")
                    loc_y=input("Eixo do y: ")
                loc_y = float(loc_y)
                ano_plantacao=input("Ano de Plantação: ")
                while verificar_string_vazia(ano_plantacao) or not verificar_string_to_int(ano_plantacao):
                    print("Opção inválida!\n")
                    ano_plantacao=input("Ano de Plantação: ")
                ano_plantacao = int(ano_plantacao)
                if parque.add_plant_park(Plant(lista_especies[nome], (loc_x, loc_y), ano_plantacao)) == True:
                    print("\nPlanta Adicionada com Sucesso!! \n")
        except ValueError as e:
            print(e)
    
    elif i == 2:
        print("\nQual a localizção da planta que deseja remover?")
        loc_x=input("Eixo do x: ")
        while verificar_string_vazia(loc_x) or not verificar_string_to_float(loc_x):
            print("Opção inválida!\n")
            loc_x=input("Eixo do x: ")
        loc_x = float(loc_x)
        loc_y=input("Eixo do y: ")
        while verificar_string_vazia(loc_y) or not verificar_string_to_float(loc_y):
            print("Opção inválida!\n")
            loc_y=input("Eixo do y: ")
        loc_y = float(loc_y)
        coordenadas = (loc_x, loc_y)
        if parque.remove_plant_park(coordenadas):
            print("\nPlanta encontrada e Removida!\n")
        elif not parque.is_inside_limits_given_location(coordenadas):
            print("\nA localização não coincide com a área do Parque.\n")
        else:
            print("\nA localização nao coincide com a área de uma planta no parque.\n")
    
    elif i == 3:
        if len(parque.lista_plantas) == 0:
            print("\nAinda não existem plantas no Parque!\n")
        else:
            print("\n-----Lista de Plantas-----\n")
            parque.show_plants()
    
    elif i == 4:
        if parque.area_ocupada() == 0:
            print("\nAinda não foram adicionadas Plantas!\n")
        else:
            print(f"\nA área ocupada é {parque.area_ocupada()} metros quadrados\n")
            
    elif i == 5:
        print("\nÁrea disponível para Plantação:")
        print(f"{parque.free_area()} metros quadrados\n")
        
    elif i == 6:
        parque.mapa()
        
    elif i == 7:
        lista_2menu = ["Mostrar a média de idades das plantas do parque", "Mostrar o número de espécies diferentes", "Listar as espécies existentes no parque", "Listar todas as plantas organizadas por espécie", "Listar todas as plantas organizadas por ano de plantação", "Listar as plantas que excederam o tempo médio de vida da sua espécie", "Histograma por idade", "Histograma por espécie"]  
        print("\n--------Estatísticas e Informações--------")
        number = 1
        for element in lista_2menu:
            print(f"{number}. {element}")
            number+=1
        option = input("> ")
        while not option.isdigit() or not 1 <= int(option) <= 8:
            option = input(" > ")
        option = int(option)
        
        if option == 1:
            if len(parque.lista_plantas) != 0:
                year = input("Qual o ano em conta?... ")
                while verificar_string_vazia(year) or not verificar_string_to_int(year):
                    print("Opção inválida!\n")
                    year=input("Qual o ano em conta?... ")
                year = int(year)
                if parque.average_age_plants(year) >= 0:
                    print(f"\nA idade média das plantas é {parque.average_age_plants(year)} anos\n")
                else:
                    print("\nPlantas não foram plantadas antes do ano em conta.\n")
            else:
                print("\nNão existem Plantas no parque\n")
        
        elif option == 2:
            if parque.how_many_species() == 0:
                print("\nAinda não foram adicionadas espécies !\n")
            elif parque.how_many_species() == 1:
                print(f"\n Existe {parque.how_many_species()} espécie no parque\n")
            else:
                print(f"\n Existem {parque.how_many_species()} espécies no parque\n")
        
        elif option == 3:
            if len(parque.list_species()) != 0:
                contador=1
                print("\n----Lista de Espécies----")
                for species in parque.list_species():
                    print(f"{contador} - {species}")
                    contador+=1
                print()
            else:
                print("\nNão existem plantas no Parque!\n")
        
        elif option == 4:
            if len(parque.list_species()) != 0:
                print("\n----Lista de Plantas organizadas por espécie----")
                print(parque.show_plants_by_species())
            else:
                print("\nDe momento não existem plantas no Parque!\n")
                
        elif option == 5:
            if len(parque.list_species()) != 0:
                print("\n----Lista de Plantas organizadas por ano de plantação----")
                print(parque.show_plants_by_plantation_year())
            else:
                print("\nDe momento não existem plantas no Parque!\n")
                
        elif option == 6:
            if len(parque.list_species()) != 0:
                year = input("Qual é o ano em consideração?... ")
                while verificar_string_vazia(year):
                    print("Opção inválida!\n")
                    year = input("Qual é o ano em consideração?... ")
                year = int(year) 
                if len(parque.list_plants_above_average_age(year)) > 0:
                    print("\n----Lista de Plantas que excederam o tempo médio de vida da sua espécie----\n")
                    for p in parque.list_plants_above_average_age(year):
                        print(p)
                else:
                    print("\nNão existem plantas que ultrapassaram o tempo médio de vida da sua espécie considerando o ano introduzido.\n")
            else:
                print("\nDe momento não existem plantas no Parque!\n")
             
        elif option == 7:
            if len(parque.list_species()) != 0:
                year = input("\nQual é o ano em consideração?... ")
                while verificar_string_vazia(year):
                    print("Opção inválida!")
                    year = input("\nQual é o ano em consideração?... ")
                year = int(year)
                labels = [] # idade das plantas em anos
                for plant in parque.lista_plantas:
                    if plant.age(year) != -1:
                        labels.append(str(plant.age(year)))
                if len(labels) != 0:
                    labels = sorted(labels)
                    values = [] # quantidade de plantas com x anos
                    i = 0
                    for age in labels:
                        values.append(0)
                        for plant in parque.lista_plantas:
                            if str(plant.age(year)) == age:
                                values[i] += 1   
                        i += 1
                    plt.bar(labels, values)
                    plt.show()
                else:
                    print("\nPlantas não foram plantadas antes do ano em consideração.\n")
            else:
                print("\nDe momento não existem plantas no Parque.\n")
            
        elif option == 8:
            if len(parque.lista_plantas) != 0:
                species = []# especies das plantas do parque
                for x in parque.lista_plantas:
                    species.append(str(x.especie_pertencente.especie))
                values = []# quantidade de plantas com x anos
                i = 0
                for specie in species:
                    values.append(0)
                    for plant in parque.lista_plantas:
                        if str(plant.especie_pertencente.especie) == specie:
                            values[i] += 1   
                    i += 1
                plt.bar(species, values)
                plt.show()
            else:
                print("\nPlantas não foram adicionadas ao Parque\n")
    elif i == 8:
        f = open("parks.txt", "w")
        f.write(parque.park)
        f.write(', (')
        f.write(str(parque.medidas[0]))
        f.write(',')
        f.write(str(parque.medidas[1]))
        f.write(')\n')
        for p in parque.lista_plantas:
            f.write(p.__str_to_file__())
        f.close()
        print("\nO Parque foi escrito com sucesso no ficheiro parks.txt\n")
        
        
#k1 = Park('josefina', (60.0,60.0))
