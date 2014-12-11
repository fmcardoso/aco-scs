import matplotlib.pyplot as plt

def plotExecution(acoSizeVector, scsSizeVector, acoDistVector, scsDistVector,
    pathPrefix):
    # Plota grafico de tamanhos
    plt.figure(1)
    plt.plot(acoSizeVector, linewidth=2, label = "Nosso")
    plt.plot(scsSizeVector, linewidth=2, label = "Inimigo")
    plt.legend(loc=2);
    plt.ylabel('Disparidade do Tamanho')
    plt.xlabel('Tamanho Sequências')
    plt.savefig(pathPrefix + "-tam.png")
    
    # Plota grafico de distância de edição
    plt.figure(2)
    plt.plot(acoDistVector, linewidth=2, label = "Nosso")
    plt.plot(scsDistVector, linewidth=2, label = "Inimigo")
    plt.legend(loc=2);
    plt.ylabel('Distância de Edição')
    plt.xlabel('Tamanho Sequências')
    plt.savefig(pathPrefix + "-dist.png")
    

def plotPair(k1, v1, k2, v2, pathPrefix, ylabel, sufix, n):
    plt.figure(n)
    plt.plot(*zip(*v1))
    plt.plot(*zip(*v2))
    plt.legend(loc=2);
    plt.ylabel(ylabel)
    plt.xlabel('Tamanho Sequências')
    plt.savefig(pathPrefix + "-" + sufix +  ".png")


def plotAll(data, pathPrefix):
    # Vetor de dados com tamanho das soluções
    acoSizeVector = []
    acoSizeVectorLabel = []
    gdySizeVector = []
    gdySizeVectorLabel = []

    # Vetor de dados com distancia das soluções
    acoDistVector = []
    acoDistVectorLabel = []
    gdyDistVector = []
    gdyDistVectorLabel = []
    
    for key, value in data.items():
        if key == "dist":
            for k, v in value.items():
                if k == "aco":
                    for k2, v2 in v.items():
                        acoDistVectorLabel.append(k2.split("-")[0])
                        acoDistVector.append([k2.split("-")[0], v2])
                else:
                    for k2, v2 in v.items():
                        gdyDistVectorLabel.append(k2.split("-")[0])
                        gdyDistVector.append([k2.split("-")[0], v2])
        if key == "tam":
            for k, v in value.items():
                if k == "aco":
                    for k2, v2 in v.items():
                        acoSizeVectorLabel.append(k2.split("-")[0])
                        acoSizeVector.append([k2.split("-")[0], v2])
                else:
                    for k2, v2 in v.items():
                        gdySizeVectorLabel.append(k2.split("-")[0])
                        gdySizeVector.append([k2.split("-")[0], v2])
    
    # Gera de tamanho
    plotPair(acoSizeVectorLabel, acoSizeVector, gdySizeVectorLabel, 
             gdySizeVector, pathPrefix, 'Disparidade do Tamanho', "tam", 5)
    
     # Gera de distancia
    plotPair(acoDistVectorLabel, acoDistVector, gdyDistVectorLabel, 
             gdyDistVector, pathPrefix, 'Distância de Edição', "gdy", 6)
    
    
                