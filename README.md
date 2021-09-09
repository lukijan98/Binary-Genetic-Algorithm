# Binary Genetic Algorithm
Homework for class "Genetic Algorithms" at Računarski fakultet



## Encoding and decoding functions
The normalization function is used for encoding and decoding. The values of the variables are scaled to the interval (0, 1). The function is then used to convert to binary value.

## Crossover
Uniform crossover is used. For each position in the chromosome, the parent from which the bit is transcribed is randomly selected. The probability of selecting each chromosome for each bit is 0.5.

## Mutation
By random selection from the part of the population susceptible to mutation, based on the assigned probability, the bits to be mutated are selected. The bits are mutated by assigning them the opposite value.

## Test function for optimization
The [test function](https://en.wikipedia.org/wiki/Test_functions_for_optimization) used is the Levi function no. 13. Its values are in the interval (-10.10), and its minimum in points 1 and 1 is 0.\
![Plot](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Levi_function_13.pdf/page1-800px-Levi_function_13.pdf.jpg)\
![Formula1](https://wikimedia.org/api/rest_v1/media/math/render/svg/34c3c75a8c0b0a1bcb07f31501f208d56aa20587)![Formula2](https://wikimedia.org/api/rest_v1/media/math/render/svg/ea61c2670922e5564125165b769f9a6abcca209e)

## Genetic algorithm
The tournament selection algorithm is used. All chromosomes are given equal chances to participate in the competition. The winner of the competition is determined on the basis of the lowest cost and he is eligible for crossover.

## Note:
Google Colab was used for running the script.
