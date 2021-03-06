import numpy
from termcolor import colored

class PointSource:
    def __init__(self, alpha):
        # watch out for missing ',' in arrays
        disp = 0.01
        i_alpha = 1e-1
        self.alpha = alpha
        self.r = [
            [0.1, 0.34],
            [0.1, -0.34],
            [0.17, 0.37],
            [0.17, -0.37],
            [0.4, 0.37],
            [0.4, -0.37],
            [0.53, 0.185],
            [0.53, -0.185]
        ] #array of vector point sources position 
        self.i_disp = [
            [-0, disp],
            [-0, disp],
            [-3910, disp],
            [-3910, disp],
            [-6260, disp],
            [-6260, disp],
            [-530, disp],
            [-530, disp]
        ] #array of [current of the point source, characteristic decay distance]
        
        poor_input = (numpy.shape(self.r) != numpy.shape(self.i_disp)) # check if you input all
        #data concerning each point source
        
        if poor_input:
            print(colored("WARNING! Size of self.r and self.i_disp arrays are not the same!\n", 'red'))
        