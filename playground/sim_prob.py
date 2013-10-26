#! /usr/bin/python2

import numpy as np
import scipy as sp
import networkx as nx
import matplotlib.pyplot as plt
import random

## Plants and pollinators are defined by two traits: one is quantitative (proboscis / flower depth), and one is qualitative (flower color / flower preference)

## In addition, both have a population size (number of individuals)

class pollinator:
   def __init__(self, length, color, pop):
      self.x = length
      self.n = pop
      self.c = color
   def __str__(self):
      return "pol"
   def attributes(self):
      return {'type': 'pollinator', 'trait': self.x, 'pop': self.n, 'color': self.c}

class plant:
   def __init__(self, depth, color, pop):
      self.x = depth
      self.n = pop
      self.c = color
   def __str__(self):
      return "pla"
   def attributes(self):
      return {'type': 'plant', 'trait': self.x, 'pop': self.n, 'color': self.c}

colors = ["red", "blue", "orange"]
n_plants = 100
n_pollinators = 100

## Generate a pool of plants
Pl = [plant(np.random.normal(loc = 4.0), random.choice(colors), np.random.lognormal(0.5, 2.0)) for n in xrange(n_plants)]
## The same with pollinators
Po = [pollinator(np.random.normal(loc = 4.0), random.choice(colors), np.random.lognormal(1.5, 2.0)) for n in xrange(n_pollinators)]

## Rule for color preference
def colorPref(pref, col):
   if pref == col:
      return 1.0
   else :
      return 0.2

## Rule for length / depth
def traitMatch(l, d):
   return np.exp(-((l-d)**2)/float(2*0.35**2))

## Build a probabilistic network
## Three possibilities:
## 1. Traits only
## 2. Abudances only
## 3. Traits x abundances
pure_trait = np.zeros((n_plants, n_pollinators))
pure_abund = np.zeros((n_plants, n_pollinators))
both_terms = np.zeros((n_plants, n_pollinators))

plant_n = [pl.n for pl in Pl]
pollinator_n = [po.n for po in Po]

plant_N = np.max(plant_n)
pollinator_N = np.max(pollinator_n)

for i in xrange(len(Po)):
   for j in xrange(len(Pl)):
      N_ij = (Po[i].n / float(pollinator_N))*(Pl[j].n / float(plant_N))
      T_ij = colorPref(Po[i].c, Pl[j].c) * traitMatch(Po[i].x, Pl[j].x)
      pure_trait[i][j] = T_ij
      pure_abund[i][j] = N_ij
      both_terms[i][j] = (T_ij + N_ij)/2.0

print both_terms

def generateNetwork(po, pl, probamat):
   G = nx.DiGraph()
   for p in po:
      G.add_node(p, p.attributes())
   for p in pl:
      G.add_node(p, p.attributes())
   ## Start filling the matrix
   for i in xrange(len(po)):
      for j in xrange(len(pl)):
         if np.random.uniform() <= probamat[i][j]:
            G.add_edge(po[i], pl[j])
   return G

test_n1 = generateNetwork(Po, Pl, both_terms)

nx.write_gml(test_n1, "test.gml")
