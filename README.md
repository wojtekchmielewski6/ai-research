# AI Infrastructure Financing Effectiveness Model

Analiza porownawcza efektywnosci finansowania infrastruktury AI w USA, UE i Chinach (2015-2025).

## Cel projektu

Ocena efektywnosci inwestycji w infrastrukture AI z uwzglednieniem roznych celow strategicznych kazdego regionu:

| Region | Podejscie strategiczne | Glowne cele |
|--------|------------------------|-------------|
| **USA** | Rynkowe, zdecentralizowane | Innowacyjnosc, dominacja technologiczna |
| **UE** | Regulacyjne (AI Act) | Bezpieczenstwo, prawa czlowieka, zaufanie |
| **Chiny** | Centralne, panstwowe | Samowystarczalnosc, kontrola, skala |

## Metryki efektywnosci (na podstawie literatury)

### Zmienne wejsciowe (Inputs)
- Inwestycje publiczne w AI R&D
- Inwestycje prywatne (VC, corporate)
- Kapital ludzki (liczba badaczy AI)
- Infrastruktura obliczeniowa (compute capacity)

### Zmienne wyjsciowe (Outputs)
- Patenty AI (wazone cytatami)
- Publikacje naukowe (NeurIPS, ICML, itd.)
- Liczba startupow AI
- Modele foundation (LLM, vision)
- Wskaznik adopcji AI w gospodarce
- Wplyw na produktywnosc (TFP)

## Top 5 modeli statystycznych

1. **DEA (Data Envelopment Analysis)** - nieparametryczna analiza efektywnosci wzglednej
2. **SFA (Stochastic Frontier Analysis)** - parametryczna z dekompozycja bledu
3. **Panel Data Models (FE/RE)** - modele panelowe dla danych czasowo-przestrzennych
4. **Difference-in-Differences (DiD)** - ewaluacja wplywu polityk
5. **Two-Stage DEA/Tobit** - analiza determinant efektywnosci

## Struktura projektu

```
ai-research/
├── data/
│   ├── raw/              # Surowe dane ze zrodel
│   └── processed/        # Przetworzone dane do analizy
├── src/
│   ├── utils/            # Funkcje pomocnicze
│   └── data_collection/  # Skrypty pobierania danych
├── models/               # Implementacje modeli
├── analysis/             # Notebooki Jupyter z analiza
├── reports/              # Wyniki, wykresy, raporty
└── requirements.txt      # Zaleznosci Python
```

## Zrodla danych

- [Stanford HAI AI Index](https://hai.stanford.edu/ai-index/2025-ai-index-report)
- [OECD AI Policy Observatory](https://oecd.ai/)
- [WIPO Global Innovation Index](https://www.wipo.int/gii/)
- World Bank / IMF
- Crunchbase (dane o VC)
- USPTO, EPO, CNIPA (patenty)

## Literatura

### Metodologia
- Kumbhakar & Lovell (2000) - Stochastic Frontier Analysis
- Cooper et al. (2007) - Data Envelopment Analysis
- Wooldridge (2010) - Econometric Analysis of Panel Data

### Porownanie regionow
- [Atlantic Council - Transatlantic AI Strategy](https://www.atlanticcouncil.org/in-depth-research-reports/issue-brief/what-drives-the-divide-in-transatlantic-ai-strategy/)
- [Comparative Global AI Regulation (arXiv)](https://arxiv.org/html/2410.21279v1)

## Uruchomienie

```bash
pip install -r requirements.txt
python src/main.py
```

## Autor

Projekt badawczy - analiza efektywnosci finansowania AI
