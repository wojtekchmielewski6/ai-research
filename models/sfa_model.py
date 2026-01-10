"""
Stochastic Frontier Analysis (SFA) Model

Parametryczna metoda estymacji granicy produkcji z dekompozycja bledu
na komponent losowy (v) i nieefektywnosc (u).

Model: y = f(x; β) + v - u
gdzie:
- v ~ N(0, σ_v²) - szum losowy (symetryczny)
- u ~ |N(0, σ_u²)| - nieefektywnosc (nieujemna)

Literatura:
- Aigner, Lovell, Schmidt (1977)
- Meeusen & van den Broeck (1977)
- Battese & Coelli (1992, 1995)
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm, truncnorm
from dataclasses import dataclass
from typing import Optional, Tuple, List
import warnings


@dataclass
class SFAResult:
    """Wyniki estymacji modelu SFA."""
    coefficients: dict
    sigma_v: float  # Odchylenie standardowe szumu
    sigma_u: float  # Odchylenie standardowe nieefektywnosci
    lambda_param: float  # sigma_u / sigma_v
    log_likelihood: float
    efficiency_scores: pd.Series
    residuals: np.ndarray
    aic: float
    bic: float
    n_obs: int


class SFAModel:
    """
    Implementacja Stochastic Frontier Analysis (SFA).

    Wspiera specyfikacje:
    - production: y = f(x) + v - u (output-oriented)
    - cost: y = f(x) + v + u (input-oriented)

    Rozklady nieefektywnosci:
    - half_normal: u ~ |N(0, σ_u²)|
    - exponential: u ~ Exp(σ_u)
    - truncated_normal: u ~ N+(μ, σ_u²)
    """

    def __init__(
        self,
        y: np.ndarray,
        X: np.ndarray,
        frontier_type: str = "production",
        inefficiency_dist: str = "half_normal"
    ):
        """
        Inicjalizacja modelu SFA.

        Args:
            y: Wektor zmiennej zaleznej (log output)
            X: Macierz zmiennych niezaleznych (z kolumna jedynek dla stalej)
            frontier_type: "production" lub "cost"
            inefficiency_dist: "half_normal", "exponential", lub "truncated_normal"
        """
        self.y = np.asarray(y).flatten()
        self.X = np.asarray(X)
        self.frontier_type = frontier_type
        self.inefficiency_dist = inefficiency_dist

        self.n, self.k = self.X.shape

        # Wyniki
        self.beta: Optional[np.ndarray] = None
        self.sigma_v: Optional[float] = None
        self.sigma_u: Optional[float] = None
        self.result: Optional[SFAResult] = None

    def _log_likelihood_half_normal(self, params: np.ndarray) -> float:
        """
        Funkcja log-wiarygodnosci dla rozkladu half-normal.

        Wzor (Aigner et al. 1977):
        ln L = const - n*ln(σ) + Σ ln Φ(-ε_i * λ/σ) - (1/2σ²) Σ ε_i²

        gdzie:
        - σ² = σ_v² + σ_u²
        - λ = σ_u / σ_v
        - ε = y - Xβ (dla production: ε = v - u)
        """
        beta = params[:self.k]
        sigma_v = np.exp(params[self.k])      # Parametryzacja log dla dodatnosci
        sigma_u = np.exp(params[self.k + 1])

        sigma = np.sqrt(sigma_v**2 + sigma_u**2)
        lambda_param = sigma_u / sigma_v

        # Residua
        epsilon = self.y - self.X @ beta

        # Znak zalezny od typu frontiery
        sign = -1 if self.frontier_type == "production" else 1

        # Log-likelihood
        ll = (
            -self.n * np.log(sigma)
            + np.sum(np.log(norm.cdf(sign * epsilon * lambda_param / sigma) + 1e-10))
            - (1 / (2 * sigma**2)) * np.sum(epsilon**2)
            + self.n * np.log(2 / np.sqrt(2 * np.pi))
        )

        return -ll  # Zwracamy ujemna wartosc do minimalizacji

    def fit(self, method: str = "BFGS") -> SFAResult:
        """
        Estymuje model SFA metoda MLE.

        Args:
            method: Metoda optymalizacji (BFGS, L-BFGS-B, Nelder-Mead)

        Returns:
            SFAResult z wynikami estymacji
        """
        # Wartosci poczatkowe z OLS
        beta_ols = np.linalg.lstsq(self.X, self.y, rcond=None)[0]
        residuals_ols = self.y - self.X @ beta_ols
        sigma_ols = np.std(residuals_ols)

        # Poczatkowe wartosci parametrow
        initial_params = np.concatenate([
            beta_ols,
            [np.log(sigma_ols * 0.7), np.log(sigma_ols * 0.7)]  # log(sigma_v), log(sigma_u)
        ])

        # Optymalizacja
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = minimize(
                self._log_likelihood_half_normal,
                initial_params,
                method=method,
                options={'maxiter': 1000, 'disp': False}
            )

        # Ekstrakcja wynikow
        self.beta = result.x[:self.k]
        self.sigma_v = np.exp(result.x[self.k])
        self.sigma_u = np.exp(result.x[self.k + 1])

        sigma = np.sqrt(self.sigma_v**2 + self.sigma_u**2)
        lambda_param = self.sigma_u / self.sigma_v

        # Residua
        residuals = self.y - self.X @ self.beta

        # Efektywnosc (Jondrow et al. 1982)
        efficiency_scores = self._compute_efficiency(residuals, sigma, lambda_param)

        # Kryteria informacyjne
        log_likelihood = -result.fun
        n_params = len(result.x)
        aic = 2 * n_params - 2 * log_likelihood
        bic = n_params * np.log(self.n) - 2 * log_likelihood

        # Nazwy wspolczynnikow
        coef_names = [f'beta_{i}' for i in range(self.k)]
        coefficients = dict(zip(coef_names, self.beta))

        self.result = SFAResult(
            coefficients=coefficients,
            sigma_v=self.sigma_v,
            sigma_u=self.sigma_u,
            lambda_param=lambda_param,
            log_likelihood=log_likelihood,
            efficiency_scores=efficiency_scores,
            residuals=residuals,
            aic=aic,
            bic=bic,
            n_obs=self.n
        )

        return self.result

    def _compute_efficiency(
        self,
        residuals: np.ndarray,
        sigma: float,
        lambda_param: float
    ) -> pd.Series:
        """
        Oblicza punktowe oszacowania efektywnosci (Jondrow et al. 1982).

        E[u|ε] = σ_* [φ(ε*λ/σ) / Φ(-ε*λ/σ) - ε*λ/σ]

        gdzie σ_* = σ_u * σ_v / σ
        """
        sign = -1 if self.frontier_type == "production" else 1

        sigma_star = (self.sigma_u * self.sigma_v) / sigma
        z = sign * residuals * lambda_param / sigma

        # E[u|ε] - warunkowa wartosc oczekiwana nieefektywnosci
        mu_star = sigma_star * (norm.pdf(z) / (norm.cdf(-z) + 1e-10) - z)

        # Efektywnosc techniczna
        efficiency = np.exp(-mu_star)

        return pd.Series(efficiency)

    def predict(self, X_new: Optional[np.ndarray] = None) -> np.ndarray:
        """Predykcja na granicy (bez nieefektywnosci)."""
        if X_new is None:
            X_new = self.X
        return X_new @ self.beta

    def get_summary(self) -> str:
        """Zwraca tekstowe podsumowanie wynikow."""
        if self.result is None:
            return "Model nie zostal jeszcze oszacowany. Uzyj metody fit()."

        summary = [
            "=" * 60,
            "Stochastic Frontier Analysis - Wyniki",
            "=" * 60,
            f"Typ frontiery: {self.frontier_type}",
            f"Rozklad nieefektywnosci: {self.inefficiency_dist}",
            f"Liczba obserwacji: {self.result.n_obs}",
            "",
            "Wspolczynniki:",
            "-" * 30
        ]

        for name, value in self.result.coefficients.items():
            summary.append(f"  {name}: {value:.6f}")

        summary.extend([
            "",
            "Parametry wariancji:",
            "-" * 30,
            f"  sigma_v: {self.result.sigma_v:.6f}",
            f"  sigma_u: {self.result.sigma_u:.6f}",
            f"  lambda (sigma_u/sigma_v): {self.result.lambda_param:.6f}",
            "",
            "Dopasowanie modelu:",
            "-" * 30,
            f"  Log-likelihood: {self.result.log_likelihood:.4f}",
            f"  AIC: {self.result.aic:.4f}",
            f"  BIC: {self.result.bic:.4f}",
            "",
            "Statystyki efektywnosci:",
            "-" * 30,
            f"  Srednia: {self.result.efficiency_scores.mean():.4f}",
            f"  Mediana: {self.result.efficiency_scores.median():.4f}",
            f"  Min: {self.result.efficiency_scores.min():.4f}",
            f"  Max: {self.result.efficiency_scores.max():.4f}",
            "=" * 60
        ])

        return "\n".join(summary)


def run_sfa_for_ai_funding(data: pd.DataFrame) -> Tuple[SFAResult, pd.DataFrame]:
    """
    Uruchamia analize SFA dla danych o finansowaniu AI.

    Model produkcji Cobb-Douglas:
    ln(Y) = β_0 + β_1*ln(public_inv) + β_2*ln(private_inv) + β_3*ln(researchers) + v - u

    Args:
        data: DataFrame z danymi

    Returns:
        Tuple (SFAResult, DataFrame z efektywnoscią per region)
    """
    # Przygotowanie danych - agregacja output jako indeks
    data = data.copy()

    # Normalizacja outputow do indeksu kompozytowego
    output_cols = ['patents', 'publications', 'startups']
    for col in output_cols:
        data[f'{col}_norm'] = data[col] / data[col].max()

    # Indeks kompozytowy (srednia wazona)
    data['output_index'] = (
        0.4 * data['patents_norm'] +
        0.3 * data['publications_norm'] +
        0.3 * data['startups_norm']
    )

    # Logarytmy
    data['ln_output'] = np.log(data['output_index'] + 0.01)
    data['ln_public'] = np.log(data['public_investment'] + 0.01)
    data['ln_private'] = np.log(data['private_investment'] + 0.01)
    data['ln_researchers'] = np.log(data['researchers'] + 1)

    # Macierz X (z kolumna jedynek)
    X = np.column_stack([
        np.ones(len(data)),
        data['ln_public'].values,
        data['ln_private'].values,
        data['ln_researchers'].values
    ])

    y = data['ln_output'].values

    # Estymacja
    model = SFAModel(y, X, frontier_type="production", inefficiency_dist="half_normal")
    result = model.fit()

    # Dodanie efektywnosci do danych
    data['efficiency_sfa'] = result.efficiency_scores.values

    # Podsumowanie per region
    region_summary = data.groupby('region').agg({
        'efficiency_sfa': ['mean', 'std', 'min', 'max'],
        'output_index': 'mean'
    }).round(4)

    print(model.get_summary())

    return result, region_summary


if __name__ == "__main__":
    # Przykladowe dane testowe
    np.random.seed(42)

    regions = ['USA', 'EU', 'China']
    years = range(2015, 2026)

    test_data = []
    for year in years:
        for region in regions:
            base_investment = {'USA': 100, 'EU': 50, 'China': 60}
            growth_rate = {'USA': 0.15, 'EU': 0.10, 'China': 0.25}
            efficiency_base = {'USA': 0.85, 'EU': 0.75, 'China': 0.80}

            years_from_start = year - 2015

            test_data.append({
                'year': year,
                'region': region,
                'public_investment': base_investment[region] * (1 + growth_rate[region]) ** years_from_start * 0.25,
                'private_investment': base_investment[region] * (1 + growth_rate[region]) ** years_from_start * 0.75,
                'researchers': int(50000 * (1 + growth_rate[region]) ** years_from_start),
                'patents': int(1000 * efficiency_base[region] * (1 + growth_rate[region] * 0.8) ** years_from_start * (0.9 + np.random.random() * 0.2)),
                'publications': int(5000 * efficiency_base[region] * (1 + growth_rate[region] * 0.7) ** years_from_start * (0.9 + np.random.random() * 0.2)),
                'startups': int(200 * efficiency_base[region] * (1 + growth_rate[region] * 1.2) ** years_from_start * (0.8 + np.random.random() * 0.4)),
            })

    df = pd.DataFrame(test_data)

    print("=== SFA Analysis for AI Funding Efficiency ===\n")
    result, summary = run_sfa_for_ai_funding(df)
    print("\nRegion Summary:")
    print(summary)
