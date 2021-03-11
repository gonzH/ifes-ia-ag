import math
import copy
import random
from chromosome import Chromosome
import csv
from statistics import mean

def write_csv(filename, population, generation):
    """Write generations results in a csv file

    Args:
        filename (string): name of the file to be created
        population (list): A list of individuals AKA population
        generation (int): identifier of the current generation
    """
    with open(filename + '.csv', mode='a', newline='') as f:
        f = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        if generation == 0:
            fields = ['generation']
            [fields.append('indiv-' + str(i)) for i in range(len(population))]
            fields.append('mean')
            f.writerow(fields)
        
        population_fitness = [generation]
        mean_fitness = 0
        for individual in population:
            population_fitness.append('{0:.4f}'.format(individual.fitness))
            mean_fitness = mean_fitness + individual.fitness
        
        mean_fitness = mean_fitness / len(population)
        population_fitness.append('{0:.4f}'.format(mean_fitness))
        
        f.writerow(population_fitness)
            

def elitism(population):
    """Select the best individual of the population
        by evaluating each one fitness

    Args:
        population (list): A list of individuals AKA population

    Returns:
        Chromosome: The best individual
    """
    
    elite_individual = max((individual.fitness, i) for i, individual in enumerate(population))[1]
    elite_individual = population[elite_individual]
    
    return copy.deepcopy(elite_individual)

def elitism_perk(population, elite_individual):
    """Replaces the worst fitness individual of the population by
       the previously selected elite individual

    Args:
        population (list): A list of individuals AKA population
        elite_individual (Chromosome): A individual selected as the best individual of his population

    Returns:
        population (list): The individuals list with thre worst individual replaced by the best
    """
    
    lowest_fitness_individual_index = min((individual.fitness, i) for i, individual in enumerate(population))[1]
    population[lowest_fitness_individual_index] = elite_individual
    
    return population


def tournament(population, n, k = 75):
    """A selection method that chooses n individuals at random to
       dispute between them in order to determine who is the best 
       individual.

    Args:
        population (list): A list of individuals AKA population
        n (int): number of individuals per dispute

    Returns:
        list: a list of the tournament winners
    """
    
    tournament_winners = []
    
    for round in range(len(population)):
        # Chooses n unique random individual from the population
        tournament_key = random.sample(population, n)
        
        r = random.randint(1,100)
        if r < k:
            # The best individual is choosen
            if tournament_key[0].fitness > tournament_key[1].fitness:
                tournament_winners.append(tournament_key[0])
            else:
                tournament_winners.append(tournament_key[1])
        else:
            # The worst individual is choosen
            if tournament_key[0].fitness > tournament_key[1].fitness:
                tournament_winners.append(tournament_key[1])
            else:
                tournament_winners.append(tournament_key[0])
    
    return tournament_winners

def crossover(population, threshold):
    """Within a certain threshold, individuals cross their genes
       in order to create a different individual made by a slice
       of fathers randomly choosed index of genotype

    Args:
        population (list): A list of individuals AKA population
        threshold (float): A limit for determining whether a crossover should take place

    Raises:
        Exception: Sorry, population must be even

    Returns:
        list: The cross population (if it happened)
    """
    
    if len(population) % 2 != 0:
        raise Exception("Sorry, population must be even")
        
    crop_limit = Chromosome().get_genotype_length() - 1
    
    for i in range(0, len(population), 2):
        father1, father2 = population[i], population[i+1]
        
        r = random.randint(1,100)
        if r <= threshold:
            crop = random.randint(1, crop_limit)
            
            # Crossing genes
            son1_gene = father1.genotype[crop:] + father2.genotype[:crop]
            son2_gene = father2.genotype[crop:] + father1.genotype[:crop]
            
            # Create a individual with a custom gene but no fenotype and fitness
            population[i] = Chromosome(son1_gene)
            population[i+1] = Chromosome(son2_gene)

    return population

def mutation(population, chance):
    """With a certain chance, when a mutation occurs a gene
       get inverted

    Args:
        population (list): A list of individuals AKA population
        chance (float): A chance to the mutation occurs

    Returns:
        list: The mutated population (if it happened)
    """
    for individual in population:
        for i, gene in enumerate(individual.genotype):
            r = random.randint(1, 100)
            
            if r <= chance:
                if gene == '0':
                    temp = list(individual.genotype)
                    temp[i] = '1'
                    individual.genotype = "".join(temp)
                else:
                    temp = list(individual.genotype)
                    temp[i] = '0'
                    individual.genotype = "".join(temp)
    
    return population


def genetic_algorithm(num_individuals = 10, generations = 10, crossover_threshold = 60, mutation_chance = 1):
    """The genetic algorithm flow

    Args:
        num_individuals (int, optional): Number of individuals/Total population. Defaults to 10.
        generations (int, optional): Number of generations. Defaults to 10.
        crossover_threshold (int, optional): A limit for determining whether a crossover should take place. Defaults to 60%.
        mutation_chance (int, optional): A chance to the mutation occurs. Defaults to 1%.

    Returns:
        Chromosome: The best individual
    """
    filename = str(num_individuals) + 'individuals' + str(generations) + 'generations'
    
    # Step 1) Generate the initial population
    # Step 2) Inside of Chromosome class there is a function to calculate the fitness of each one
    population = [Chromosome().generate_characteristics() for _ in range(num_individuals)]
    
    # Step 3) While we don't hit the stop criteria, wich we are covering just the generation limit
    for generation in range(generations):
        write_csv(filename, population, generation)
        
        # Step 3.1) Select the most fitness individual
        individual_with_the_best_fitness = elitism(population)
        population = tournament(population, 2)
        
        # Step 3.2) Create new individuals applying Crossover and Mutation
        population = crossover(population, crossover_threshold)
        population = mutation(population, mutation_chance)
        
        # Step 3.3) Revamp population with the new individuals
        # Step 3.4) Assesses each individual 
        population = [Chromosome(individual.genotype).generate_characteristics() for individual in population]
        population = elitism_perk(population, individual_with_the_best_fitness)
    
    print('The best individual details:')
    return elitism(population)