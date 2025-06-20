from pathlib import Path
import json
from typing import Dict, Union, Any, Optional

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors"""
    pass

class ConfigHelper:
    """Helper class to handle different configuration initialization approaches"""
    
    @staticmethod
    def load_and_validate_config(
        config_path: Optional[Union[str, Path]] = None,
        config_dir: Optional[Union[str, Path]] = None,
        environment: str = 'bbg'
    ) -> Dict[str, Any]:
        """
        Load configuration either from a single file or from directory with environment.
        
        Args:
            config_path: Path to a specific config file (takes precedence if provided)
            config_dir: Directory containing configuration files
            environment: Environment name for loading specific config
            
        Returns:
            Dictionary containing validated configuration
            
        Raises:
            ConfigurationError: If configuration is invalid or cannot be loaded
        """
        
        if config_path is not None:
            # Single file configuration takes precedence
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                ConfigHelper._validate_config(config)
                return config
            except Exception as e:
                raise ConfigurationError(f"Failed to load config file {config_path}: {str(e)}")
        
        # Directory-based configuration
        if config_dir is None:
            # Use default config directory from project root
            from . import CONFIG_DIR
            config_dir = CONFIG_DIR
        else:
            config_dir = Path(config_dir)
            
        try:
            # Load base configuration
            base_config_path = config_dir / 'rms_config.json'
            with open(base_config_path, 'r') as f:
                config = json.load(f)
            
            # Load environment-specific configuration if it exists
            env_config_path = config_dir / f'rms_config.{environment}.json'
            if env_config_path.exists():
                with open(env_config_path, 'r') as f:
                    env_config = json.load(f)
                config.update(env_config)
                print(f"Loaded {environment} configuration")
            else:
                print(f"Warning: No configuration found for environment: {environment}")
                
            ConfigHelper._validate_config(config)
            return config
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {str(e)}")
    
    @staticmethod
    def _validate_config(config: Dict[str, Any]) -> None:
        """
        Validate configuration dictionary
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        
        required_keys = {
            'key': str,
            'uuid': int,
            'url': str
        }
        
        optional_keys = {
            'timeout': (int, float)
        }
        
        # Check required keys
        for key, expected_type in required_keys.items():
            if key not in config:
                raise ConfigurationError(f"Missing required configuration key: {key}")
            if not isinstance(config[key], expected_type):
                raise ConfigurationError(
                    f"Configuration key {key} must be of type {expected_type.__name__}"
                )
        
        # Check optional keys if they exist
        for key, expected_type in optional_keys.items():
            if key in config and not isinstance(config[key], expected_type):
                raise ConfigurationError(
                    f"Configuration key {key} must be of type {expected_type.__name__}"
                )