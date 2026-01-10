# Data collection module
"""
Modul do pobierania danych o finansowaniu AI z roznych zrodel.

Wspierane zrodla:
- Stanford HAI AI Index
- OECD AI Policy Observatory
"""

from .stanford_hai import StanfordHAIDataLoader, load_stanford_hai_data
from .oecd_ai import OECDAIDataLoader, load_oecd_data

__all__ = [
    'StanfordHAIDataLoader',
    'load_stanford_hai_data',
    'OECDAIDataLoader',
    'load_oecd_data'
]
