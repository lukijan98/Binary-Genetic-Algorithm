# -*- coding: utf-8 -*-


import random
import sys
import math
import matplotlib.pyplot as graph

"""**Function for generating chromosome with all zeros**


"""

def generateChromosome(numberOfBits):
  gen = []
  for i in range(0, numberOfBits+1):
    gen.append(0)
  return gen

"""**Encoding and decoding functions**

The normalization function is used for encoding and decoding. The values of the variables are scaled to the interval (0, 1). The function is then used to convert to binary value.
"""

def encoding(chromosome,interval,numberOfBits):
  chromosome2 = []
  pnorm = []
  lowerLimit = interval[0]
  upperLimit = interval[1]
  for i in range(0,2):
        chromosome2.append(generateChromosome(numberOfBits))
        pnorm.append((chromosome[i]-lowerLimit)/(upperLimit-lowerLimit))
          
  for k in range(0,2):
      for s in range(1,numberOfBits+1):
        sum = 0
        for i in range(1,s):
          sum+=(chromosome2[k][i]*(2**(-i)))
        chromosome2[k][s] = math.ceil(pnorm[k]-(2**(-s))-sum)
    
  return chromosome2

def decoding(chromosome, interval):
  chromosome2 = []
  lowerLimit = interval[0]
  upperLimit = interval[1]
  numberOfBits = len(chromosome[0])
  pnorm=[0,0]
  for i in range(0,2):
    for j in range(1,numberOfBits):
      pnorm[i]+=(chromosome[i][j]*(2**(-j))+2**(-numberOfBits))
    chromosome2.append(pnorm[i]*(upperLimit-lowerLimit)+lowerLimit)  
      
  return chromosome2

"""**Crossover**

Uniform crossover is used. For each position in the chromosome, the parent from which the bit is transcribed is randomly selected. The probability of selecting each chromosome for each bit is 0.5.
"""

def crossover(chromosome1,chromosome2):
  numberOfBits = len(chromosome1[0])-1
  chromosome3 = []
  chromosome4 = []
  chromosome3.append(generateChromosome(numberOfBits))
  chromosome3.append(generateChromosome(numberOfBits))
  chromosome4.append(generateChromosome(numberOfBits))
  chromosome4.append(generateChromosome(numberOfBits))

  for j in range(0,2):
    for i in range(1,numberOfBits+1): 
      if random.random()<=0.5:
        chromosome3[j][i] = chromosome1[j][i]
      else:
        chromosome3[j][i] = chromosome2[j][i]

  for j in range(0,2):
    for i in range(1,numberOfBits+1): 
      if random.random()<=0.5:
        chromosome4[j][i] = chromosome1[j][i]
      else:
        chromosome4[j][i] = chromosome2[j][i]    
  
  return chromosome3,chromosome4

"""**Mutation**

By random selection from the part of the population susceptible to mutation, based on the assigned probability, the bits to be mutated are selected. The bits are mutated by assigning them the opposite value.
"""

def mutation(chromosome, probability):
  length = len(chromosome[0])
  for j in range(0,2):
    for i in range(1,length):
      if random.random()<=probability:
        chromosome[j][i] = (chromosome[j][i]+1)%2
  return chromosome

"""**Test function for optimization**

The test function used is the Levi function no. 13. Its values are in the interval (-10.10), and its minimum in points 1 and 1 is 0.

"""

def test(gen):
  x = gen[0]
  y = gen[1]
  return ((math.sin(3*math.pi*x))**2) + ((x-1)**2)*(1+((math.sin(3*math.pi*y))**2)) + ((y-1)**2)*(1+((math.sin(2*math.pi*y))**2))

"""**Binary genetic algorithm**

The tournament selection algorithm is used. All chromosomes are given equal chances to participate in the competition. The winner of the competition is determined on the basis of the lowest cost and he is eligible for crossover.
"""

def genetic(numberOfBits,interval,mut_rat,populations,numberOfStarts,maxGenerations):
  
  def tournament(function, pop, number):
        z = []
        while len(z) < number:
            z.append(random.choice(pop))
        best = None
        best_f = None
        for e in z:
            ff = function(e)
            if best is None or ff < best_f:
               best_f = ff
               best = e
        return best
  
  

  test_size = 2
  
  for pop_size in populations:
    outfile = sys.stdout
    avg_cost = 0
    avg_iteration = 0
    best_ever_sol = None
    best_ever_f = None
    global_generation = []
    global_cost = []
    global_cost_avg = []
    print("Population size: " +str(pop_size))
    npop_size = pop_size
    for k in range(numberOfStarts):
        print('Starting: GA', mut_rat, k, file=outfile)
        best = None
        best_f = None
        t = 0
        list_generation = []
        list_cost= []
        list_avg = []
        pop = [[random.uniform(*interval) for i in range(test_size)] for j in range(pop_size)]
        while best_f != 0 and t < maxGenerations:
            list_avg_help = []
            n_pop = pop[:]
            while len(n_pop) < pop_size + npop_size:
                c1 = tournament(test, pop, 3)
                c2 = tournament(test, pop, 3)
                c1 = encoding(c1,interval,numberOfBits)
                c2 = encoding(c2,interval,numberOfBits)
                c3, c4 = crossover(c1, c2)
                c3 = mutation(c3, mut_rat)
                c4 = mutation(c4, mut_rat)
                c3 = decoding(c3,interval)
                c4 = decoding(c4,interval)
                n_pop.append(c3)
                n_pop.append(c4)
                list_avg_help.append(test(c3))
                list_avg_help.append(test(c4))
            pop = sorted(n_pop, key=lambda x : test(x))[:pop_size]
            f = test(pop[0])
            if best_f is None or best_f > f:
                best_f = f
                best = pop[0]
  #                    print(t, best_f, file=outfile)
            t += 1
            list_avg.append(sum(list_avg_help)/len(list_avg_help))
            list_generation.append(t)
            list_cost.append(f)
        global_generation.append(list_generation)
        global_cost.append(list_cost)
        global_cost_avg.append(list_avg)
        avg_cost += best_f
        avg_iteration += t
        # if we find a better one than the previous one, we update the best solution
        if best_ever_f is None or best_ever_f > best_f:
            best_ever_f = best_f
            best_ever_sol = best
        print(t, best, best_f, file=outfile)
  #                print(t, best, best_f)
      # at the end of all executions we calculate the average cost and the average number of iterations
    avg_cost /= numberOfStarts
    avg_iteration /= numberOfStarts
    print('Average cost: %g' % avg_cost, file=outfile)
    print('Average number of iterations: %.2f' % avg_iteration, file=outfile)
    print('Best result: %s' % best_ever_sol, file=outfile)
    print('Best result in bits: %s' % encoding(best_ever_sol,interval,numberOfBits), file=outfile)
    print('Best cost: %g' % best_ever_f, file=outfile)
    count = len(global_generation)
    for i in range(count):
      graph.plot(global_generation[i],global_cost[i],label = i)
    graph.xlabel('Generations')
    graph.ylabel('Best cost')
    graph.legend()  
    graph.show()
    for i in range(count):
      graph.plot(global_genera[i],global_cost_avg[i],label = i)
    graph.xlabel('Generations')
    graph.ylabel('Average cost')
    graph.legend()  
    graph.show()

"""**Setting parameters**"""

interval = [-10,10]
numberOfBits = 10
mutation_rate = 0.3
populations = [20,100,150]
numberOfStarts = 5
maxGenerations = 500
genetic(numberOfBits,interval,mutation_rate, populations,numberOfStarts,maxGenerations)
