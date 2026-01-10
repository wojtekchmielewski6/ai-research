"""
Difference-in-Differences (DiD) Model

Metoda ewaluacji wplywu polityk/interwencji poprzez porownanie
zmian w grupie traktowanej vs kontrolnej przed i po interwencji.

Model:
Y_it = α + β₁*Post_t + β₂*Treat_i + β₃*(Post_t × Treat_i) + ε_it

gdzie β₃ = efekt przyczynowy (ATT - Average Treatment Effect on Treated)

Zastosowanie w projekcie:
- Ocena wplywu regulacji AI (np. EU AI Act) na efektywnosc inwestycji
- Porownanie regionow przed/po wprowadzeniu kluczowych polityk

Literatura:
- Card & Krueger (1994)
- Angrist & Pischke (2009) - Mostly Harmless Econometrics
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from scipy import stats
import warnings


@dataclass
class DiDResult:
    """Wyniki estymacji modelu Difference-in-Differences."""
    att: float  # Average Treatment Effect on Treated (β₃)
    att_se: float
    att_t_stat: float
    att_p_value: float
    pre_trend_diff: float  # Roznica w trendach przed interwencja
    parallel_trends_test: Tuple[float, float]  # (statystyka, p-value)
    coefficients: Dict[str, float]
    std_errors: Dict[str, float]
    r_squared: float
    n_obs: int
    n_treated: int
    n_control: int


class DiDModel:
    """
    Implementacja modelu Difference-in-Differences.

    Wspiera:
    - Klasyczny DiD (2x2)
    - DiD z wieloma okresami
    - Event study design
    - DiD z kontrolami
    """

    def __init__(
        self,
        data: pd.DataFrame,
        outcome_var: str,
        time_var: str,
        entity_var: str,
        treatment_var: str,
        treatment_time: int,
        controls: Optional[List[str]] = None
    ):
        """
        Inicjalizacja modelu DiD.

        Args:
            data: DataFrame z danymi panelowymi
            outcome_var: Zmienna wynikowa
            time_var: Zmienna czasowa
            entity_var: Zmienna identyfikujaca jednostki
            treatment_var: Zmienna binarna (1 = jednostka traktowana)
            treatment_time: Okres wprowadzenia interwencji
            controls: Lista zmiennych kontrolnych (opcjonalnie)
        """
        self.data = data.copy()
        self.outcome_var = outcome_var
        self.time_var = time_var
        self.entity_var = entity_var
        self.treatment_var = treatment_var
        self.treatment_time = treatment_time
        self.controls = controls or []

        # Utworzenie zmiennych DiD
        self.data['post'] = (self.data[time_var] >= treatment_time).astype(int)
        self.data['treat'] = self.data[treatment_var]
        self.data['did'] = self.data['post'] * self.data['treat']

        self.n = len(self.data)
        self.n_treated = len(self.data[self.data['treat'] == 1])
        self.n_control = len(self.data[self.data['treat'] == 0])

    def fit(self) -> DiDResult:
        """
        Estymuje model DiD.

        Model: Y = α + β₁*Post + β₂*Treat + β₃*DiD + γ'X + ε

        Returns:
            DiDResult z wynikami estymacji
        """
        # Macierz X
        X_vars = ['post', 'treat', 'did'] + self.controls
        X = self.data[X_vars].values
        X = np.column_stack([np.ones(self.n), X])  # Dodanie stalej

        y = self.data[self.outcome_var].values

        # OLS
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        y_pred = X @ beta
        residuals = y - y_pred

        # R-squared
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - ss_res / ss_tot

        # Robust standard errors (clustered by entity)
        k = len(beta)
        df = self.n - k

        # Prosta estymacja SE (bez klastrowania - do rozbudowy)
        sigma2 = ss_res / df
        var_beta = sigma2 * np.linalg.inv(X.T @ X)
        std_errors = np.sqrt(np.diag(var_beta))

        # t-statistics i p-values
        t_stats = beta / std_errors
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df))

        # Nazwy zmiennych
        var_names = ['const', 'post', 'treat', 'did'] + self.controls

        # ATT (efekt interwencji)
        att = beta[3]  # Wspolczynnik przy 'did'
        att_se = std_errors[3]
        att_t_stat = t_stats[3]
        att_p_value = p_values[3]

        # Test parallel trends
        pre_trend_diff, parallel_test = self._test_parallel_trends()

        return DiDResult(
            att=att,
            att_se=att_se,
            att_t_stat=att_t_stat,
            att_p_value=att_p_value,
            pre_trend_diff=pre_trend_diff,
            parallel_trends_test=parallel_test,
            coefficients=dict(zip(var_names, beta)),
            std_errors=dict(zip(var_names, std_errors)),
            r_squared=r_squared,
            n_obs=self.n,
            n_treated=self.n_treated,
            n_control=self.n_control
        )

    def _test_parallel_trends(self) -> Tuple[float, Tuple[float, float]]:
        """
        Test rownoleglych trendow (parallel trends assumption).

        Porownuje trendy w grupach przed interwencja.
        """
        pre_data = self.data[self.data['post'] == 0]

        if len(pre_data) < 4:
            return 0.0, (0.0, 1.0)

        # Trend dla grupy traktowanej
        treated_pre = pre_data[pre_data['treat'] == 1]
        control_pre = pre_data[pre_data['treat'] == 0]

        if len(treated_pre) < 2 or len(control_pre) < 2:
            return 0.0, (0.0, 1.0)

        # Regresja trendu dla kazdej grupy
        def calc_trend(group_data):
            if len(group_data) < 2:
                return 0.0
            X = np.column_stack([
                np.ones(len(group_data)),
                group_data[self.time_var].values
            ])
            y = group_data[self.outcome_var].values
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
            return beta[1]  # Wspolczynnik przy czasie

        trend_treated = calc_trend(treated_pre)
        trend_control = calc_trend(control_pre)

        pre_trend_diff = trend_treated - trend_control

        # Uproszczony test (roznica trendow)
        # W praktyce: regresja z interakcja time*treat na danych pre-treatment
        # i test istotnosci wspolczynnika interakcji

        # Tutaj: prosty test t dla roznicy srednich zmian
        treated_changes = treated_pre.groupby(self.entity_var)[self.outcome_var].apply(
            lambda x: x.diff().mean()
        ).dropna()
        control_changes = control_pre.groupby(self.entity_var)[self.outcome_var].apply(
            lambda x: x.diff().mean()
        ).dropna()

        if len(treated_changes) > 0 and len(control_changes) > 0:
            t_stat, p_val = stats.ttest_ind(treated_changes, control_changes)
        else:
            t_stat, p_val = 0.0, 1.0

        return pre_trend_diff, (t_stat, p_val)

    def event_study(self, leads: int = 3, lags: int = 3) -> pd.DataFrame:
        """
        Event study - analiza efektow w czasie wzgledem interwencji.

        Tworzy wskazniki dla kazdego okresu wzgledem momentu interwencji
        i estymuje osobne efekty.

        Args:
            leads: Liczba okresow przed interwencja
            lags: Liczba okresow po interwencji

        Returns:
            DataFrame z efektami dla kazdego okresu
        """
        data = self.data.copy()

        # Czas wzgledny
        data['rel_time'] = data[self.time_var] - self.treatment_time

        # Ograniczenie do okna
        data = data[(data['rel_time'] >= -leads) & (data['rel_time'] <= lags)]

        # Tworzenie wskaznikow dla kazdego okresu (oprocz -1 jako referencji)
        event_dummies = []
        for t in range(-leads, lags + 1):
            if t != -1:  # -1 jako okres referencyjny
                col_name = f'rel_{t}'
                data[col_name] = ((data['rel_time'] == t) & (data['treat'] == 1)).astype(int)
                event_dummies.append(col_name)

        # Regresja
        X_vars = event_dummies + self.controls
        X = data[X_vars].values
        X = np.column_stack([np.ones(len(data)), X])

        y = data[self.outcome_var].values

        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        residuals = y - X @ beta

        # Standard errors
        df = len(data) - len(beta)
        sigma2 = np.sum(residuals**2) / df
        var_beta = sigma2 * np.linalg.inv(X.T @ X)
        std_errors = np.sqrt(np.diag(var_beta))

        # Wyniki
        results = []
        for i, t in enumerate(range(-leads, lags + 1)):
            if t == -1:
                # Okres referencyjny
                results.append({
                    'relative_time': t,
                    'coefficient': 0.0,
                    'std_error': 0.0,
                    'ci_lower': 0.0,
                    'ci_upper': 0.0
                })
            else:
                idx = i if t < -1 else i  # Indeks w beta (po stalej)
                coef = beta[idx + 1]
                se = std_errors[idx + 1]
                ci_lower = coef - 1.96 * se
                ci_upper = coef + 1.96 * se

                results.append({
                    'relative_time': t,
                    'coefficient': coef,
                    'std_error': se,
                    'ci_lower': ci_lower,
                    'ci_upper': ci_upper
                })

        return pd.DataFrame(results).sort_values('relative_time')


def print_did_result(result: DiDResult):
    """Drukuje wyniki modelu DiD."""
    print("=" * 70)
    print("Difference-in-Differences Results")
    print("=" * 70)
    print(f"Observations: {result.n_obs}")
    print(f"Treated units: {result.n_treated}")
    print(f"Control units: {result.n_control}")
    print(f"R-squared: {result.r_squared:.4f}")

    print("\n" + "-" * 70)
    print("Average Treatment Effect on Treated (ATT):")
    print("-" * 70)
    sig = "***" if result.att_p_value < 0.01 else "**" if result.att_p_value < 0.05 else "*" if result.att_p_value < 0.1 else ""
    print(f"  ATT: {result.att:.4f} {sig}")
    print(f"  Std. Error: {result.att_se:.4f}")
    print(f"  t-statistic: {result.att_t_stat:.3f}")
    print(f"  P-value: {result.att_p_value:.4f}")
    print(f"  95% CI: [{result.att - 1.96*result.att_se:.4f}, {result.att + 1.96*result.att_se:.4f}]")

    print("\n" + "-" * 70)
    print("Parallel Trends Test (Pre-treatment):")
    print("-" * 70)
    print(f"  Trend difference: {result.pre_trend_diff:.4f}")
    print(f"  Test statistic: {result.parallel_trends_test[0]:.3f}")
    print(f"  P-value: {result.parallel_trends_test[1]:.4f}")

    if result.parallel_trends_test[1] > 0.05:
        print("  -> Parallel trends assumption likely holds (p > 0.05)")
    else:
        print("  -> WARNING: Parallel trends may be violated (p < 0.05)")

    print("\n" + "-" * 70)
    print("Full Regression Coefficients:")
    print("-" * 70)
    print(f"{'Variable':<15} {'Coef':>12} {'Std.Err':>12}")
    print("-" * 40)
    for var in result.coefficients:
        print(f"{var:<15} {result.coefficients[var]:>12.4f} {result.std_errors[var]:>12.4f}")

    print("=" * 70)


def run_did_for_ai_policy(data: pd.DataFrame, policy_year: int, treated_region: str) -> DiDResult:
    """
    Uruchamia analize DiD dla oceny wplywu polityki AI.

    Przyklad: Ocena wplywu EU AI Act na efektywnosc inwestycji

    Args:
        data: DataFrame z danymi
        policy_year: Rok wprowadzenia polityki
        treated_region: Region objety polityka (np. 'EU')

    Returns:
        DiDResult z wynikami
    """
    data = data.copy()

    # Oznaczenie grupy traktowanej
    data['treated'] = (data['region'] == treated_region).astype(int)

    # Przygotowanie zmiennej wynikowej (efektywnosc jako patents/investment)
    data['efficiency'] = data['patents'] / (data['public_investment'] + data['private_investment'] + 0.01)

    # Model DiD
    model = DiDModel(
        data=data,
        outcome_var='efficiency',
        time_var='year',
        entity_var='region',
        treatment_var='treated',
        treatment_time=policy_year,
        controls=[]  # Mozna dodac kontrole
    )

    result = model.fit()
    print_did_result(result)

    return result


# Przyklad: Kluczowe polityki AI do analizy
AI_POLICY_EVENTS = {
    'EU': {
        2024: 'EU AI Act wejscie w zycie',
        2021: 'EU AI Act propozycja',
        2018: 'EU AI Strategy'
    },
    'USA': {
        2023: 'Executive Order on AI Safety',
        2020: 'National AI Initiative Act',
        2019: 'American AI Initiative'
    },
    'China': {
        2023: 'Generative AI Regulations',
        2021: 'AI Algorithm Regulations',
        2017: 'New Generation AI Development Plan'
    }
}


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

            # Symulacja efektu EU AI Act (2024) - spadek efektywnosci krotkoterminowo
            policy_effect = 0
            if region == 'EU' and year >= 2024:
                policy_effect = -0.1 * (year - 2023)  # Negatywny efekt regulacji

            efficiency_base = {'USA': 1.0, 'EU': 0.9, 'China': 0.95}[region]
            noise = np.random.randn() * 0.05

            test_data.append({
                'year': year,
                'region': region,
                'public_investment': base[region] * (1 + growth[region]) ** t * 0.25,
                'private_investment': base[region] * (1 + growth[region]) ** t * 0.75,
                'patents': int(1000 * efficiency_base * (1 + growth[region] * 0.8) ** t * (1 + policy_effect + noise)),
            })

    df = pd.DataFrame(test_data)

    print("=== DiD Analysis: Impact of EU AI Act ===\n")
    result = run_did_for_ai_policy(df, policy_year=2024, treated_region='EU')
