# from pathlib import Path

# # Get the absolute path to the project root directory
# RMS_API_ROOT = Path(__file__).parent.absolute()
# CONFIG_DIR = RMS_API_ROOT / 'config'

# # Export the classes
# from .DocumentRetriever import DocumentRetriever
# from .RMSBQL import RMSBQL

# def get_config_dir() -> Path:
#     """Returns the absolute path to the config directory"""
#     return CONFIG_DIR

# def initialize_rmsbql_client(environment: str = 'bbg'):
#     """Initialize RMSBQL client"""
#     config_dir = get_config_dir()
#     return RMSBQL(config_dir=config_dir, environment=environment)

# def initialize_docretrieval_client(environment: str = 'bbg'):
#     """Initialize DocumentRetriever client"""
#     config_dir = get_config_dir()
#     return DocumentRetriever(config_dir=config_dir, environment=environment)

# def initialize_clients(environment: str = 'bbg'):
#     """Initialize both clients"""
#     config_dir = get_config_dir()
#     return (
#         RMSBQL(config_dir=config_dir, environment=environment),
#         DocumentRetriever(config_dir=config_dir, environment=environment)
#     )

from pathlib import Path
from typing import Tuple, Union, Optional

# Get the absolute path to the project root directory
RMS_API_ROOT = Path(__file__).parent.absolute()
CONFIG_DIR = RMS_API_ROOT / 'config'

# Export the classes and helpers
from .config_helper import ConfigHelper, ConfigurationError
from .DocumentRetriever import DocumentRetriever
from .RMSBQL import RMSBQL
from .CDEUploader import CDEUploader
from .NotePublisher import NotePublisher
from .NotePublisher import (
    UserType, 
    ShareableType, 
    TagType, 
    SubType,
    CMTY,
    BBG_USER,
    BBG_SPDL,
    TAGLIST,
    NOTE_SECURITY,
    BaseEntity
)

__all__ = [
    'RMSBQL',
    'DocumentRetriever',
    'CDEUploader',
    'NotePublisher',
    'ConfigHelper',
    'ConfigurationError',
    'initialize_rmsbql_client',
    'initialize_docretrieval_client',
    'initialize_clients',
    'get_config_dir'
]

def get_config_dir() -> Path:
    """Returns the absolute path to the config directory"""
    return CONFIG_DIR

def initialize_rmsbql_client(
    config_path: Optional[Union[str, Path]] = None,
    environment: str = 'bbg'
) -> RMSBQL:
    """Initialize RMSBQL client"""
    if config_path:
        return RMSBQL(config_path=config_path)
    return RMSBQL(config_dir=get_config_dir(), environment=environment)

def initialize_docretrieval_client(
    config_path: Optional[Union[str, Path]] = None,
    environment: str = 'bbg'
) -> DocumentRetriever:
    """Initialize DocumentRetriever client"""
    if config_path:
        return DocumentRetriever(config_path=config_path)
    return DocumentRetriever(config_dir=get_config_dir(), environment=environment)

def initialize_cdeuploader_client(
    config_path: Optional[Union[str, Path]] = None,
    environment: str = 'bbg'
) -> CDEUploader:
    """Initialize CDEUploader client"""
    if config_path:
        return CDEUploader(config_path=config_path)
    return CDEUploader(config_dir=get_config_dir(), environment=environment)

def initialize_notepublisher_client(
    config_path: Optional[Union[str, Path]] = None,
    environment: str = 'bbg'
) -> NotePublisher:
    """Initialize NotePublisher client"""
    if config_path:
        return NotePublisher(config_path=config_path)
    return NotePublisher(config_dir=get_config_dir(), environment=environment)

def initialize_clients(
    config_path: Optional[Union[str, Path]] = None,
    environment: str = 'bbg'
) -> Tuple[RMSBQL, DocumentRetriever, CDEUploader]:
    """Initialize both clients"""
    if config_path:
        return (
            RMSBQL(config_path=config_path),
            DocumentRetriever(config_path=config_path),
            CDEUploader(config_path=config_path),
            CDEUploader(config_path=config_path)
        )
    config_dir = get_config_dir()
    return (
        RMSBQL(config_dir=config_dir, environment=environment),
        DocumentRetriever(config_dir=config_dir, environment=environment),
        CDEUploader(config_dir=config_dir, environment=environment),
        NotePublisher(config_dir=config_dir, environment=environment)
    )