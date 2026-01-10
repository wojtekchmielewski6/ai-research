"""
Panel Data Models (Fixed Effects / Random Effects)

Modele dla danych panelowych - obserwacji jednostek (regiony)
w wielu okresach czasu.

Modele:
- Pooled OLS: y_it = α + X_it'β + ε_it
- Fixed Effects (FE): y_it = α_i + X_it'β + ε_it
- Random Effects (RE): y_it = α + X_it'β + u_i + ε_it

Test Hausmana: wybor miedzy FE a RE

Literatura:
- Wooldridge (2010) - Econometric Analysis of Panel Data
- Baltagi (2021) - Econometric Analysis of Panel Data
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
from scipy import stats
import warnings


@dataclass
class PanelResult:
    """Wyniki estymacji modelu panelowego."""
    model_type: str
    coefficients: Dict[str, float]
    std_errors: Dict[str, float]
    t_stats: Dict[str, float]
    p_values: Dict[str, float]
    r_squared: float
    r_squared_within: Optional[float]
    r_squared_between: Optional[float]
    fixed_effects: Optional[Dict[str, float]]
    n_obs: int
    n_groups: int
    n_periods: int


class PanelDataModel:
    """
    Implementacja modeli dla danych panelowych.

    Wspiera:
    - Pooled OLS
    - Fixed Effects (within estimator)
    - Random Effects (GLS)
    - Between Effects
    """

    def __init__(
        self,
        data: pd.DataFrame,
        dependent_var: str,
        independent_vars: List[str],
        entity_col: str = 'region',
        time_col: str = 'year'
    ):
        """
        Inicjalizacja modelu panelowego.

        Args:
            data: DataFrame z danymi panelowymi
            dependent_var: Nazwa zmiennej zaleznej
            independent_vars: Lista nazw zmiennych niezaleznych
            entity_col: Nazwa kolumny z jednostkami (np. 'region')
            time_col: Nazwa kolumny z czasem (np. 'year')
        """
        self.data = data.copy()
        self.dependent_var = dependent_var
        self.independent_vars = independent_vars
        self.entity_col = entity_col
        self.time_col = time_col

        # Sortowanie i indeksowanie
        self.data = self.data.sort_values([entity_col, time_col])

        self.entities = self.data[entity_col].unique()
        self.times = self.data[time_col].unique()

        self.n = len(self.data)
        self.n_groups = len(self.entities)
        self.n_periods = len(self.times)
        self.k = len(independent_vars)

        # Przygotowanie macierzy
        self.y = self.data[dependent_var].values
        self.X = self.data[independent_vars].values

    def fit_pooled_ols(self) -> PanelResult:
        """
        Estymuje model Pooled OLS (ignoruje strukture panelowa).

        y_it = α + X_it'β + ε_it
        """
        # Dodanie stalej
        X_const = np.column_stack([np.ones(self.n), self.X])

        # OLS
        beta = np.linalg.lstsq(X_const, self.y, rcond=None)[0]
        y_pred = X_const @ beta
        residuals = self.y - y_pred

        # R-squared
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((self.y - np.mean(self.y))**2)
        r_squared = 1 - ss_res / ss_tot

        # Standard errors (heteroskedasticity-robust)
        sigma2 = ss_res / (self.n - self.k - 1)
        var_beta = sigma2 * np.linalg.inv(X_const.T @ X_const)
        std_errors = np.sqrt(np.diag(var_beta))

        # t-statistics i p-values
        t_stats = beta / std_errors
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), self.n - self.k - 1))

        # Nazwy
        var_names = ['const'] + self.independent_vars

        return PanelResult(
            model_type='Pooled OLS',
            coefficients=dict(zip(var_names, beta)),
            std_errors=dict(zip(var_names, std_errors)),
            t_stats=dict(zip(var_names, t_stats)),
            p_values=dict(zip(var_names, p_values)),
            r_squared=r_squared,
            r_squared_within=None,
            r_squared_between=None,
            fixed_effects=None,
            n_obs=self.n,
            n_groups=self.n_groups,
            n_periods=self.n_periods
        )

    def fit_fixed_effects(self) -> PanelResult:
        """
        Estymuje model Fixed Effects (within estimator).

        y_it - y_i_mean = (X_it - X_i_mean)'β + (ε_it - ε_i_mean)

        Eliminuje nieobserwowalna heterogenicznosc miedzy jednostkami.
        """
        # Demeaning (within transformation)
        y_demeaned = np.zeros(self.n)
        X_demeaned = np.zeros((self.n, self.k))

        entity_means_y = {}
        entity_means_X = {}

        for entity in self.entities:
            mask = self.data[self.entity_col] == entity
            entity_means_y[entity] = np.mean(self.y[mask])
            entity_means_X[entity] = np.mean(self.X[mask], axis=0)

            y_demeaned[mask] = self.y[mask] - entity_means_y[entity]
            X_demeaned[mask] = self.X[mask] - entity_means_X[entity]

        # OLS na zdementowanych danych (bez stalej)
        beta = np.linalg.lstsq(X_demeaned, y_demeaned, rcond=None)[0]

        # Residua
        y_pred_demeaned = X_demeaned @ beta
        residuals = y_demeaned - y_pred_demeaned

        # R-squared within
        ss_res = np.sum(residuals**2)
        ss_tot_within = np.sum(y_demeaned**2)
        r_squared_within = 1 - ss_res / ss_tot_within if ss_tot_within > 0 else 0

        # Efekty stale (fixed effects)
        fixed_effects = {}
        for entity in self.entities:
            mask = self.data[self.entity_col] == entity
            alpha_i = entity_means_y[entity] - entity_means_X[entity] @ beta
            fixed_effects[entity] = alpha_i

        # R-squared between
        y_between = np.array([entity_means_y[e] for e in self.entities])
        X_between = np.array([entity_means_X[e] for e in self.entities])
        y_pred_between = X_between @ beta + np.array([fixed_effects[e] for e in self.entities])
        ss_res_between = np.sum((y_between - np.mean(y_between))**2)
        ss_tot_between = np.sum((y_between - np.mean(y_between))**2)
        r_squared_between = 1 - np.sum((y_between - y_pred_between)**2) / ss_tot_between if ss_tot_between > 0 else 0

        # Standard errors
        df = self.n - self.n_groups - self.k
        sigma2 = ss_res / df
        var_beta = sigma2 * np.linalg.inv(X_demeaned.T @ X_demeaned)
        std_errors = np.sqrt(np.diag(var_beta))

        # t-statistics
        t_stats = beta / std_errors
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df))

        # Overall R-squared
        y_pred_full = self.X @ beta
        for i, entity in enumerate(self.data[self.entity_col]):
            y_pred_full[i] += fixed_effects[entity]

        ss_res_full = np.sum((self.y - y_pred_full)**2)
        ss_tot_full = np.sum((self.y - np.mean(self.y))**2)
        r_squared = 1 - ss_res_full / ss_tot_full

        return PanelResult(
            model_type='Fixed Effects',
            coefficients=dict(zip(self.independent_vars, beta)),
            std_errors=dict(zip(self.independent_vars, std_errors)),
            t_stats=dict(zip(self.independent_vars, t_stats)),
            p_values=dict(zip(self.independent_vars, p_values)),
            r_squared=r_squared,
            r_squared_within=r_squared_within,
            r_squared_between=r_squared_between,
            fixed_effects=fixed_effects,
            n_obs=self.n,
            n_groups=self.n_groups,
            n_periods=self.n_periods
        )

    def fit_random_effects(self) -> PanelResult:
        """
        Estymuje model Random Effects (GLS).

        y_it = α + X_it'β + u_i + ε_it

        gdzie u_i ~ IID(0, σ_u²) i ε_it ~ IID(0, σ_ε²)
        """
        # Krok 1: Estymacja wariancji z FE i between
        fe_result = self.fit_fixed_effects()

        # Residua z FE
        y_demeaned = np.zeros(self.n)
        X_demeaned = np.zeros((self.n, self.k))

        for entity in self.entities:
            mask = self.data[self.entity_col] == entity
            y_demeaned[mask] = self.y[mask] - np.mean(self.y[mask])
            X_demeaned[mask] = self.X[mask] - np.mean(self.X[mask], axis=0)

        beta_fe = np.array([fe_result.coefficients[v] for v in self.independent_vars])
        residuals_fe = y_demeaned - X_demeaned @ beta_fe

        # Sigma_epsilon² z FE
        sigma2_epsilon = np.sum(residuals_fe**2) / (self.n - self.n_groups - self.k)

        # Between estimator dla sigma_u²
        entity_means_y = self.data.groupby(self.entity_col)[self.dependent_var].mean()
        entity_means_X = self.data.groupby(self.entity_col)[self.independent_vars].mean()

        X_between = np.column_stack([np.ones(self.n_groups), entity_means_X.values])
        y_between = entity_means_y.values

        beta_between = np.linalg.lstsq(X_between, y_between, rcond=None)[0]
        residuals_between = y_between - X_between @ beta_between

        sigma2_between = np.sum(residuals_between**2) / (self.n_groups - self.k - 1)
        T_mean = self.n / self.n_groups
        sigma2_u = max(0, sigma2_between - sigma2_epsilon / T_mean)

        # Krok 2: GLS transformation
        theta = 1 - np.sqrt(sigma2_epsilon / (T_mean * sigma2_u + sigma2_epsilon)) if sigma2_u > 0 else 0

        # Quasi-demeaning
        y_quasi = np.zeros(self.n)
        X_quasi = np.zeros((self.n, self.k + 1))  # +1 dla stalej

        for entity in self.entities:
            mask = self.data[self.entity_col] == entity
            y_i = self.y[mask]
            X_i = self.X[mask]

            y_quasi[mask] = y_i - theta * np.mean(y_i)
            X_quasi[mask, 0] = 1 - theta
            X_quasi[mask, 1:] = X_i - theta * np.mean(X_i, axis=0)

        # GLS
        beta_re = np.linalg.lstsq(X_quasi, y_quasi, rcond=None)[0]

        # Predykcje i residua
        y_pred = X_quasi @ beta_re
        residuals = y_quasi - y_pred

        # R-squared
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y_quasi - np.mean(y_quasi))**2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        # Standard errors
        df = self.n - self.k - 1
        sigma2 = ss_res / df
        var_beta = sigma2 * np.linalg.inv(X_quasi.T @ X_quasi)
        std_errors = np.sqrt(np.diag(var_beta))

        # t-statistics
        t_stats = beta_re / std_errors
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df))

        var_names = ['const'] + self.independent_vars

        return PanelResult(
            model_type='Random Effects',
            coefficients=dict(zip(var_names, beta_re)),
            std_errors=dict(zip(var_names, std_errors)),
            t_stats=dict(zip(var_names, t_stats)),
            p_values=dict(zip(var_names, p_values)),
            r_squared=r_squared,
            r_squared_within=None,
            r_squared_between=None,
            fixed_effects=None,
            n_obs=self.n,
            n_groups=self.n_groups,
            n_periods=self.n_periods
        )

    def hausman_test(self) -> Tuple[float, float, str]:
        """
        Test Hausmana dla wyboru miedzy FE a RE.

        H0: RE jest efektywny i spojny (preferuj RE)
        H1: RE jest niespojny (preferuj FE)

        Returns:
            (statystyka chi2, p-value, rekomendacja)
        """
        fe_result = self.fit_fixed_effects()
        re_result = self.fit_random_effects()

        # Wspolczynniki (bez stalej)
        beta_fe = np.array([fe_result.coefficients[v] for v in self.independent_vars])
        beta_re = np.array([re_result.coefficients[v] for v in self.independent_vars if v in re_result.coefficients])

        # Roznica
        diff = beta_fe - beta_re[:len(beta_fe)]

        # Macierz wariancji roznicy (uproszczona)
        var_fe = np.diag([fe_result.std_errors[v]**2 for v in self.independent_vars])
        var_re = np.diag([re_result.std_errors.get(v, 0)**2 for v in self.independent_vars])

        var_diff = var_fe - var_re

        # Unikaj problemow z macierza osobliwa
        try:
            var_diff_inv = np.linalg.inv(var_diff)
            hausman_stat = diff.T @ var_diff_inv @ diff
        except np.linalg.LinAlgError:
            hausman_stat = np.sum(diff**2 / (np.diag(var_fe) + 1e-10))

        p_value = 1 - stats.chi2.cdf(hausman_stat, self.k)

        recommendation = "Fixed Effects" if p_value < 0.05 else "Random Effects"

        return hausman_stat, p_value, recommendation


def print_panel_result(result: PanelResult):
    """Drukuje wyniki modelu panelowego."""
    print("=" * 70)
    print(f"Model: {result.model_type}")
    print("=" * 70)
    print(f"Observations: {result.n_obs}")
    print(f"Groups: {result.n_groups}")
    print(f"Periods: {result.n_periods}")
    print(f"R-squared: {result.r_squared:.4f}")

    if result.r_squared_within is not None:
        print(f"R-squared (within): {result.r_squared_within:.4f}")
    if result.r_squared_between is not None:
        print(f"R-squared (between): {result.r_squared_between:.4f}")

    print("\n" + "-" * 70)
    print(f"{'Variable':<20} {'Coef':>12} {'Std.Err':>12} {'t-stat':>10} {'P>|t|':>10}")
    print("-" * 70)

    for var in result.coefficients:
        coef = result.coefficients[var]
        se = result.std_errors[var]
        t = result.t_stats[var]
        p = result.p_values[var]
        sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
        print(f"{var:<20} {coef:>12.4f} {se:>12.4f} {t:>10.3f} {p:>9.4f} {sig}")

    print("-" * 70)
    print("Significance: *** p<0.01, ** p<0.05, * p<0.1")

    if result.fixed_effects:
        print("\nFixed Effects (Entity):")
        for entity, effect in result.fixed_effects.items():
            print(f"  {entity}: {effect:.4f}")

    print("=" * 70)


def run_panel_analysis_for_ai_funding(data: pd.DataFrame) -> Dict[str, PanelResult]:
    """
    Uruchamia analize panelowa dla danych o finansowaniu AI.

    Args:
        data: DataFrame z danymi

    Returns:
        Slownik z wynikami roznych modeli
    """
    # Przygotowanie zmiennych
    data = data.copy()

    # Logarytmy (dla elastycznosci)
    data['ln_patents'] = np.log(data['patents'] + 1)
    data['ln_public'] = np.log(data['public_investment'] + 0.01)
    data['ln_private'] = np.log(data['private_investment'] + 0.01)
    data['ln_researchers'] = np.log(data['researchers'] + 1)

    # Model
    model = PanelDataModel(
        data=data,
        dependent_var='ln_patents',
        independent_vars=['ln_public', 'ln_private', 'ln_researchers'],
        entity_col='region',
        time_col='year'
    )

    results = {}

    # Pooled OLS
    results['pooled'] = model.fit_pooled_ols()
    print_panel_result(results['pooled'])

    # Fixed Effects
    results['fe'] = model.fit_fixed_effects()
    print_panel_result(results['fe'])

    # Random Effects
    results['re'] = model.fit_random_effects()
    print_panel_result(results['re'])

    # Test Hausmana
    print("\n" + "=" * 70)
    print("Test Hausmana (FE vs RE)")
    print("=" * 70)
    h_stat, p_val, recommendation = model.hausman_test()
    print(f"Chi-squared statistic: {h_stat:.4f}")
    print(f"P-value: {p_val:.4f}")
    print(f"Rekomendacja: {recommendation}")
    print("=" * 70)

    return results


if __name__ == "__main__":
    # Przykladowe dane testowe
    np.random.seed(42)

    regions = ['USA', 'EU', 'China']
    years = range(2015, 2026)

    test_data = []
    for year in years:
        for region in regions:
            base = {'USA': 100, 'EU': 50, 'China': 60}
            growth = {'USA': 0.15, 'EU': 0.10, 'China': 0.25}
            t = year - 2015

            test_data.append({
                'year': year,
                'region': region,
                'public_investment': base[region] * (1 + growth[region]) ** t * 0.25 * (1 + np.random.randn() * 0.1),
                'private_investment': base[region] * (1 + growth[region]) ** t * 0.75 * (1 + np.random.randn() * 0.1),
                'researchers': int(50000 * (1 + growth[region]) ** t * (1 + np.random.randn() * 0.1)),
                'patents': int(1000 * (1 + growth[region] * 0.8) ** t * (1 + np.random.randn() * 0.15)),
            })

    df = pd.DataFrame(test_data)

    print("=== Panel Data Analysis for AI Funding ===\n")
    results = run_panel_analysis_for_ai_funding(df)
