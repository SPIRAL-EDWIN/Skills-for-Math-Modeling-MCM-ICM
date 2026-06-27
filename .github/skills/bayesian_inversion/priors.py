"""
Prior distribution classes for Bayesian inference
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Union


class Prior(ABC):
    """Base class for prior distributions"""
    
    @abstractmethod
    def log_prob(self, theta: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Compute log probability: ln p(θ)
        
        Args:
            theta: Parameter value(s)
            
        Returns:
            Log probability
        """
        pass
    
    @abstractmethod
    def sample(self, n: int = 1) -> np.ndarray:
        """
        Draw random samples from prior
        
        Args:
            n: Number of samples
            
        Returns:
            Array of samples, shape (n,)
        """
        pass
    
    @abstractmethod
    def bounds(self) -> tuple:
        """
        Return (lower, upper) bounds for parameter
        Used for PSO initialization
        """
        pass


class UniformPrior(Prior):
    """
    Uniform (flat) prior: p(θ) ∝ 1 for θ ∈ [low, high]
    
    Example:
        >>> prior = UniformPrior(0.1, 1.0)
        >>> prior.log_prob(0.5)  # Returns 0.0
        >>> prior.log_prob(2.0)  # Returns -inf
    """
    
    def __init__(self, low: float, high: float):
        """
        Args:
            low: Lower bound
            high: Upper bound
        """
        assert low < high, f"low ({low}) must be < high ({high})"
        self.low = low
        self.high = high
        self._log_prob_value = -np.log(high - low)  # Normalize
    
    def log_prob(self, theta: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Log probability of uniform distribution"""
        in_bounds = (theta >= self.low) & (theta <= self.high)
        
        if np.isscalar(theta):
            return self._log_prob_value if in_bounds else -np.inf
        else:
            result = np.full_like(theta, -np.inf, dtype=float)
            result[in_bounds] = self._log_prob_value
            return result
    
    def sample(self, n: int = 1) -> np.ndarray:
        """Draw uniform samples"""
        return np.random.uniform(self.low, self.high, size=n)
    
    def bounds(self) -> tuple:
        """Return bounds"""
        return (self.low, self.high)
    
    def __repr__(self):
        return f"UniformPrior({self.low}, {self.high})"


class GaussianPrior(Prior):
    """
    Gaussian (normal) prior: p(θ) ∝ exp(-0.5 * ((θ - μ) / σ)²)
    
    Example:
        >>> prior = GaussianPrior(mu=0.5, sigma=0.1)
        >>> prior.log_prob(0.5)  # Returns ~0.0 (peak at mean)
    """
    
    def __init__(self, mu: float, sigma: float, bounds: tuple = None):
        """
        Args:
            mu: Mean
            sigma: Standard deviation
            bounds: Optional (low, high) bounds for truncation
        """
        assert sigma > 0, f"sigma ({sigma}) must be > 0"
        self.mu = mu
        self.sigma = sigma
        self._bounds = bounds if bounds else (-np.inf, np.inf)
        
        # Normalization constant (ignoring truncation for simplicity)
        self._log_norm = -0.5 * np.log(2 * np.pi * sigma**2)
    
    def log_prob(self, theta: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Log probability of Gaussian"""
        log_p = self._log_norm - 0.5 * ((theta - self.mu) / self.sigma)**2
        
        # Apply bounds if specified
        if self._bounds != (-np.inf, np.inf):
            in_bounds = (theta >= self._bounds[0]) & (theta <= self._bounds[1])
            if np.isscalar(theta):
                return log_p if in_bounds else -np.inf
            else:
                log_p[~in_bounds] = -np.inf
        
        return log_p
    
    def sample(self, n: int = 1) -> np.ndarray:
        """Draw Gaussian samples (with rejection if bounded)"""
        if self._bounds == (-np.inf, np.inf):
            return np.random.normal(self.mu, self.sigma, size=n)
        else:
            # Rejection sampling for truncated Gaussian
            samples = []
            while len(samples) < n:
                candidate = np.random.normal(self.mu, self.sigma)
                if self._bounds[0] <= candidate <= self._bounds[1]:
                    samples.append(candidate)
            return np.array(samples)
    
    def bounds(self) -> tuple:
        """Return bounds (use 3-sigma if unbounded)"""
        if self._bounds != (-np.inf, np.inf):
            return self._bounds
        else:
            return (self.mu - 3*self.sigma, self.mu + 3*self.sigma)
    
    def __repr__(self):
        return f"GaussianPrior(mu={self.mu}, sigma={self.sigma})"


class LogUniformPrior(Prior):
    """
    Log-uniform prior: p(θ) ∝ 1/θ for θ ∈ [low, high]
    Useful for scale parameters that span orders of magnitude
    
    Example:
        >>> prior = LogUniformPrior(1e-10, 1e-6)  # For wear coefficient
        >>> prior.sample(10)  # Samples uniformly in log-space
    """
    
    def __init__(self, low: float, high: float):
        """
        Args:
            low: Lower bound (must be > 0)
            high: Upper bound
        """
        assert 0 < low < high, f"Need 0 < low ({low}) < high ({high})"
        self.low = low
        self.high = high
        self.log_low = np.log(low)
        self.log_high = np.log(high)
        self._log_norm = -np.log(np.log(high / low))
    
    def log_prob(self, theta: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Log probability: ln(1/θ) + normalization"""
        in_bounds = (theta >= self.low) & (theta <= self.high)
        
        if np.isscalar(theta):
            if not in_bounds:
                return -np.inf
            return self._log_norm - np.log(theta)
        else:
            result = np.full_like(theta, -np.inf, dtype=float)
            result[in_bounds] = self._log_norm - np.log(theta[in_bounds])
            return result
    
    def sample(self, n: int = 1) -> np.ndarray:
        """Draw samples uniform in log-space"""
        log_samples = np.random.uniform(self.log_low, self.log_high, size=n)
        return np.exp(log_samples)
    
    def bounds(self) -> tuple:
        """Return bounds"""
        return (self.low, self.high)
    
    def __repr__(self):
        return f"LogUniformPrior({self.low}, {self.high})"


class MultivariatePrior:
    """
    Container for multiple independent priors
    
    Example:
        >>> priors = MultivariatePrior({
        ...     'alpha': LogUniformPrior(1e-10, 1e-8),
        ...     'N': UniformPrior(100, 1000),
        ...     'T': UniformPrior(50, 200)
        ... })
        >>> theta = {'alpha': 5e-9, 'N': 500, 'T': 100}
        >>> priors.log_prob(theta)
    """
    
    def __init__(self, priors: dict):
        """
        Args:
            priors: Dictionary mapping parameter names to Prior objects
        """
        self.priors = priors
        self.param_names = list(priors.keys())
    
    def log_prob(self, theta: dict) -> float:
        """
        Compute joint log probability (assuming independence):
        ln p(θ) = Σ ln p(θ_i)
        
        Args:
            theta: Dictionary of parameter values
            
        Returns:
            Sum of log probabilities
        """
        return sum(
            self.priors[name].log_prob(theta[name])
            for name in self.param_names
        )
    
    def sample(self, n: int = 1) -> dict:
        """
        Draw samples from joint prior
        
        Returns:
            Dictionary of parameter arrays, each shape (n,)
        """
        return {
            name: self.priors[name].sample(n)
            for name in self.param_names
        }
    
    def bounds(self) -> dict:
        """Return bounds for all parameters"""
        return {
            name: self.priors[name].bounds()
            for name in self.param_names
        }
    
    def __repr__(self):
        items = ', '.join(f"{k}: {v}" for k, v in self.priors.items())
        return f"MultivariatePrior({{{items}}})"
