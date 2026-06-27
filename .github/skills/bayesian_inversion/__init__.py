"""
Bayesian Parameter Inversion Skill

A reusable framework for inverting model parameters from observed data.
Implements O-award winning approaches from MCM 2025 Problem A.
"""

from .core import BayesianInverter, InversionResult
from .priors import Prior, UniformPrior, GaussianPrior, LogUniformPrior

__version__ = "1.0.0"
__all__ = [
    "BayesianInverter",
    "InversionResult",
    "Prior",
    "UniformPrior",
    "GaussianPrior",
    "LogUniformPrior",
]
