"""
Data models and interfaces for market, fundamental, and event data.

This module defines the data contracts and interfaces that the
archetype system expects, without implementing specific data sources.

The goal is to provide a clean abstraction layer that can work with
different data providers (Bloomberg API, local files, mock data, etc.)
"""

from .market_data import (
    MarketDataInterface,
    SecurityPrice,
    VolumeData,
    VolatilityMetrics,
    TechnicalIndicators
)

from .fundamental_data import (
    FundamentalDataInterface,
    EarningsData,
    EstimateData,
    ConsensusData,
    FinancialStatement
)

from .event_data import (
    EventDataInterface,
    CorporateEvent,
    NewsEvent,
    MarketEvent,
    EventCalendar
)

# Abstract base classes for data providers
from .interfaces import (
    DataProvider,
    DataQuery,
    DataResponse,
    DataError
)

# Mock implementations for testing and development
from .mock_providers import (
    MockMarketDataProvider,
    MockFundamentalDataProvider, 
    MockEventDataProvider
)

__all__ = [
    # Interface definitions
    "MarketDataInterface",
    "FundamentalDataInterface",
    "EventDataInterface",
    
    # Data structures
    "SecurityPrice",
    "VolumeData", 
    "VolatilityMetrics",
    "TechnicalIndicators",
    "EarningsData",
    "EstimateData",
    "ConsensusData",
    "FinancialStatement",
    "CorporateEvent",
    "NewsEvent", 
    "MarketEvent",
    "EventCalendar",
    
    # Abstract base classes
    "DataProvider",
    "DataQuery",
    "DataResponse",
    "DataError",
    
    # Mock implementations
    "MockMarketDataProvider",
    "MockFundamentalDataProvider",
    "MockEventDataProvider",
]