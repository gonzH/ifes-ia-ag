import random
import math

class Chromosome():
    """A individual
    """
    __individual_genotype_length = 16     # 16 genes
    __max_interval = 20.0
    __min_interval = -20.0
    
    def __init__(self, genotype = ''):
        self.genotype = genotype
        self.fenotype = 0  # this is x    
        self.fitness  = 0
    
    def __generate_genotype(self):
        """A Genotype represents the genetic composition of the organism, 
            that means that genotype is composed by genes, to represent it,
            we create symbolic genes to build a genotype which will be a 
            string of bits.
            
            A Genotype can not be modified once created.
        """
        if len(self.genotype) < self.__individual_genotype_length:
            gene = ''
            
            while len(self.genotype) < self.__individual_genotype_length:
                gene = str(random.randint(0,1))
            
                self.genotype = self.genotype + gene
            
    def __generate_fenotype(self):
        """A Fenotype represent the Genotype characteristics decodified
            into new characteristics. To represent it, we will submit the
            Genotype to a "decodification"/"normalization" equation.
        
            A Fenotype can be modified by influences such as the environment
        """
        
        """
        Equation:
            x = min + (((max - min) * genotype) / (2 ** genotype_length - 1))
        """
        
        self.fenotype = self.__min_interval +                                                           \
            (((self.__max_interval - self.__min_interval) * int(self.genotype, 2))                            \
            / (2 ** self.__individual_genotype_length - 1))
            
    def __calculate_fitness(self):
        """To assess the fitness of an individual we are going to subject
            him to an equation.
        """
        """
        Equation:
            f(fenotype) = cos(fenotype) * fenotype + 2
        """
        self.fitness = math.cos(self.fenotype) * self.fenotype + 2

    
    def generate_characteristics(self):
        """Just a pipeline in order to create a individual
        """
        self.__generate_genotype()
        self.__generate_fenotype()
        self.__calculate_fitness()
        
        return self
    
    def print(self):
        """[summary]
        """
        print("Genotype: {}\nFenotype: {}\nFitness: {} \n"\
            .format(self.genotype, self.fenotype, self.fitness))
    
    def get_genotype_length(self):
        return self.__individual_genotype_length
    
        
        
