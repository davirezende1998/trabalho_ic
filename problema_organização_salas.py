# -*- coding: utf-8 -*-
"""
Aplicando o ILS ao Problema da Organização das Salas
Inteligência Computacional - DCC136 - 2020.1 - ERE - UFJF
Aluno: Davi Rezende        
Professora: Luciana Brugiolo Gonçalvez
"""
#%% BIBLIOTECAS
import numpy as np
import random
from random import seed
import time
seed(1)

#%% NÓ
class Sala:
    #construtor
    def __init__(self, id, comprimento):
        self.id = id
        self.comprimento = comprimento
        self.centro = comprimento/2
        self.posicao = 0
        
    def getId(self):
        return self.id
    
    def getComprimento(self):
        return self.comprimento
    
    def getCentro(self):
        return self.centro
    
    def getPosicao(self):
        return self.posicao
    
    def setId(self, id):
        self.id = id
        
    def setComprimento(self, comprimento):
        self.comprimento = comprimento
        
    def setCentro(self, centro):
        self.centro = centro
        
    def setPosicao(self, posicao):
        self.posicao = posicao
        
#%% ARESTA
class Trafego:
    #construtor
    def __init__(self, id, sala_A, sala_B, media_trafego):
        self.id = id
        self.sala_A = sala_A
        self.sala_B = sala_B
        self.media_trafego = media_trafego
        
    def getId(self):
        return self.id
    
    def getSala_A(self):
        return self.sala_A
    
    def getSala_B(self):
        return self.sala_B
    
    def getMediaTrafego(self):
        return self.media_trafego
    
    def setId(self, id):
        self.id = id
        
    def setSala_A(self, sala_A):
        self.sala_A = sala_A
        
    def setSala_B(self, sala_B):
        self.sala_B = sala_B
        
    def setMediaTrafego(self, media_trafego):
        self.media_trafego = media_trafego

#%% GRAFO 
class Corredor():
    #construtor
    def __init__(self):
        self.salas = []
        self.trafegos = []
        
    def buscarSala(self, id):
        for i in self.salas:
            if id == i.getId():
                return i
            
    def buscarTrafego(self, id):
        for i in self.trafegos:
            if id == i.getId():
                return i
    
    def criarSala(self, id, comprimento):
        if self.buscarSala(id) is None:
            self.salas.append(Sala(id, comprimento))
            
    def criarTrafego(self, id, sala_A, sala_B, media_trafego):
        if self.buscarTrafego(id) is None:
            self.trafegos.append(Trafego(id, sala_A, sala_B, media_trafego))

    #algoritmo construtivo guloso que gera uma solucao inicial-----------------------------------------
    def algoritmoConstrutivo(self):
        #comprimento de cada lado do corredor
        comp_lado_cima = 0
        comp_lado_baixo = 0
        custo_total = 0 #custo
        
        #solução de cada lado do corredor
        lado_cima = []
        lado_baixo = []
        
        #arestas que serão ordenadas pelo tráfego
        candidatos = self.trafegos.copy()
        candidatos.sort(key = lambda trafego: trafego.media_trafego, reverse = True)
        
        #%% PRIMEIRA INSERÇÃO
        aresta = candidatos.pop(0)
        sala_A = aresta.getSala_A()
        sala_B = aresta.getSala_B()
        trafego = aresta.getMediaTrafego()
        
        #1ª posição: supondo sala_A e sala_B no mesmo lado
        sala_B.setPosicao(sala_A.getComprimento()+sala_B.getCentro())
        custo_mesmo_lado = abs(sala_A.getCentro()-sala_B.getCentro())*trafego
        
        #2ª posção: supondo sala_A e sala_B em lados opostos
        custo_lado_oposto = abs(sala_A.getCentro()-sala_B.getCentro())*trafego
        
        #1ª
        if custo_mesmo_lado < custo_lado_oposto:
            #adiciona na solução
            lado_cima.append(sala_A)
            lado_cima.append(sala_B)
            
            #atualizla as posições e os comprimentos
            sala_A.setPosicao(sala_A.getCentro())
            comp_lado_cima += sala_A.getComprimento()
            comp_lado_cima += sala_B.getComprimento()
            
            #atualiza o custo
            custo_total += custo_mesmo_lado
        #2ª
        else:
            lado_cima.append(sala_A)
            lado_baixo.append(sala_B)    
            sala_A.setPosicao(sala_A.getCentro())
            sala_B.setPosicao(sala_B.getCentro())    
            comp_lado_cima += sala_A.getComprimento()
            comp_lado_baixo += sala_B.getComprimento()    
            custo_total += custo_lado_oposto

        #%% DEMAIS INSERÇÕES
        #enquanto houver candidatos a serem inseridos na solução
        while len(candidatos) != 0:   
            aresta = candidatos.pop(0)    
            sala_A = aresta.getSala_A()
            sala_B = aresta.getSala_B()
            trafego = aresta.getMediaTrafego()
            
            #verifica se as salas já pertencem à solução
            pertence_A = False
            pertence_B = False
            
            for i in lado_cima:
                if i == sala_A:
                    pertence_A = True

                if i == sala_B:
                    pertence_B = True
                
            for i in lado_baixo:
                if i == sala_A:
                    pertence_A = True
                    
                if i == sala_B:
                    pertence_B = True
            
            #ambas as salas não pertencem à solução
            if pertence_A == False and pertence_B == False:
                #tráfegos com a sala_A
                trafs_sala_A_cima = []
                trafs_sala_A_baixo = []
                
                #tráfegos com a sala_B
                trafs_sala_B_cima = []
                trafs_sala_B_baixo = []
                
                #veirifca se o tráfego já foi inserido
                for i in lado_cima:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_A) or (j.getSala_A() == sala_A and j.getSala_B() == i):
                            trafs_sala_A_cima.append(j.getMediaTrafego())                    
                            candidatos.remove(j)
                            
                        if (j.getSala_A() == i and j.getSala_B() == sala_B) or (j.getSala_A() == sala_B and j.getSala_B() == i):
                            trafs_sala_B_cima.append(j.getMediaTrafego())                    
                            candidatos.remove(j)

                for i in lado_baixo:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_A) or (j.getSala_A() == sala_A and j.getSala_B() == i):
                            trafs_sala_A_baixo.append(j.getMediaTrafego())                    
                            candidatos.remove(j)

                        if (j.getSala_A() == i and j.getSala_B() == sala_B) or (j.getSala_A() == sala_B and j.getSala_B() == i):
                            trafs_sala_B_baixo.append(j.getMediaTrafego())                    
                            candidatos.remove(j)        
                custos_temp = []
                
                #1ª posição: supondo sala_A em cima e sala_B em baixo:    
                sala_A.setPosicao(comp_lado_cima+sala_A.getCentro())
                sala_B.setPosicao(comp_lado_baixo+sala_B.getCentro())        
                custo_temp = custo_total
                
                for i in range(len(trafs_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_cima[i]
                    
                for i in range(len(trafs_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_baixo[i]
                    
                for i in range(len(trafs_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_cima[i]
                    
                for i in range(len(trafs_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao()-sala_B.getPosicao()))*trafego        
                custos_temp.append(custo_temp)
                
                #2ª posição: supondo sala_B em cima e sala_A em baixo:    
                sala_A.setPosicao(comp_lado_baixo+sala_A.getCentro())
                sala_B.setPosicao(comp_lado_cima+sala_B.getCentro())        
                custo_temp = custo_total
                
                for i in range(len(trafs_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_cima[i]
                    
                for i in range(len(trafs_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_baixo[i]
                    
                for i in range(len(trafs_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_cima[i]
                    
                for i in range(len(trafs_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao()-sala_B.getPosicao()))*trafego        
                custos_temp.append(custo_temp)
                
                #3ª posição: supondo sala_A e sala_B, nessa ordem, no lado de cima
                sala_A.setPosicao(comp_lado_cima+sala_A.getCentro())
                sala_B.setPosicao(comp_lado_cima+sala_A.getComprimento()+sala_B.getCentro())        
                custo_temp = custo_total
                
                for i in range(len(trafs_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_cima[i]
                    
                for i in range(len(trafs_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_baixo[i]
                    
                for i in range(len(trafs_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_cima[i]
                    
                for i in range(len(trafs_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao()-sala_B.getPosicao()))*trafego        
                custos_temp.append(custo_temp)
                
                #4ª posição: supondo sala_B e sala_A, nessa ordem, no lado de cima
                sala_B.setPosicao(comp_lado_cima+sala_B.getCentro())
                sala_A.setPosicao(comp_lado_cima+sala_B.getComprimento()+sala_A.getCentro())        
                custo_temp = custo_total
                
                for i in range(len(trafs_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_cima[i]
                    
                for i in range(len(trafs_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_baixo[i]
                    
                for i in range(len(trafs_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_cima[i]
                    
                for i in range(len(trafs_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao()-sala_B.getPosicao()))*trafego        
                custos_temp.append(custo_temp)
                
                #5ª posição: supondo sala_A e sala_B, nessa ordem, no lado de baixo
                sala_A.setPosicao(comp_lado_baixo+sala_A.getCentro())
                sala_B.setPosicao(comp_lado_baixo+sala_A.getComprimento()+sala_B.getCentro())
                custo_temp = custo_total
                
                for i in range(len(trafs_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_cima[i]
                    
                for i in range(len(trafs_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_baixo[i]
                    
                for i in range(len(trafs_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_cima[i]
                    
                for i in range(len(trafs_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao()-sala_B.getPosicao()))*trafego
                custos_temp.append(custo_temp)
                
                #6ª posição: supondo sala_B e sala_A, nessa ordem, no lado de baixo
                sala_B.setPosicao(comp_lado_baixo+sala_B.getCentro())
                sala_A.setPosicao(comp_lado_baixo+sala_B.getComprimento()+sala_A.getCentro())
                custo_temp = custo_total

                for i in range(len(trafs_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_cima[i]
                    
                for i in range(len(trafs_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_A.getPosicao()))*trafs_sala_A_baixo[i]
                    
                for i in range(len(trafs_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_cima[i]
                    
                for i in range(len(trafs_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao()-sala_B.getPosicao()))*trafs_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao()-sala_B.getPosicao()))*trafego
                custos_temp.append(custo_temp)
                menor_custo_i = np.argmin(custos_temp)
                
                #1ª
                if menor_custo_i == 0:
                    lado_cima.append(sala_A)
                    lado_baixo.append(sala_B)    
                    sala_A.setPosicao(comp_lado_cima+sala_A.getCentro())
                    sala_B.setPosicao(comp_lado_baixo+sala_B.getCentro())
                    comp_lado_cima += sala_A.getComprimento()
                    comp_lado_baixo += sala_B.getComprimento()
                #2ª
                elif menor_custo_i == 1:
                    lado_cima.append(sala_B)
                    lado_baixo.append(sala_A)
                    sala_A.setPosicao(comp_lado_baixo+sala_A.getCentro())
                    sala_B.setPosicao(comp_lado_cima+sala_B.getCentro())    
                    comp_lado_cima += sala_B.getComprimento()
                    comp_lado_baixo += sala_A.getComprimento()
                #3ª
                elif menor_custo_i == 2:
                    lado_cima.append(sala_A)
                    lado_cima.append(sala_B)    
                    sala_A.setPosicao(comp_lado_cima+sala_A.getCentro())
                    sala_B.setPosicao(comp_lado_cima+sala_A.getComprimento()+sala_B.getCentro())
                    comp_lado_cima += sala_A.getComprimento()+sala_B.getComprimento()
                #4ª
                elif menor_custo_i == 3:
                    lado_cima.append(sala_B)
                    lado_cima.append(sala_A)    
                    sala_B.setPosicao(comp_lado_cima+sala_B.getCentro())
                    sala_A.setPosicao(comp_lado_cima+sala_B.getComprimento()+sala_A.getCentro())    
                    comp_lado_cima += sala_B.getComprimento()+sala_A.getComprimento()
                #5ª
                elif menor_custo_i == 4:
                    lado_baixo.append(sala_A)
                    lado_baixo.append(sala_B)
                    sala_A.setPosicao(comp_lado_baixo+sala_A.getCentro())
                    sala_B.setPosicao(comp_lado_baixo+sala_A.getComprimento()+sala_B.getCentro())
                    comp_lado_baixo += sala_A.getComprimento()+sala_B.getComprimento()
                #6ª
                else:
                    lado_baixo.append(sala_B)
                    lado_baixo.append(sala_A)
                    sala_B.setPosicao(comp_lado_baixo+sala_B.getCentro())
                    sala_A.setPosicao(comp_lado_baixo+sala_B.getComprimento()+sala_A.getCentro())                    
                    comp_lado_baixo += sala_B.getComprimento()+sala_A.getComprimento()                                        
                
                custo_total = custos_temp[menor_custo_i]
                    
            #sala_B não pertence à solução
            if pertence_A == True and pertence_B == False:
                #tréfegos com a sala_B
                trafegos_sala_cima = []
                trafegos_sala_baixo = []                
                #veirifca se o tráfego já foi inserido
                for i in lado_cima:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_B) or (j.getSala_A() == sala_B and j.getSala_B() == i):
                            trafegos_sala_cima.append(j.getMediaTrafego())                            
                            candidatos.remove(j)
                            
                for i in lado_baixo:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_B) or (j.getSala_A() == sala_B and j.getSala_B() == i):
                            trafegos_sala_baixo.append(j.getMediaTrafego())                            
                            candidatos.remove(j)
                            
                #supondo sala_B em cima
                sala_B.setPosicao(comp_lado_cima+sala_B.getCentro())                
                custo_temp_cima = custo_total
                
                for i in range(len(trafegos_sala_cima)):
                    custo_temp_cima += (abs(lado_cima[i].getPosicao()-sala_B.getPosicao()))*trafegos_sala_cima[i]
                    
                for i in range(len(trafegos_sala_baixo)):
                    custo_temp_cima += (abs(lado_baixo[i].getPosicao()-sala_B.getPosicao()))*trafegos_sala_baixo[i]
                    
                #supondo sala_B em baixo
                sala_B.setPosicao(comp_lado_baixo+sala_B.getCentro())                
                custo_temp_baixo = custo_total
                
                for i in range(len(trafegos_sala_cima)):
                    custo_temp_baixo += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*trafegos_sala_cima[i]
                    
                for i in range(len(trafegos_sala_baixo)):
                    custo_temp_baixo += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*trafegos_sala_baixo[i]
                
                #adicionado a sala_B na solução: critério do comprimento dos lados
                if custo_temp_cima < custo_temp_baixo:
                    lado_cima.append(sala_B)                    
                    custo_total = custo_temp_cima                    
                    sala_B.setPosicao(comp_lado_cima+sala_B.getCentro())                    
                    comp_lado_cima += sala_B.getComprimento()
                elif custo_temp_baixo < custo_temp_cima:
                    lado_baixo.append(sala_B)                    
                    custo_total = custo_temp_baixo                    
                    sala_B.setPosicao(comp_lado_baixo+sala_B.getCentro())                    
                    comp_lado_baixo += sala_B.getComprimento()
                else:
                    if comp_lado_baixo <= comp_lado_cima:
                        lado_baixo.append(sala_B)                    
                        custo_total = custo_temp_baixo                    
                        sala_B.setPosicao(comp_lado_baixo+sala_B.getCentro())                    
                        comp_lado_baixo += sala_B.getComprimento()
                    else:
                        lado_cima.append(sala_B)                    
                        custo_total = custo_temp_cima                    
                        sala_B.setPosicao(comp_lado_cima+sala_B.getCentro())                        
                        comp_lado_cima += sala_B.getComprimento()
                        
            #sala_A não pertence à solução
            if pertence_A == False and pertence_B == True:
                #trafegos com a sala_A
                trafegos_sala_cima = []
                trafegos_sala_baixo = []
                
                #veirifca se o tráfego já foi inserido
                for i in lado_cima:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_A) or (j.getSala_A() == sala_A and j.getSala_B() == i):
                            trafegos_sala_cima.append(j.getMediaTrafego())                            
                            candidatos.remove(j)
                            
                for i in lado_baixo:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_A) or (j.getSala_A() == sala_A and j.getSala_B() == i):
                            trafegos_sala_baixo.append(j.getMediaTrafego())                            
                            candidatos.remove(j)
                            
                #supondo sala_A em cima
                sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())                
                custo_temp_cima = custo_total
                
                for i in range(len(trafegos_sala_cima)):
                    custo_temp_cima += (abs(lado_cima[i].getPosicao()-sala_A.getPosicao()))*trafegos_sala_cima[i]
                    
                for i in range(len(trafegos_sala_baixo)):
                    custo_temp_cima += (abs(lado_baixo[i].getPosicao()-sala_A.getPosicao()))*trafegos_sala_baixo[i]
                    
                #supondo sala_A em baixo
                sala_A.setPosicao(comp_lado_baixo+sala_A.getCentro())                
                custo_temp_baixo = custo_total
                
                for i in range(len(trafegos_sala_cima)):
                    custo_temp_baixo += (abs(lado_cima[i].getPosicao()-sala_A.getPosicao()))*trafegos_sala_cima[i]
                    
                for i in range(len(trafegos_sala_baixo)):
                    custo_temp_baixo += (abs(lado_baixo[i].getPosicao()-sala_A.getPosicao()))*trafegos_sala_baixo[i]
                
                #adicionado a sala_A na solução: critério do comprimento dos lados
                if custo_temp_cima < custo_temp_baixo:
                    lado_cima.append(sala_A)                    
                    custo_total = custo_temp_cima                    
                    sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())                    
                    comp_lado_cima += sala_A.getComprimento()
                elif custo_temp_baixo <  custo_temp_cima:
                    lado_baixo.append(sala_A)                    
                    custo_total = custo_temp_baixo                    
                    sala_A.setPosicao(comp_lado_baixo + sala_A.getCentro())                    
                    comp_lado_baixo += sala_A.getComprimento()
                else:
                    if comp_lado_baixo <= comp_lado_cima:
                        lado_baixo.append(sala_A)                    
                        custo_total = custo_temp_baixo                    
                        sala_A.setPosicao(comp_lado_baixo+sala_A.getCentro())                    
                        comp_lado_baixo += sala_A.getComprimento()
                    else:
                        lado_cima.append(sala_A)                    
                        custo_total = custo_temp_cima                    
                        sala_A.setPosicao(comp_lado_cima+sala_A.getCentro())                        
                        comp_lado_cima += sala_A.getComprimento()
        
        custo_total = corredor.recalculaCusto(lado_cima, lado_baixo)
        return lado_cima, lado_baixo, custo_total
        #---------------------------------------------------------------------------------------------------
    
    #funcao que recebe como parametros duas disposicoes de corredores e calcula o custo total
    def recalculaCusto(self, lado_cima, lado_baixo):
        comp_lado_cima = 0
        comp_lado_baixo = 0
        custo_temp = 0
        ts = self.trafegos.copy()

        for i in lado_cima:
            i.setPosicao(comp_lado_cima + i.getCentro())    
            comp_lado_cima += i.getComprimento()
        
        for i in lado_baixo:
            i.setPosicao(comp_lado_baixo + i.getCentro())  
            comp_lado_baixo += i.getComprimento()
        
        #atualiza custo lado_cima com lado_cima
        for i in range(len(lado_cima)):
            n = i+1
            while n < len(lado_cima):
                for t in ts:
                    if(t.getSala_A() == lado_cima[i] and t.getSala_B() == lado_cima[n]) or (t.getSala_A() == lado_cima[n] and t.getSala_B() == lado_cima[i]):
                        custo_temp += abs(lado_cima[i].getPosicao() - lado_cima[n].getPosicao())*t.getMediaTrafego()                
                        ts.remove(t)                
                        break
                n += 1
            
            #atualiza custo lado_cima com lado_baixo
            for j in range(len(lado_baixo)):
                for t in ts:
                    if(t.getSala_A() == lado_cima[i] and t.getSala_B() == lado_baixo[j]) or (t.getSala_A() == lado_baixo[j] and t.getSala_B() == lado_cima[i]):
                        custo_temp += abs(lado_cima[i].getPosicao() - lado_baixo[j].getPosicao())*t.getMediaTrafego()                
                        ts.remove(t)                
                        break
        
        #atualiza custo lado_baixo com lado_baixo
        for i in range(len(lado_baixo)):
            n = i+1
            while n < len(lado_baixo):
                for t in ts:
                    if(t.getSala_A() == lado_baixo[i] and t.getSala_B() == lado_baixo[n]) or (t.getSala_A() == lado_baixo[n] and t.getSala_B() == lado_baixo[i]):
                        custo_temp += abs(lado_baixo[i].getPosicao() - lado_baixo[n].getPosicao())*t.getMediaTrafego()                
                        ts.remove(t)                
                        break      
                n += 1
        return custo_temp
    
    #funcao que implementa a busca local. Movimento: troca dois elementos de posicao
    def buscaLocal(self, lado_cima, lado_baixo, custo_total):
        i=0
        while i < len(lado_cima):
            #movimento: lado_cima com lado_cima
            n = i+1
            while n < (len(lado_cima)):
                sala_n = lado_cima[n]
                lado_cima[n] = lado_cima[i]
                lado_cima[i] = sala_n   
                custo_temp = self.recalculaCusto(lado_cima, lado_baixo)
            
                if custo_temp < custo_total:
                    custo_total = custo_temp
                    
                else:
                    sala_n = lado_cima[n]
                    lado_cima[n] = lado_cima[i]
                    lado_cima[i] = sala_n
                
                n += 1
                
            k = i
            while k < len(lado_baixo):
                #movimento: lado_cima com lado_baixo
                sala_j = lado_baixo[k]
                lado_baixo[k] = lado_cima[i]
                lado_cima[i] = sala_j   
                custo_temp = self.recalculaCusto(lado_cima, lado_baixo)
                
                if custo_temp < custo_total:
                    custo_total = custo_temp
                        
                else:
                    sala_j = lado_baixo[k]       
                    lado_baixo[k] = lado_cima[i]
                    lado_cima[i] = sala_j
                
                k+=1
            i+=1
              
        i = 0
        #movimento: lado_baixo com lado_baixo
        while (i < len(lado_baixo)):
            n = i+1
            while n < (len(lado_baixo)):
                sala_n = lado_baixo[n]
                lado_baixo[n] = lado_baixo[i]
                lado_baixo[i] = sala_n
                custo_temp = self.recalculaCusto(lado_cima, lado_baixo)
                
                if custo_temp < custo_total:
                    custo_total = custo_temp

                else:
                    sala_n = lado_baixo[n]
                    lado_baixo[n] = lado_baixo[i]
                    lado_baixo[i] = sala_n
                    
                n += 1  
            i+=1
            
        return lado_cima, lado_baixo, custo_total

    #funcao que aplica a perturbacao em um otimo local, para explorarmos novas regioes no espaco de busca
    def perturbacao(self, lado_cima, lado_baixo): #2 swap-moves, 1 interchange move     
        #swap moves
        lado = random.randint(1, 2) #sorteia em qual lado vamos mexer/1 eh cima, 2 eh baixo
        if(lado == 1):
            sala = random.randint(0, (len(lado_cima)-1))
            if(sala == (len(lado_cima)-1)): #se for a ultima sala do corredor, muda pra sala anterior
                sala = sala - 1
            aux = lado_cima[sala]
            lado_cima[sala] = lado_cima[sala+1]
            lado_cima[sala+1] = aux
                
        else:
            sala = random.randint(0, (len(lado_baixo)-1))
            if(sala == (len(lado_baixo)-1)): #se for a ultima sala do corredor, muda pra sala anterior
                sala = sala - 1
            aux = lado_baixo[sala]
            lado_baixo[sala] = lado_baixo[sala+1]
            lado_baixo[sala+1] = aux               
        
        lado = random.randint(1, 2) #sorteia em qual lado vamos mexer/1 eh cima, 2 eh baixo
        if(lado == 1):
            sala = random.randint(0, (len(lado_cima)-1))
            if(sala == (len(lado_cima)-1)): #se for a ultima sala do corredor, muda pra sala anterior
                sala = sala - 1
            aux = lado_cima[sala]
            lado_cima[sala] = lado_cima[sala+1]
            lado_cima[sala+1] = aux
                
        else:
            sala = random.randint(0, (len(lado_baixo)-1))
            if(sala == (len(lado_baixo)-1)): #se for a ultima sala do corredor, muda pra sala anterior
                sala = sala - 1
            aux = lado_baixo[sala]
            lado_baixo[sala] = lado_baixo[sala+1]
            lado_baixo[sala+1] = aux               
        
        #interchange move
        lado = random.randint(1,2)
        lado2 = random.randint(1,2)
        if(lado == 1):
            sala1 = random.randint(0, (len(lado_cima)-1))
        else:
            sala1 = random.randint(0, (len(lado_baixo)-1))
                        
        if(lado2 == 1):
            sala2 = random.randint(0, (len(lado_cima)-1))
        else:
            sala2 = random.randint(0, (len(lado_baixo)-1))
            
        if(lado == 1 and lado2 == 1):
            aux = lado_cima[sala1]
            lado_cima[sala1] = lado_cima[sala2]
            lado_cima[sala2] = aux
        else:
            if(lado==1 and lado2==2):
                aux = lado_cima[sala1]
                lado_cima[sala1] = lado_baixo[sala2]
                lado_baixo[sala2] = aux
            else:
                if(lado==2 and lado2==1):
                    aux = lado_baixo[sala1]
                    lado_baixo[sala1] = lado_cima[sala2]
                    lado_cima[sala2] = aux
                else:
                    aux = lado_baixo[sala1]
                    lado_baixo[sala1] = lado_baixo[sala2]
                    lado_baixo[sala2] = aux
        
        #agora que a perturbacao foi aplicada, vamos aplicar uma busca local
        novo_custo = (self.recalculaCusto(lado_cima, lado_baixo))     
        return lado_cima, lado_baixo, novo_custo
    
#%% LEITURA DAS INSTÂNCIAS
def leitura(nome_arquivo, corredor):
    num_salas = 0
    i = 1
    for linha in arquivo:
        if i == 1:
            salas = linha.split()
            num_salas = int(salas[0]) #guarda o número de salas        
        if i == 2:
            comprimentos = linha.split()
            
            for j in range(num_salas):
                corredor.criarSala(j+1, int(comprimentos[j])) #cria os nós            
            break            
        i+=1    
    matriz_trafegos = np.zeros((num_salas, num_salas))
    i = 0
    for linha in arquivo:
        trafegos = linha.split()    
        for j in range(num_salas):
            matriz_trafegos[i][j] = int(trafegos[j])        
        i+=1
    id = 1
    for i in range(num_salas):        
        for j in range(num_salas):
            if i > j:
                corredor.criarTrafego(id, corredor.buscarSala(i+1), corredor.buscarSala(j+1), int(matriz_trafegos[i][j])) #cria as aresta
                id+=1
    arquivo.close()
    return True
#%% INSTÂNCIAS
#nessa lista devem ser colocados os nomes dos arquivos instancias a serem lidos
nomes_arq = ["S10","S11","A15","QAP_sko42_01_n","QAP_sko42_02_n","QAP_sko42_03_n", "QAP_sko42_04_n","QAP_sko42_05_n",
"QAP_sko49_01_n","QAP_sko49_02_n","QAP_sko49_03_n","QAP_sko49_04_n","QAP_sko49_05_n","QAP_sko56_01_n","QAP_sko56_02_n",
"QAP_sko56_03_n","QAP_sko56_04_n","QAP_sko56_05_n","CAP_n_60_d_30_L_30_1","CAP_n_60_d_30_L_30_2","CAP_n_60_d_30_L_30_3",
"CAP_n_60_d_30_L_40_1","CAP_n_60_d_30_L_40_2","CAP_n_60_d_30_L_40_3","CAP_n_60_d_30_L_50_1","CAP_n_60_d_30_L_50_2",
"CAP_n_60_d_30_L_50_3","CAP_n_60_d_30_L_60_1","CAP_n_60_d_30_L_60_2","CAP_n_60_d_30_L_60_3",
"CAP_n_60_d_60_L_30_1","CAP_n_60_d_60_L_30_2","CAP_n_60_d_60_L_30_3","CAP_n_60_d_60_L_40_1",
"CAP_n_60_d_60_L_40_2","CAP_n_60_d_60_L_40_3","CAP_n_60_d_60_L_50_1","CAP_n_60_d_60_L_50_2",
"CAP_n_60_d_60_L_50_3","CAP_n_60_d_60_L_60_1","CAP_n_60_d_60_L_60_2","CAP_n_60_d_60_L_60_3",
"CAP_n_60_d_90_L_30_1","CAP_n_60_d_90_L_30_2","CAP_n_60_d_90_L_30_3","CAP_n_60_d_90_L_40_1","CAP_n_60_d_90_L_40_2","CAP_n_60_d_90_L_40_3",
"CAP_n_60_d_90_L_50_2","CAP_n_60_d_90_L_50_3","CAP_n_60_d_90_L_60_1","CAP_n_60_d_90_L_60_2","CAP_n_60_d_90_L_60_3"]

num_insts = len(nomes_arq)
#%% INTERFACE
print("*INTELIGÊNCIA COMPUTACIONAL*")
print("Aplicando o ILS ao Problema da Organização de Salas")

opcao_analise = ""
while opcao_analise != str(3):
    print("\nOPÇÕES DE ANÁLISE:")
    print("(1) ALGORITMO ILS")
    print("(2) SAIR")
    teste = True
    while teste:
        opcao_analise = input("Opção: ")
        if opcao_analise != "1" and opcao_analise != "2":
            print("Digite (1/2).")
        else:
            teste = False

    if opcao_analise == "1":
        #lista para armazenar os tempos e os custos medidos para uma instancia
        custos = []
        #disposição, de cada instância, da solução do algoritmo construtivo
        disps_cima_constr = []
        disps_baixo_constr = []
        #disposição, de cada instância, da solução da busca local
        disps_cima_bl = []
        disps_baixo_bl = []
 
        for i in range(num_insts -1):
            arquivo_aberto = False
            while arquivo_aberto == False:
                try:
                    arquivo = open("insts/" + nomes_arq[i] + ".txt", 'r', encoding = "utf8")
                    arquivo_aberto = True
                except:
                    print("\nArquivo '" + nomes_arq[i] + "' inexistente!")
                    nomes_arq.remove(nomes_arq[i])
                    num_insts -= 1
            
            #instancia a estrutura de grafo
            corredor = Corredor()
            
            if leitura(nomes_arq[i], corredor) == False:
                print("\nErro na leitura do arquivo! Verifique o arquivo de entrada.")
            
            else:
                #comeca a medir o tempo do ils
                t_inicial_ils = time.time()
                print("\nInstância '" + nomes_arq[i] + "' algoritmo construtivo...")
                #execução do algoritmo construtivo
                lado_cima, lado_baixo, custo_constr = corredor.algoritmoConstrutivo()
                print("Concluído!")
                solucao_cima_constr = []
                solucao_baixo_constr = []
                
                for j in lado_cima:
                    solucao_cima_constr.append(j.getId())
                    
                for j in lado_baixo:
                    solucao_baixo_constr.append(j.getId())

                print("configuracao apos o algoritmo construtivo")
                print(solucao_cima_constr)
                print(solucao_baixo_constr)
                print("custo = " + str(custo_constr))
                disps_cima_constr.append(solucao_cima_constr)
                disps_baixo_constr.append(solucao_baixo_constr)
                
                print("\nInstância '" + nomes_arq[i] + "' busca local...")
                #execução da primeira busca local
                lado_cima, lado_baixo, custo_bl = corredor.buscaLocal(lado_cima, lado_baixo, custo_constr)
                print("Concluído!")
                solucao_cima_bl = []
                solucao_baixo_bl = []
                
                for j in lado_cima:
                    solucao_cima_bl.append(j.getId())
                    
                for j in lado_baixo:
                   solucao_baixo_bl.append(j.getId())
                
                disps_cima_bl.append(solucao_cima_bl)
                disps_baixo_bl.append(solucao_baixo_bl)
                print("configuracao apos a busca local")
                print(solucao_cima_bl)
                print(solucao_baixo_bl)
                print("custo = " + str(custo_bl))
                
                #variavel que determina o numero de iteracoes a serem aplicadas
                iteracoes = 0
                custo_total = custo_bl #guarda o custo corrente (referente ao otimo local encontrado na primeira busca local, aplicada na solucao inicial)
                custo_corrente_it = 0#guarda o custo do otimo local da iteracao atual
                while iteracoes < 10:
    
                    #aplicando a perturbacao-----------------------------------------------------------------
                    print("\nInstância '" + nomes_arq[i] + "' perturbacao...")
                    lado_cima_pert, lado_baixo_pert, custo_pert = corredor.perturbacao(lado_cima, lado_baixo)
                    print("Concluído!")
                    print("configuracao apos a " + str(iteracoes + 1) + " perturbacao")                
                    solucao_cima_pert = []
                    solucao_baixo_pert =[]
                    for j in lado_cima_pert:
                        solucao_cima_pert.append(j.getId())
                        
                    for j in lado_baixo_pert:
                        solucao_baixo_pert.append(j.getId())
                    print(solucao_cima_pert)
                    print(solucao_baixo_pert)
                    print("custo = " + str(custo_pert))
                    custo_corrente_it = custo_pert
                    #----------------------------------------------------------------------------------------
                    
                    #aplicando busca local-------------------------------------------------------------------
                    print("\nInstância '" + nomes_arq[i] + "' segunda busca local...")
                    lado_cima_pert, lado_baixo_pert, custo_pert = corredor.buscaLocal(lado_cima_pert, lado_baixo_pert, custo_constr)
                    print("Concluído!")
                    print("configuracao apos a " + str(iteracoes + 1) + " busca local")
                    for j in lado_cima_pert:
                        solucao_cima_pert.append(j.getId())
                        
                    for j in lado_baixo_pert:
                        solucao_baixo_pert.append(j.getId())
                    #reutilizando as variaveis solucao_cima_pert, solucao_baixo_pert, custo_pert
                    print(solucao_cima_pert)
                    print(solucao_baixo_pert)
                    print("custo = " + str(custo_pert))
                    custo_corrente_it = custo_pert
                
                    #funcao criterio de aceitacao
                    #solucoes melhores sempre sao aceitas
                    if(custo_corrente_it <= custo_total):
                        custo_total = custo_corrente_it
                    else:
                        #solucoes piores podem ser aceitas, se o custo corrente for pelo menos 90% do novo custo
                        res = custo_total / custo_corrente_it
                        if(res >= 0.90):
                            custo_total = custo_corrente_it
                    
                    custos.append(custo_total) #guarda o custo resultante dessa iteracao na lista de custos                                        
                    iteracoes = iteracoes + 1 #passa para a proxima iteracao

                t_final_ils = time.time()
                t_ils = t_final_ils - t_inicial_ils #calcula o tempo necessario para as 10 execucoes de cada instancia
                
                #calcula o custo medio, e recupera o menor custo obtido
                s = 0
                menor = custos[0]
                aux = 0
                for k in custos:
                    s += k
                    aux = k
                    if(aux < menor):
                        menor = aux
                s = s / 10
                
                print("\nDADOS FINAIS: Instância '" + nomes_arq[i] + "'")
                print("a media dos custos para essa instancia foi: " + str(s))
                print("o menor custo para essa instancia foi: " + str(menor))
                print("o tempo de execucao para essa instancia foi: " + str(t_ils))    
                print()
                print("--------------------------------------------------------------")
                print()
                print()
                
                
                #zera os custos para a proxima instancia
                custos = []
                arquivo.close()
    else:
        print("\nEncerrando aplicação...")