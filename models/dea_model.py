"""
Data Envelopment Analysis (DEA) Model

Nieparametryczna metoda oceny efektywnosci wzglednej jednostek decyzyjnych (DMU).
W kontekscie tego projektu: porownanie efektywnosci USA, UE i Chin w przeksztalcaniu
inwestycji AI na wyniki (patenty, publikacje, startupy, itd.).

Literatura:
- Charnes, Cooper, Rhodes (1978) - CCR Model
- Banker, Charnes, Cooper (1984) - BCC Model
"""

import numpy as np
from scipy.optimize import linprog
from dataclasses import dataclass
from typing import List, Dict, Optional
import pandas as pd


@dataclass
class DEAResult:
    """Wyniki analizy DEA dla pojedynczej jednostki."""
    dmu_name: str
    efficiency_score: float
    is_efficient: bool
    slack_inputs: np.ndarray
    slack_outputs: np.ndarray
    reference_set: List[str]  # Jednostki referencyjne dla nieefektywnych


class DEAModel:
    """
    Implementacja modelu DEA (Data Envelopment Analysis).

    Wspiera modele:
    - CCR (Constant Returns to Scale) - zaklada stale efekty skali
    - BCC (Variable Returns to Scale) - zaklada zmienne efekty skali

    Orientacja:
    - input: minimalizacja nakladow przy stalych wynikach
    - output: maksymalizacja wynikow przy stalych nakladach
    """

    def __init__(
        self,
        inputs: pd.DataFrame,
        outputs: pd.DataFrame,
        model_type: str = "CCR",
        orientation: str = "input"
    ):
        """
        Inicjalizacja modelu DEA.

        Args:
            inputs: DataFrame z nakladami (kolumny = zmienne, wiersze = DMU)
            outputs: DataFrame z wynikami
            model_type: "CCR" lub "BCC"
            orientation: "input" lub "output"
        """
        self.inputs = inputs.values
        self.outputs = outputs.values
        self.dmu_names = inputs.index.tolist()
        self.input_names = inputs.columns.tolist()
        self.output_names = outputs.columns.tolist()
        self.model_type = model_type
        self.orientation = orientation

        self.n_dmu = len(self.dmu_names)
        self.n_inputs = self.inputs.shape[1]
        self.n_outputs = self.outputs.shape[1]

        self.results: List[DEAResult] = []

    def solve(self) -> List[DEAResult]:
        """
        Rozwiazuje model DEA dla wszystkich jednostek.

        Returns:
            Lista wynikow DEA dla kazdej jednostki
        """
        self.results = []

        for i in range(self.n_dmu):
            if self.orientation == "input":
                result = self._solve_input_oriented(i)
            else:
                result = self._solve_output_oriented(i)
            self.results.append(result)

        return self.results

    def _solve_input_oriented(self, dmu_index: int) -> DEAResult:
        """
        Rozwiazuje model DEA zorientowany na nakłady dla pojedynczej DMU.

        Model CCR input-oriented:
        min θ
        s.t. Σ λ_j * x_ij <= θ * x_i0  (dla wszystkich i - inputs)
             Σ λ_j * y_rj >= y_r0      (dla wszystkich r - outputs)
             λ_j >= 0

        Model BCC dodaje: Σ λ_j = 1
        """
        x0 = self.inputs[dmu_index]
        y0 = self.outputs[dmu_index]

        # Zmienne: [theta, lambda_1, ..., lambda_n]
        n_vars = 1 + self.n_dmu

        # Funkcja celu: min theta
        c = np.zeros(n_vars)
        c[0] = 1

        # Ograniczenia nierownosci
        # Inputs: -theta * x_i0 + Σ λ_j * x_ij <= 0
        A_ub_inputs = np.zeros((self.n_inputs, n_vars))
        for i in range(self.n_inputs):
            A_ub_inputs[i, 0] = -x0[i]
            A_ub_inputs[i, 1:] = self.inputs[:, i]
        b_ub_inputs = np.zeros(self.n_inputs)

        # Outputs: -Σ λ_j * y_rj <= -y_r0
        A_ub_outputs = np.zeros((self.n_outputs, n_vars))
        for r in range(self.n_outputs):
            A_ub_outputs[r, 0] = 0
            A_ub_outputs[r, 1:] = -self.outputs[:, r]
        b_ub_outputs = -y0

        A_ub = np.vstack([A_ub_inputs, A_ub_outputs])
        b_ub = np.hstack([b_ub_inputs, b_ub_outputs])

        # Ograniczenia rownosci (BCC)
        A_eq = None
        b_eq = None
        if self.model_type == "BCC":
            A_eq = np.zeros((1, n_vars))
            A_eq[0, 1:] = 1
            b_eq = np.array([1.0])

        # Granice zmiennych
        bounds = [(0, None)] + [(0, None)] * self.n_dmu

        # Rozwiazanie
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                        bounds=bounds, method='highs')

        if result.success:
            theta = result.x[0]
            lambdas = result.x[1:]

            # Znajdz jednostki referencyjne
            reference_set = [
                self.dmu_names[j]
                for j in range(self.n_dmu)
                if lambdas[j] > 1e-6 and j != dmu_index
            ]

            return DEAResult(
                dmu_name=self.dmu_names[dmu_index],
                efficiency_score=theta,
                is_efficient=(theta >= 0.9999),
                slack_inputs=np.zeros(self.n_inputs),  # Uproszczone
                slack_outputs=np.zeros(self.n_outputs),
                reference_set=reference_set
            )
        else:
            return DEAResult(
                dmu_name=self.dmu_names[dmu_index],
                efficiency_score=np.nan,
                is_efficient=False,
                slack_inputs=np.zeros(self.n_inputs),
                slack_outputs=np.zeros(self.n_outputs),
                reference_set=[]
            )

    def _solve_output_oriented(self, dmu_index: int) -> DEAResult:
        """
        Rozwiazuje model DEA zorientowany na wyniki.

        Model CCR output-oriented:
        max φ
        s.t. Σ λ_j * x_ij <= x_i0      (dla wszystkich i - inputs)
             Σ λ_j * y_rj >= φ * y_r0  (dla wszystkich r - outputs)
             λ_j >= 0
        """
        x0 = self.inputs[dmu_index]
        y0 = self.outputs[dmu_index]

        # Zmienne: [phi, lambda_1, ..., lambda_n]
        n_vars = 1 + self.n_dmu

        # Funkcja celu: max phi => min -phi
        c = np.zeros(n_vars)
        c[0] = -1

        # Inputs: Σ λ_j * x_ij <= x_i0
        A_ub_inputs = np.zeros((self.n_inputs, n_vars))
        for i in range(self.n_inputs):
            A_ub_inputs[i, 0] = 0
            A_ub_inputs[i, 1:] = self.inputs[:, i]
        b_ub_inputs = x0

        # Outputs: -phi * y_r0 + Σ λ_j * y_rj >= 0 => phi * y_r0 - Σ λ_j * y_rj <= 0
        A_ub_outputs = np.zeros((self.n_outputs, n_vars))
        for r in range(self.n_outputs):
            A_ub_outputs[r, 0] = y0[r]
            A_ub_outputs[r, 1:] = -self.outputs[:, r]
        b_ub_outputs = np.zeros(self.n_outputs)

        A_ub = np.vstack([A_ub_inputs, A_ub_outputs])
        b_ub = np.hstack([b_ub_inputs, b_ub_outputs])

        # BCC constraint
        A_eq = None
        b_eq = None
        if self.model_type == "BCC":
            A_eq = np.zeros((1, n_vars))
            A_eq[0, 1:] = 1
            b_eq = np.array([1.0])

        bounds = [(1, None)] + [(0, None)] * self.n_dmu

        result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                        bounds=bounds, method='highs')

        if result.success:
            phi = result.x[0]
            lambdas = result.x[1:]

            reference_set = [
                self.dmu_names[j]
                for j in range(self.n_dmu)
                if lambdas[j] > 1e-6 and j != dmu_index
            ]

            # Efektywnosc = 1/phi dla orientacji output
            efficiency = 1 / phi if phi > 0 else np.nan

            return DEAResult(
                dmu_name=self.dmu_names[dmu_index],
                efficiency_score=efficiency,
                is_efficient=(phi <= 1.0001),
                slack_inputs=np.zeros(self.n_inputs),
                slack_outputs=np.zeros(self.n_outputs),
                reference_set=reference_set
            )
        else:
            return DEAResult(
                dmu_name=self.dmu_names[dmu_index],
                efficiency_score=np.nan,
                is_efficient=False,
                slack_inputs=np.zeros(self.n_inputs),
                slack_outputs=np.zeros(self.n_outputs),
                reference_set=[]
            )

    def get_efficiency_scores(self) -> pd.Series:
        """Zwraca wyniki efektywnosci jako Series."""
        if not self.results:
            self.solve()
        return pd.Series(
            {r.dmu_name: r.efficiency_score for r in self.results}
        )

    def get_summary(self) -> pd.DataFrame:
        """Zwraca podsumowanie wynikow."""
        if not self.results:
            self.solve()

        data = []
        for r in self.results:
            data.append({
                'DMU': r.dmu_name,
                'Efficiency': r.efficiency_score,
                'Efficient': r.is_efficient,
                'Reference Set': ', '.join(r.reference_set) if r.reference_set else '-'
            })

        return pd.DataFrame(data)


def run_dea_for_ai_funding(data: pd.DataFrame) -> pd.DataFrame:
    """
    Uruchamia analize DEA dla danych o finansowaniu AI.

    Args:
        data: DataFrame z kolumnami:
            - region: nazwa regionu (USA, EU, China)
            - year: rok
            - public_investment: inwestycje publiczne
            - private_investment: inwestycje prywatne
            - researchers: liczba badaczy AI
            - patents: liczba patentow
            - publications: liczba publikacji
            - startups: liczba startupow
            - adoption_rate: wskaznik adopcji AI

    Returns:
        DataFrame z wynikami efektywnosci dla kazdego regionu-roku
    """
    results = []

    # Grupowanie po latach dla porownania regionow w czasie
    for year in data['year'].unique():
        year_data = data[data['year'] == year].set_index('region')

        inputs = year_data[['public_investment', 'private_investment', 'researchers']]
        outputs = year_data[['patents', 'publications', 'startups', 'adoption_rate']]

        # Model CCR
        model_ccr = DEAModel(inputs, outputs, model_type="CCR", orientation="input")
        model_ccr.solve()

        # Model BCC
        model_bcc = DEAModel(inputs, outputs, model_type="BCC", orientation="input")
        model_bcc.solve()

        for ccr, bcc in zip(model_ccr.results, model_bcc.results):
            results.append({
                'year': year,
                'region': ccr.dmu_name,
                'efficiency_ccr': ccr.efficiency_score,
                'efficiency_bcc': bcc.efficiency_score,
                'scale_efficiency': ccr.efficiency_score / bcc.efficiency_score if bcc.efficiency_score > 0 else np.nan,
                'is_efficient_ccr': ccr.is_efficient,
                'is_efficient_bcc': bcc.is_efficient
            })

    return pd.DataFrame(results)


if __name__ == "__main__":
    # Przykladowe dane testowe
    np.random.seed(42)

    regions = ['USA', 'EU', 'China']
    years = range(2015, 2026)

    test_data = []
    for year in years:
        for region in regions:
            # Symulowane dane (do zastapienia rzeczywistymi)
            base_investment = {'USA': 100, 'EU': 50, 'China': 60}
            growth_rate = {'USA': 0.15, 'EU': 0.10, 'China': 0.25}

            years_from_start = year - 2015

            test_data.append({
                'year': year,
                'region': region,
                'public_investment': base_investment[region] * (1 + growth_rate[region]) ** years_from_start * (0.2 + np.random.random() * 0.1),
                'private_investment': base_investment[region] * (1 + growth_rate[region]) ** years_from_start * (0.8 + np.random.random() * 0.2),
                'researchers': int(50000 * (1 + growth_rate[region]) ** years_from_start * (0.8 + np.random.random() * 0.4)),
                'patents': int(1000 * (1 + growth_rate[region] * 0.8) ** years_from_start * (0.7 + np.random.random() * 0.6)),
                'publications': int(5000 * (1 + growth_rate[region] * 0.7) ** years_from_start * (0.8 + np.random.random() * 0.4)),
                'startups': int(200 * (1 + growth_rate[region] * 1.2) ** years_from_start * (0.6 + np.random.random() * 0.8)),
                'adoption_rate': min(0.9, 0.1 + 0.05 * years_from_start + np.random.random() * 0.1)
            })

    df = pd.DataFrame(test_data)

    print("=== DEA Analysis for AI Funding Efficiency ===\n")
    results = run_dea_for_ai_funding(df)
    print(results.to_string(index=False))
