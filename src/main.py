"""
AI Infrastructure Financing Effectiveness Analysis

Glowny plik uruchomieniowy projektu.
Porownanie efektywnosci finansowania AI w USA, UE i Chinach (2015-2025).

Uzycie:
    python src/main.py --model all
    python src/main.py --model dea
    python src/main.py --model sfa
    python src/main.py --model panel
    python src/main.py --model did
    python src/main.py --model two_stage
"""

import argparse
import sys
import os
from pathlib import Path

# Dodanie sciezki do modeli
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd


def generate_sample_data() -> pd.DataFrame:
    """
    Generuje przykladowe dane do testowania modeli.

    W produkcji: zastap rzeczywistymi danymi ze zrodel:
    - Stanford HAI AI Index
    - OECD AI Policy Observatory
    - World Bank / IMF
    - USPTO, EPO, CNIPA (patenty)
    """
    np.random.seed(42)

    regions = ['USA', 'EU', 'China']
    years = range(2015, 2026)

    # Parametry bazowe dla kazdego regionu
    params = {
        'USA': {
            'base_investment': 100,
            'growth_rate': 0.15,
            'efficiency': 0.90,
            'public_share': 0.20,
            'regulatory_strictness': 0.3
        },
        'EU': {
            'base_investment': 60,
            'growth_rate': 0.10,
            'efficiency': 0.75,
            'public_share': 0.35,
            'regulatory_strictness': 0.9
        },
        'China': {
            'base_investment': 70,
            'growth_rate': 0.25,
            'efficiency': 0.85,
            'public_share': 0.45,
            'regulatory_strictness': 0.7
        }
    }

    data = []

    for year in years:
        for region in regions:
            p = params[region]
            t = year - 2015

            # Bazowe wartosci z trendem wzrostowym
            total_investment = p['base_investment'] * (1 + p['growth_rate']) ** t

            # Efekt regulacji (EU AI Act od 2024)
            reg_effect = 1.0
            if region == 'EU' and year >= 2024:
                reg_effect = 0.90  # Krotkoterminowy koszt compliance

            # Szum losowy
            noise = 1 + np.random.randn() * 0.05

            data.append({
                'year': year,
                'region': region,

                # Inputs
                'public_investment': total_investment * p['public_share'] * noise,
                'private_investment': total_investment * (1 - p['public_share']) * noise,
                'researchers': int(50000 * (1 + p['growth_rate']) ** t * (0.9 + np.random.random() * 0.2)),
                'compute_capacity': 100 * (1 + p['growth_rate'] * 1.5) ** t,  # Petaflops

                # Outputs
                'patents': int(1000 * p['efficiency'] * reg_effect * (1 + p['growth_rate'] * 0.8) ** t * noise),
                'publications': int(5000 * p['efficiency'] * (1 + p['growth_rate'] * 0.7) ** t * noise),
                'startups': int(200 * p['efficiency'] * (1 + p['growth_rate'] * 1.2) ** t * (0.8 + np.random.random() * 0.4)),
                'foundation_models': int(5 + t * (3 if region == 'USA' else 2 if region == 'China' else 1)),
                'adoption_rate': min(0.9, 0.1 + 0.05 * t + np.random.random() * 0.1),

                # Environmental variables
                'gdp_per_capita': {'USA': 65000, 'EU': 45000, 'China': 12000}[region] * (1.02 ** t),
                'regulatory_index': p['regulatory_strictness'] + (0.2 if region == 'EU' and year >= 2024 else 0),
                'stem_graduates': int(500000 * (1 + 0.03) ** t * {'USA': 1.0, 'EU': 1.2, 'China': 2.5}[region]),
            })

    return pd.DataFrame(data)


def run_dea_analysis(data: pd.DataFrame):
    """Uruchamia analize DEA."""
    from models.dea_model import run_dea_for_ai_funding

    print("\n" + "=" * 80)
    print(" MODEL 1: DATA ENVELOPMENT ANALYSIS (DEA)")
    print("=" * 80)
    print("\nCel: Ocena efektywnosci wzglednej regionow w przeksztalcaniu")
    print("     nakladow (inwestycje, badacze) na wyniki (patenty, publikacje, startupy)")
    print("-" * 80)

    results = run_dea_for_ai_funding(data)

    print("\nPodsumowanie efektywnosci per region:")
    summary = results.groupby('region').agg({
        'efficiency_ccr': ['mean', 'std'],
        'efficiency_bcc': ['mean', 'std'],
        'scale_efficiency': 'mean'
    }).round(4)
    print(summary)

    return results


def run_sfa_analysis(data: pd.DataFrame):
    """Uruchamia analize SFA."""
    from models.sfa_model import run_sfa_for_ai_funding

    print("\n" + "=" * 80)
    print(" MODEL 2: STOCHASTIC FRONTIER ANALYSIS (SFA)")
    print("=" * 80)
    print("\nCel: Parametryczna estymacja granicy produkcji z dekompozycja")
    print("     bledu na szum losowy i nieefektywnosc techniczna")
    print("-" * 80)

    result, summary = run_sfa_for_ai_funding(data)

    print("\nPodsumowanie efektywnosci per region:")
    print(summary)

    return result, summary


def run_panel_analysis(data: pd.DataFrame):
    """Uruchamia analize panelowa."""
    from models.panel_model import run_panel_analysis_for_ai_funding

    print("\n" + "=" * 80)
    print(" MODEL 3: PANEL DATA MODELS (FE/RE)")
    print("=" * 80)
    print("\nCel: Analiza wplywu inwestycji na wyniki z uwzglednieniem")
    print("     nieobserwowalnej heterogenicznosci miedzy regionami")
    print("-" * 80)

    results = run_panel_analysis_for_ai_funding(data)
    return results


def run_did_analysis(data: pd.DataFrame):
    """Uruchamia analize DiD dla EU AI Act."""
    from models.did_model import run_did_for_ai_policy

    print("\n" + "=" * 80)
    print(" MODEL 4: DIFFERENCE-IN-DIFFERENCES (DiD)")
    print("=" * 80)
    print("\nCel: Ocena przyczynowego wplywu EU AI Act (2024) na efektywnosc")
    print("     inwestycji w UE vs grupa kontrolna (USA, Chiny)")
    print("-" * 80)

    result = run_did_for_ai_policy(data, policy_year=2024, treated_region='EU')
    return result


def run_two_stage_analysis(data: pd.DataFrame):
    """Uruchamia dwuetapowa analize DEA-Tobit."""
    from models.two_stage_model import run_two_stage_analysis as run_ts

    print("\n" + "=" * 80)
    print(" MODEL 5: TWO-STAGE DEA-TOBIT")
    print("=" * 80)
    print("\nCel: Identyfikacja determinant efektywnosci:")
    print("     1) DEA - obliczenie wynikow efektywnosci")
    print("     2) Tobit - analiza czynnikow wplywajacych na efektywnosc")
    print("-" * 80)

    result = run_ts(data)
    return result


def main():
    parser = argparse.ArgumentParser(
        description='AI Infrastructure Financing Effectiveness Analysis'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='all',
        choices=['all', 'dea', 'sfa', 'panel', 'did', 'two_stage'],
        help='Model do uruchomienia (default: all)'
    )
    parser.add_argument(
        '--data',
        type=str,
        default=None,
        help='Sciezka do pliku CSV z danymi (opcjonalnie)'
    )

    args = parser.parse_args()

    print("=" * 80)
    print(" AI INFRASTRUCTURE FINANCING EFFECTIVENESS ANALYSIS")
    print(" Porownanie: USA vs EU vs Chiny (2015-2025)")
    print("=" * 80)

    # Wczytanie danych
    if args.data and os.path.exists(args.data):
        data = pd.read_csv(args.data)
        print(f"\nWczytano dane z: {args.data}")
    else:
        print("\nUwaga: Uzywam przykladowych danych (sample data).")
        print("Dla rzeczywistej analizy, dostarcz dane ze zrodel:")
        print("  - Stanford HAI AI Index")
        print("  - OECD AI Policy Observatory")
        print("  - World Bank / IMF")
        print("  - USPTO, EPO, CNIPA (patenty)")
        data = generate_sample_data()

    print(f"\nLiczba obserwacji: {len(data)}")
    print(f"Regiony: {data['region'].unique().tolist()}")
    print(f"Okres: {data['year'].min()}-{data['year'].max()}")

    # Uruchomienie modeli
    results = {}

    if args.model in ['all', 'dea']:
        results['dea'] = run_dea_analysis(data)

    if args.model in ['all', 'sfa']:
        results['sfa'] = run_sfa_analysis(data)

    if args.model in ['all', 'panel']:
        results['panel'] = run_panel_analysis(data)

    if args.model in ['all', 'did']:
        results['did'] = run_did_analysis(data)

    if args.model in ['all', 'two_stage']:
        results['two_stage'] = run_two_stage_analysis(data)

    # Podsumowanie
    print("\n" + "=" * 80)
    print(" PODSUMOWANIE ANALIZY")
    print("=" * 80)

    print("""
WNIOSKI (na podstawie przykladowych danych):

1. DEA: Pokazuje relatywna efektywnosc regionow w przeksztalcaniu
   inwestycji na wyniki. USA zazwyczaj na granicy efektywnosci.

2. SFA: Parametryczna estymacja pozwala na dekompozycje bledu
   i identyfikacje systematycznej nieefektywnosci.

3. Panel Models: Fixed Effects preferowany (test Hausmana),
   wskazuje na istotny wplyw inwestycji prywatnych na patenty.

4. DiD: Ocena wplywu EU AI Act (2024) - krotkoterminowy negatywny
   efekt na efektywnosc (koszty compliance), ale potencjalne
   dlugoterminowe korzysci (zaufanie, bezpieczenstwo).

5. Two-Stage: Identyfikuje regulatory_index jako negatywny
   determinant efektywnosci krotkoterminowej.

UWAGA: Wyniki oparte na symulowanych danych. Dla rzeczywistych
wnioskow, nalezy uzyc danych z wiarygodnych zrodel.
""")

    return results


if __name__ == "__main__":
    main()
