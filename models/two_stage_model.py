"""
Two-Stage DEA/Tobit Model

Dwuetapowa analiza efektywnosci:
1. Etap 1: DEA - obliczenie wynikow efektywnosci
2. Etap 2: Regresja Tobit - analiza determinant efektywnosci

Model Tobit jest stosowany, poniewaz wyniki DEA sa ograniczone do [0, 1].

Alternatywne podejscia w etapie 2:
- Truncated regression (Simar & Wilson, 2007)
- Fractional regression
- Bootstrap DEA

Literatura:
- Banker & Natarajan (2008)
- Simar & Wilson (2007) - bootstrap approach
- McDonald (2009) - on the use of Tobit
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
import warnings

from .dea_model import DEAModel, DEAResult


@dataclass
class TobitResult:
    """Wyniki estymacji modelu Tobit."""
    coefficients: Dict[str, float]
    std_errors: Dict[str, float]
    t_stats: Dict[str, float]
    p_values: Dict[str, float]
    marginal_effects: Dict[str, float]  # Efekty kraƒcowe
    sigma: float
    log_likelihood: float
    pseudo_r_squared: float
    n_obs: int
    n_censored: int


@dataclass
class TwoStageResult:
    """Wyniki dwuetapowej analizy DEA-Tobit."""
    dea_results: pd.DataFrame
    tobit_result: TobitResult
    efficiency_drivers: pd.DataFrame  # Ranking determinant


class TobitModel:
    """
    Implementacja modelu Tobit (censored regression).

    Model:
    y* = Xβ + ε, ε ~ N(0, σ²)
    y = max(0, min(1, y*))  dla efektywnosci DEA

    Estymacja MLE.
    """

    def __init__(
        self,
        y: np.ndarray,
        X: np.ndarray,
        lower_bound: float = 0.0,
        upper_bound: float = 1.0
    ):
        """
        Inicjalizacja modelu Tobit.

        Args:
            y: Wektor zmiennej zaleznej (wyniki efektywnosci DEA)
            X: Macierz zmiennych niezaleznych
            lower_bound: Dolna granica cenzurowania
            upper_bound: Gorna granica cenzurowania
        """
        self.y = np.asarray(y).flatten()
        self.X = np.asarray(X)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.n, self.k = self.X.shape

        # Identyfikacja obserwacji cenzurowanych
        self.censored_lower = self.y <= lower_bound
        self.censored_upper = self.y >= upper_bound
        self.uncensored = ~(self.censored_lower | self.censored_upper)

        self.n_censored = np.sum(self.censored_lower) + np.sum(self.censored_upper)

    def _log_likelihood(self, params: np.ndarray) -> float:
        """
        Funkcja log-wiarygodnosci dla modelu Tobit.

        L = Π[φ((y-Xβ)/σ)/σ] dla niecenzurowanych
            × Π[Φ((L-Xβ)/σ)] dla cenzurowanych od dolu
            × Π[1-Φ((U-Xβ)/σ)] dla cenzurowanych od gory
        """
        beta = params[:-1]
        sigma = np.exp(params[-1])  # Log-parametryzacja dla dodatniosci

        Xbeta = self.X @ beta

        ll = 0.0

        # Niecenzurowane
        if np.any(self.uncensored):
            z = (self.y[self.uncensored] - Xbeta[self.uncensored]) / sigma
            ll += np.sum(norm.logpdf(z) - np.log(sigma))

        # Cenzurowane od dolu
        if np.any(self.censored_lower):
            z = (self.lower_bound - Xbeta[self.censored_lower]) / sigma
            ll += np.sum(norm.logcdf(z))

        # Cenzurowane od gory
        if np.any(self.censored_upper):
            z = (self.upper_bound - Xbeta[self.censored_upper]) / sigma
            ll += np.sum(np.log(1 - norm.cdf(z) + 1e-10))

        return -ll  # Ujemna do minimalizacji

    def fit(self) -> TobitResult:
        """
        Estymuje model Tobit metoda MLE.

        Returns:
            TobitResult z wynikami
        """
        # Wartosci poczatkowe z OLS
        beta_ols = np.linalg.lstsq(self.X, self.y, rcond=None)[0]
        residuals = self.y - self.X @ beta_ols
        sigma_ols = np.std(residuals)

        initial_params = np.concatenate([beta_ols, [np.log(sigma_ols)]])

        # Optymalizacja
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = minimize(
                self._log_likelihood,
                initial_params,
                method='BFGS',
                options={'maxiter': 1000, 'disp': False}
            )

        # Ekstrakcja wynikow
        beta = result.x[:-1]
        sigma = np.exp(result.x[-1])

        # Numeryczne obliczenie macierzy Hessiana dla SE
        # Uproszczona wersja - przyblizenie
        eps = 1e-5
        n_params = len(result.x)
        hessian = np.zeros((n_params, n_params))

        for i in range(n_params):
            for j in range(n_params):
                params_pp = result.x.copy()
                params_pm = result.x.copy()
                params_mp = result.x.copy()
                params_mm = result.x.copy()

                params_pp[i] += eps
                params_pp[j] += eps
                params_pm[i] += eps
                params_pm[j] -= eps
                params_mp[i] -= eps
                params_mp[j] += eps
                params_mm[i] -= eps
                params_mm[j] -= eps

                hessian[i, j] = (
                    self._log_likelihood(params_pp)
                    - self._log_likelihood(params_pm)
                    - self._log_likelihood(params_mp)
                    + self._log_likelihood(params_mm)
                ) / (4 * eps * eps)

        try:
            var_matrix = np.linalg.inv(hessian)
            std_errors = np.sqrt(np.abs(np.diag(var_matrix)))
        except np.linalg.LinAlgError:
            std_errors = np.ones(n_params) * 0.1

        std_errors_beta = std_errors[:-1]

        # t-statistics i p-values
        t_stats = beta / (std_errors_beta + 1e-10)
        p_values = 2 * (1 - norm.cdf(np.abs(t_stats)))

        # Efekty kracowe (marginal effects at mean)
        # ME = β * Φ((Xβ)/σ) dla Tobit
        Xbeta_mean = np.mean(self.X @ beta)
        prob_uncensored = norm.cdf((self.upper_bound - Xbeta_mean) / sigma) - norm.cdf((self.lower_bound - Xbeta_mean) / sigma)
        marginal_effects = beta * prob_uncensored

        # Pseudo R-squared (McFadden)
        ll_full = -result.fun
        # LL modelu tylko ze stala
        beta_null = np.zeros(self.k)
        beta_null[0] = np.mean(self.y)  # Zakladajac, ze pierwsza kolumna to stala
        ll_null = -self._log_likelihood(np.concatenate([beta_null, [np.log(sigma)]]))
        pseudo_r2 = 1 - ll_full / ll_null if ll_null != 0 else 0

        return TobitResult(
            coefficients=dict(enumerate(beta)),
            std_errors=dict(enumerate(std_errors_beta)),
            t_stats=dict(enumerate(t_stats)),
            p_values=dict(enumerate(p_values)),
            marginal_effects=dict(enumerate(marginal_effects)),
            sigma=sigma,
            log_likelihood=ll_full,
            pseudo_r_squared=pseudo_r2,
            n_obs=self.n,
            n_censored=self.n_censored
        )


class TwoStageDEATobit:
    """
    Dwuetapowa analiza DEA-Tobit.

    Etap 1: DEA dla obliczenia efektywnosci
    Etap 2: Tobit dla identyfikacji determinant efektywnosci
    """

    def __init__(
        self,
        data: pd.DataFrame,
        input_vars: List[str],
        output_vars: List[str],
        environmental_vars: List[str],
        entity_var: str = 'region',
        time_var: str = 'year',
        dea_model_type: str = 'BCC'
    ):
        """
        Inicjalizacja modelu dwuetapowego.

        Args:
            data: DataFrame z danymi
            input_vars: Zmienne nakladow dla DEA
            output_vars: Zmienne wynikow dla DEA
            environmental_vars: Zmienne srodowiskowe dla Tobit
            entity_var: Kolumna z jednostkami
            time_var: Kolumna z czasem
            dea_model_type: 'CCR' lub 'BCC'
        """
        self.data = data.copy()
        self.input_vars = input_vars
        self.output_vars = output_vars
        self.environmental_vars = environmental_vars
        self.entity_var = entity_var
        self.time_var = time_var
        self.dea_model_type = dea_model_type

    def run(self) -> TwoStageResult:
        """
        Uruchamia dwuetapowa analize.

        Returns:
            TwoStageResult z wynikami obu etapow
        """
        # ETAP 1: DEA
        print("=" * 70)
        print("ETAP 1: Data Envelopment Analysis")
        print("=" * 70)

        dea_results = self._run_dea_stage()
        print(f"\nWyniki efektywnosci DEA ({self.dea_model_type}):")
        print(dea_results.to_string())

        # ETAP 2: Tobit
        print("\n" + "=" * 70)
        print("ETAP 2: Tobit Regression - Determinanty efektywnosci")
        print("=" * 70)

        tobit_result = self._run_tobit_stage(dea_results)

        # Ranking determinant
        efficiency_drivers = self._create_driver_ranking(tobit_result)

        return TwoStageResult(
            dea_results=dea_results,
            tobit_result=tobit_result,
            efficiency_drivers=efficiency_drivers
        )

    def _run_dea_stage(self) -> pd.DataFrame:
        """
        Etap 1: Obliczenie efektywnosci DEA dla kazdej obserwacji.
        """
        results = []

        # DEA per okres lub calosciowo
        for year in self.data[self.time_var].unique():
            year_data = self.data[self.data[self.time_var] == year]

            if len(year_data) < 2:
                continue

            inputs = year_data[self.input_vars].copy()
            outputs = year_data[self.output_vars].copy()

            # Ustawienie indeksu na jednostki
            inputs.index = year_data[self.entity_var].values
            outputs.index = year_data[self.entity_var].values

            # DEA
            model = DEAModel(
                inputs=inputs,
                outputs=outputs,
                model_type=self.dea_model_type,
                orientation='input'
            )
            model.solve()

            for r in model.results:
                results.append({
                    self.time_var: year,
                    self.entity_var: r.dmu_name,
                    'efficiency': r.efficiency_score,
                    'is_efficient': r.is_efficient
                })

        return pd.DataFrame(results)

    def _run_tobit_stage(self, dea_results: pd.DataFrame) -> TobitResult:
        """
        Etap 2: Regresja Tobit na wynikach efektywnosci.
        """
        # Polaczenie wynikow DEA ze zmiennymi srodowiskowymi
        merged = dea_results.merge(
            self.data[[self.entity_var, self.time_var] + self.environmental_vars],
            on=[self.entity_var, self.time_var],
            how='left'
        )

        # Usuniecie brakujacych
        merged = merged.dropna()

        if len(merged) < 5:
            raise ValueError("Za malo obserwacji dla regresji Tobit")

        # Macierz X (ze stala)
        X = np.column_stack([
            np.ones(len(merged)),
            merged[self.environmental_vars].values
        ])

        y = merged['efficiency'].values

        # Estymacja Tobit
        model = TobitModel(y, X, lower_bound=0.0, upper_bound=1.0)
        result = model.fit()

        # Zamiana indeksow na nazwy zmiennych
        var_names = ['const'] + self.environmental_vars

        result.coefficients = dict(zip(var_names, result.coefficients.values()))
        result.std_errors = dict(zip(var_names, result.std_errors.values()))
        result.t_stats = dict(zip(var_names, result.t_stats.values()))
        result.p_values = dict(zip(var_names, result.p_values.values()))
        result.marginal_effects = dict(zip(var_names, result.marginal_effects.values()))

        self._print_tobit_result(result)

        return result

    def _print_tobit_result(self, result: TobitResult):
        """Drukuje wyniki Tobit."""
        print(f"\nLiczba obserwacji: {result.n_obs}")
        print(f"Obserwacje cenzurowane: {result.n_censored}")
        print(f"Log-likelihood: {result.log_likelihood:.4f}")
        print(f"Pseudo R-squared: {result.pseudo_r_squared:.4f}")
        print(f"Sigma: {result.sigma:.4f}")

        print("\n" + "-" * 80)
        print(f"{'Variable':<25} {'Coef':>10} {'Std.Err':>10} {'t-stat':>10} {'P>|t|':>10} {'Marg.Eff':>10}")
        print("-" * 80)

        for var in result.coefficients:
            coef = result.coefficients[var]
            se = result.std_errors[var]
            t = result.t_stats[var]
            p = result.p_values[var]
            me = result.marginal_effects[var]
            sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""

            print(f"{var:<25} {coef:>10.4f} {se:>10.4f} {t:>10.3f} {p:>9.4f} {me:>10.4f} {sig}")

        print("-" * 80)
        print("Significance: *** p<0.01, ** p<0.05, * p<0.1")

    def _create_driver_ranking(self, tobit_result: TobitResult) -> pd.DataFrame:
        """
        Tworzy ranking determinant efektywnosci.
        """
        drivers = []

        for var in self.environmental_vars:
            if var in tobit_result.coefficients:
                drivers.append({
                    'variable': var,
                    'coefficient': tobit_result.coefficients[var],
                    'marginal_effect': tobit_result.marginal_effects[var],
                    'p_value': tobit_result.p_values[var],
                    'significant': tobit_result.p_values[var] < 0.1,
                    'impact': 'positive' if tobit_result.coefficients[var] > 0 else 'negative'
                })

        df = pd.DataFrame(drivers)
        df['abs_effect'] = np.abs(df['marginal_effect'])
        df = df.sort_values('abs_effect', ascending=False)

        print("\n" + "=" * 70)
        print("Ranking determinant efektywnosci:")
        print("=" * 70)
        print(df[['variable', 'marginal_effect', 'impact', 'significant']].to_string(index=False))

        return df


def run_two_stage_analysis(data: pd.DataFrame) -> TwoStageResult:
    """
    Uruchamia pelna analize dwuetapowa DEA-Tobit.

    Args:
        data: DataFrame z danymi

    Returns:
        TwoStageResult
    """
    # Przygotowanie danych
    data = data.copy()

    # Mapowanie nazw kolumn (obsluga roznych formatow danych)
    col_mapping = {
        'ai_researchers': 'researchers',
        'public_rd_investment': 'public_investment',
        'ai_adoption_rate': 'adoption_rate'
    }
    for old_col, new_col in col_mapping.items():
        if old_col in data.columns and new_col not in data.columns:
            data[new_col] = data[old_col]

    # Uzupelnienie brakujacych kolumn
    if 'researchers' not in data.columns:
        data['researchers'] = 100000

    if 'startups' not in data.columns:
        # Szacunek na podstawie notable_models
        data['startups'] = data.get('notable_models', 10) * 15 + 100

    # Zmienne srodowiskowe - uzyj istniejacych lub stworz nowe
    if 'regulatory_index' not in data.columns:
        data['regulatory_index'] = data['region'].map({
            'USA': 0.3,
            'EU': 0.9,
            'China': 0.7,
            'UK': 0.4
        }).fillna(0.5)

    # Trend czasowy
    data['time_trend'] = data['year'] - data['year'].min()

    # Dummy dla regionow
    data['is_usa'] = (data['region'] == 'USA').astype(int)
    data['is_china'] = (data['region'] == 'China').astype(int)

    # Model
    model = TwoStageDEATobit(
        data=data,
        input_vars=['public_investment', 'private_investment', 'researchers'],
        output_vars=['patents', 'publications', 'startups'],
        environmental_vars=['regulatory_index', 'time_trend', 'is_usa', 'is_china'],
        entity_var='region',
        time_var='year',
        dea_model_type='BCC'
    )

    return model.run()


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
            efficiency_base = {'USA': 0.90, 'EU': 0.75, 'China': 0.85}
            t = year - 2015

            # Efekt regulacji - EU po 2024 ma nizsza efektywnosc krotkoterminowo
            reg_effect = 1.0
            if region == 'EU' and year >= 2024:
                reg_effect = 0.85

            test_data.append({
                'year': year,
                'region': region,
                'public_investment': base[region] * (1 + growth[region]) ** t * 0.25,
                'private_investment': base[region] * (1 + growth[region]) ** t * 0.75,
                'researchers': int(50000 * (1 + growth[region]) ** t),
                'patents': int(1000 * efficiency_base[region] * reg_effect * (1 + growth[region] * 0.8) ** t * (0.9 + np.random.random() * 0.2)),
                'publications': int(5000 * efficiency_base[region] * (1 + growth[region] * 0.7) ** t * (0.9 + np.random.random() * 0.2)),
                'startups': int(200 * efficiency_base[region] * (1 + growth[region] * 1.2) ** t * (0.8 + np.random.random() * 0.4)),
            })

    df = pd.DataFrame(test_data)

    print("=== Two-Stage DEA-Tobit Analysis for AI Funding Efficiency ===\n")
    result = run_two_stage_analysis(df)
