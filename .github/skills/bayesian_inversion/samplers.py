"""
MCMC samplers for Bayesian posterior inference
"""

import numpy as np
from typing import Callable, Dict, Tuple
from .priors import MultivariatePrior


class MetropolisHastingsSampler:
    """
    Metropolis-Hastings MCMC sampler
    
    Samples from posterior distribution p(θ | data) using random walk proposals.
    Based on Paper 2504218 implementation.
    
    Algorithm:
        1. Initialize at θ^(0)
        2. For s = 1, ..., S:
            a. Propose θ' ~ N(θ^(s-1), Σ)
            b. Compute acceptance ratio: A = min(1, p(θ')/p(θ^(s-1)))
            c. Accept θ^(s) = θ' with probability A, else θ^(s) = θ^(s-1)
        3. Return samples after burn-in
    
    Example:
        >>> def log_posterior(theta):
        ...     # Gaussian posterior centered at [1, 2]
        ...     return -0.5 * ((theta['x'] - 1)**2 + (theta['y'] - 2)**2)
        >>> 
        >>> sampler = MetropolisHastingsSampler(
        ...     log_posterior_fn=log_posterior,
        ...     priors=priors,
        ...     initial_state={'x': 0, 'y': 0}
        ... )
        >>> samples, diag = sampler.sample(n_samples=5000, n_burnin=1000)
    """
    
    def __init__(
        self,
        log_posterior_fn: Callable[[Dict[str, float]], float],
        priors: MultivariatePrior,
        initial_state: Dict[str, float]
    ):
        """
        Initialize MCMC sampler
        
        Args:
            log_posterior_fn: Function computing ln p(θ | data)
            priors: Prior distributions (for bounds checking)
            initial_state: Starting point θ^(0)
        """
        self.log_posterior_fn = log_posterior_fn
        self.priors = priors
        self.param_names = priors.param_names
        self.n_params = len(self.param_names)
        
        # Convert initial state to array
        self.current_state = np.array([
            initial_state[param] for param in self.param_names
        ])
        self.current_log_prob = log_posterior_fn(initial_state)
        
        # Get parameter scales from prior bounds (for adaptive step size)
        bounds = priors.bounds()
        self.param_scales = np.array([
            bounds[param][1] - bounds[param][0]
            for param in self.param_names
        ])
    
    def sample(
        self,
        n_samples: int = 5000,
        n_burnin: int = 1000,
        step_size: float = 0.01,
        n_chains: int = 1,
        adapt_step: bool = True,
        target_accept: float = 0.234  # Optimal for Gaussian targets
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, float]]:
        """
        Run Metropolis-Hastings sampling
        
        Args:
            n_samples: Number of samples to draw (after burn-in)
            n_burnin: Number of burn-in samples to discard
            step_size: Proposal step size (fraction of parameter range)
            n_chains: Number of independent chains (for R-hat diagnostic)
            adapt_step: Adapt step size during burn-in to hit target_accept
            target_accept: Target acceptance rate (0.234 for Gaussian)
            
        Returns:
            (samples, diagnostics):
                samples: Dict of parameter arrays, each shape (n_samples,)
                diagnostics: Dict with 'accept_rate', 'rhat' (if n_chains > 1)
        """
        if n_chains == 1:
            return self._sample_single_chain(
                n_samples, n_burnin, step_size, adapt_step, target_accept
            )
        else:
            return self._sample_multiple_chains(
                n_samples, n_burnin, step_size, n_chains, adapt_step, target_accept
            )
    
    def _sample_single_chain(
        self,
        n_samples: int,
        n_burnin: int,
        step_size: float,
        adapt_step: bool,
        target_accept: float
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, float]]:
        """Run single MCMC chain"""
        
        total_samples = n_samples + n_burnin
        samples = np.zeros((total_samples, self.n_params))
        log_probs = np.zeros(total_samples)
        
        n_accepted = 0
        current_step_size = step_size
        
        for i in range(total_samples):
            # Propose new state: θ' ~ N(θ, step_size² * Σ)
            proposal_cov = (current_step_size * self.param_scales)**2
            proposal_state = self.current_state + np.random.randn(self.n_params) * np.sqrt(proposal_cov)
            
            # Convert to dict for evaluation
            proposal_dict = {
                param: proposal_state[j]
                for j, param in enumerate(self.param_names)
            }
            
            # Evaluate log posterior
            proposal_log_prob = self.log_posterior_fn(proposal_dict)
            
            # Compute acceptance ratio (in log space)
            log_accept_ratio = proposal_log_prob - self.current_log_prob
            
            # Accept/reject
            if np.log(np.random.rand()) < log_accept_ratio:
                # Accept
                self.current_state = proposal_state
                self.current_log_prob = proposal_log_prob
                n_accepted += 1
            
            # Store sample
            samples[i] = self.current_state
            log_probs[i] = self.current_log_prob
            
            # Adapt step size during burn-in
            if adapt_step and i < n_burnin and i % 100 == 0 and i > 0:
                accept_rate = n_accepted / (i + 1)
                if accept_rate > target_accept:
                    current_step_size *= 1.1  # Increase step size
                else:
                    current_step_size *= 0.9  # Decrease step size
        
        # Discard burn-in
        samples = samples[n_burnin:]
        log_probs = log_probs[n_burnin:]
        
        # Convert to dict
        samples_dict = {
            param: samples[:, i]
            for i, param in enumerate(self.param_names)
        }
        
        # Compute diagnostics
        accept_rate = n_accepted / total_samples
        diagnostics = {
            'accept_rate': accept_rate,
            'ess': self._effective_sample_size(samples),
            'final_step_size': current_step_size
        }
        
        return samples_dict, diagnostics
    
    def _sample_multiple_chains(
        self,
        n_samples: int,
        n_burnin: int,
        step_size: float,
        n_chains: int,
        adapt_step: bool,
        target_accept: float
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, float]]:
        """
        Run multiple independent chains and compute R-hat convergence diagnostic
        """
        all_chains = []
        accept_rates = []
        
        for chain_id in range(n_chains):
            # Perturb initial state for each chain
            perturbed_initial = self.current_state + 0.1 * self.param_scales * np.random.randn(self.n_params)
            perturbed_dict = {
                param: perturbed_initial[i]
                for i, param in enumerate(self.param_names)
            }
            
            # Create new sampler for this chain
            chain_sampler = MetropolisHastingsSampler(
                self.log_posterior_fn,
                self.priors,
                perturbed_dict
            )
            
            # Run chain
            samples, diag = chain_sampler._sample_single_chain(
                n_samples, n_burnin, step_size, adapt_step, target_accept
            )
            
            all_chains.append(samples)
            accept_rates.append(diag['accept_rate'])
        
        # Combine chains
        combined_samples = {
            param: np.concatenate([chain[param] for chain in all_chains])
            for param in self.param_names
        }
        
        # Compute R-hat for each parameter
        rhat_values = {}
        for param in self.param_names:
            chain_arrays = np.array([chain[param] for chain in all_chains])
            rhat_values[param] = self._compute_rhat(chain_arrays)
        
        diagnostics = {
            'accept_rate': np.mean(accept_rates),
            'rhat': rhat_values,
            'rhat_max': max(rhat_values.values())
        }
        
        return combined_samples, diagnostics
    
    @staticmethod
    def _effective_sample_size(samples: np.ndarray) -> float:
        """
        Compute effective sample size using autocorrelation
        
        ESS ≈ N / (1 + 2 Σ ρ_k) where ρ_k is autocorrelation at lag k
        """
        n, d = samples.shape
        
        # Compute autocorrelation for each dimension
        ess_per_dim = []
        for i in range(d):
            x = samples[:, i]
            x_centered = x - np.mean(x)
            
            # Compute autocorrelation
            autocorr = np.correlate(x_centered, x_centered, mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            autocorr = autocorr / autocorr[0]
            
            # Sum until autocorrelation becomes small
            max_lag = min(n // 2, 100)
            autocorr_sum = 1.0 + 2 * np.sum(autocorr[1:max_lag])
            
            ess_per_dim.append(n / autocorr_sum)
        
        return np.min(ess_per_dim)  # Return worst-case ESS
    
    @staticmethod
    def _compute_rhat(chains: np.ndarray) -> float:
        """
        Compute Gelman-Rubin R-hat convergence diagnostic
        
        R-hat ≈ 1 indicates convergence
        R-hat > 1.1 indicates chains have not converged
        
        Args:
            chains: Array shape (n_chains, n_samples)
            
        Returns:
            R-hat value
        """
        n_chains, n_samples = chains.shape
        
        # Between-chain variance
        chain_means = np.mean(chains, axis=1)
        overall_mean = np.mean(chain_means)
        B = n_samples * np.var(chain_means, ddof=1)
        
        # Within-chain variance
        chain_vars = np.var(chains, axis=1, ddof=1)
        W = np.mean(chain_vars)
        
        # Pooled variance estimate
        var_plus = ((n_samples - 1) * W + B) / n_samples
        
        # R-hat
        rhat = np.sqrt(var_plus / W) if W > 0 else 1.0
        
        return rhat
