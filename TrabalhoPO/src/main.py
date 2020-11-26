import gurobipy as gp

#Criacao da matriz que vai armazenar os custos das transicoes
matrizCusto = []

#Leitura do Arquivo
file = open('17.txt')
lines = file.readlines()
file.close()

for i in range(len(lines)):
    aux = lines[i][:-1].split('\t')
    aux = [int(i) for i in aux if i!= '']
    matrizCusto.append(aux)

#Armazena quantidade de pontos de coleta
quantidadeNos = len(matrizCusto)

#Cria os indices
origens = [i + 1 for i in range(quantidadeNos)]
destinos = [i + 1 for i in range(quantidadeNos)]

#Cria um dicionario para os custos
custos = dict()
for i, origem in enumerate(origens):
    for j, destino in enumerate(destinos):
        custos[origem, destino] = matrizCusto[i][j]

#Criacao do modelo
modelo = gp.Model('ColetaDeLixo')

#Criacao das Variaveis de decisao
x = modelo.addVars(origens, destinos, vtype=gp.GRB.BINARY)
u = modelo.addVars(origens[1:], vtype=gp.GRB.INTEGER, ub=quantidadeNos - 1)

#Funcao Objetivo
modelo.setObjective(x.prod(custos), sense=gp.GRB.MINIMIZE)

#Restricoes de garantir que todos os nos sejam origem pelo menos uma vez
c1 = modelo.addConstrs(
    gp.quicksum(x[i, j] for j in destinos if i != j) >= 1
                for i in origens),
    
#Restricoes para garantir que todos os nos sejam destino pelo menos uma vez    
c2 = modelo.addConstrs(
   gp.quicksum(x[i, j] for i in origens if i != j) >= 1
   for j in destinos)

#Restricoes de eliminacao de subrotas
c3 = modelo.addConstrs(
    u[i] - u[j] + quantidadeNos * x[i,j] <= quantidadeNos - 1
    for i in origens[1:] for j in destinos[1:] if i != j)

modelo.optimize()








