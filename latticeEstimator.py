############## you need the folder 'estimator' in the same directory as this script
############## download this folder from https://github.com/malb/lattice-estimator

from estimator import *

#### set the parameters here
# reference: https://lattice-estimator.readthedocs.io/en/latest/_apidoc/estimator.lwe_parameters/estimator.lwe_parameters.LWEParameters.html#estimator.lwe_parameters.LWEParameters
n = 1024
sigma = 3
q = 2**32


params_lwe = LWE.Parameters(n=n, q=q, Xs=ND.Uniform(-q//2, q//2), Xe=ND.DiscreteGaussian(sigma))

LWE.estimate(params_lwe, jobs=6)