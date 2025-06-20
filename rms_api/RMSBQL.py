import requests
import json
import urllib.parse
from pathlib import Path
import numpy as np
import pandas as pd

from typing import Dict, Optional, Any, Union

from .config_helper import ConfigHelper, ConfigurationError

class RMSBQLError(Exception):
    """Base exception class for RMSBQL errors"""
    pass

# class ConfigurationError(Exception):
#     """Custom exception for configuration-related errors"""
#     pass

class RMSBQL():
    
    # def __init__(self, config: Dict[str, str]) -> None:
    #     """
    #     Initialize RMSBQL client
        
    #     Args:
    #         config: Dictionary containing 'key', 'uuid', and 'url' keys
            
    #     Raises:
    #         KeyError: If required config keys are missing
    #     """

    #     required_keys = {'key', 'uuid', 'url'}
    #     if not all(key in config for key in required_keys):
    #         raise KeyError(f"Config must contain keys: {required_keys}")
        
    #     self.__apiKey = config['key']
    #     self.__uuid = config['uuid']
    #     self.__url = config['url']
    #     self.__headers = {'Cookie': f'BBCLIPSESSION={self.__apiKey}'}


    # def __init__(self, config_dir: Union[str, Path] = None, environment: str = 'bbg') -> None:
    #     """
    #     Initialize DocumentRetriever with a configuration directory and environment name and establish a session
        
    #     Args:
    #         config_dir: Path to the directory containing configuration files. 
    #                If None, uses default config directory from project root
    #         environment: Which environment config to use ('development' or 'production')

    #     Raises:
    # #         RMSBQLError: If config file is invalid or missing
    #     """
    #     #self.__config_dir = Path(config_dir)
    #     if config_dir is None:
    #         # Use the default config directory from project root
    #         from . import CONFIG_DIR
    #         self.__config_dir = CONFIG_DIR
    #     else:
    #         self.__config_dir = Path(config_dir)

    #     self.__environment = environment

    #     # Create a session that will be reused for all requests
    #     self.__session = requests.sessions.Session()

    #     try:
    #         self.__buildConfig()
    #         self.__buildCredentials()
    #     except Exception as e:
    #         raise RMSBQLError(f"Failed to initialize: {str(e)}")

    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        config_dir: Optional[Union[str, Path]] = None,
        environment: str = 'bbg'
    ) -> None:
        """
        Initialize RMSBQL with either a specific config file or directory-based configuration.
        
        Args:
            config_path: Path to a specific config file (takes precedence if provided)
            config_dir: Directory containing configuration files
            environment: Environment name for loading specific config ('bbg' by default)
            
        Raises:
            RMSBQLError: If configuration is invalid or cannot be loaded
        """
        # Create a session that will be reused for all requests
        self.__session = requests.sessions.Session()
        
        try:
            self.__config = ConfigHelper.load_and_validate_config(
                config_path=config_path,
                config_dir=config_dir,
                environment=environment
            )
            self.__buildCredentials()
        except Exception as e:
            raise RMSBQLError(f"Failed to initialize: {str(e)}")

    # def __buildConfig(self) -> None:
    #     """
    #     Builds configuration from JSON files by combining:
    #     1. Base configuration (rms_config.json)
    #     2. Environment-specific configuration (rms_config.{env}.json)
        
    #     For example, if environment is 'development':
    #     - First loads settings from rms_config.json
    #     - Then overlays settings from rms_config.development.json

    #     Raises:
    # #         ConfigurationError: If config file cannot be read or parsed
    #     """
        
    #     try:
    #         # Step 1: Load base configuration
    #         base_config = self._load_config_file(self.__config_dir / 'rms_config.json')
    #         config = base_config.copy()
            
    #         # Step 2: Load environment-specific configuration
    #         env_config_path = self.__config_dir / f'rms_config.{self.__environment}.json'
    #         if env_config_path.exists():
    #             env_config = self._load_config_file(env_config_path)
    #             # Environment config overrides base config
    #             config.update(env_config)
    #             print(f"Loaded {self.__environment} configuration")
    #         else:
    #             print(f"Warning: No configuration found for environment: {self.__environment}")
            
    #         # Step 3: Validate the final configuration
    #         self._validate_config(config)
    #         self.__config = config
            
    #     except Exception as e:
    #         raise ConfigurationError(f"Failed to build configuration: {str(e)}")
        
    # def _load_config_file(self, path: str) -> Dict[str, Any]:
    #     """
    #     Loads and parses a JSON configuration file.
        
    #     Args:
    #         path: Path to the configuration file
            
    #     Returns:
    #         Dictionary containing configuration settings
            
    #     Raises:
    #         ConfigurationError: If file cannot be read or parsed
    #     """

    #     try:
    #         with open(path, "r") as config_file:
    #             return json.load(config_file)
    #     except json.JSONDecodeError as e:
    #         raise ConfigurationError(f"Invalid JSON in config file {path}: {str(e)}")
    #     except OSError as e:
    #         raise ConfigurationError(f"Could not read config file {path}: {str(e)}")
        
    # def _validate_config(self, config: Dict[str, Any]) -> None:
    #     """
    #     Validates the configuration to ensure all required values are present
    #     and have appropriate types.
        
    #     Args:
    #         config: Configuration dictionary to validate
            
    #     Raises:
    #         ConfigurationError: If configuration is invalid
    #     """
    #     required_keys = {
    #         'key': str,
    #         'uuid': int,
    #         'url': str
    #     }
        
    #     optional_keys = {
    #         'timeout': (int, float)
    #     }
        
    #     # Check required keys
    #     for key, expected_type in required_keys.items():
    #         if key not in config:
    #             raise ConfigurationError(f"Missing required configuration key: {key}")
    #         if not isinstance(config[key], expected_type):
    #             raise ConfigurationError(
    #                 f"Configuration key {key} must be of type {expected_type.__name__}"
    #             )
        
    #     # Check optional keys if they exist
    #     for key, expected_type in optional_keys.items():
    #         if key in config and not isinstance(config[key], expected_type):
    #             raise ConfigurationError(
    #                 f"Configuration key {key} must be of type {expected_type.__name__}"
    #             )

    def __buildCredentials(self, timeout: int = 60) -> None:
        """
        Retrieve credentials and tokens from Bloomberg
        
        Args:
            timeout: Request timeout in seconds
            
        Raises:
            RMSBQLError: If credentials cannot be retrieved
        """
        try:
            self.__apiKey = self.__config['key']
            self.__uuid = self.__config['uuid']
            self.__url = self.__config['url']
            #self.__headers = {'Cookie': f'BBCLIPSESSION={self.__apiKey}'}

            # Update session headers instead of creating new headers for each request
            self.__session.headers.update({'Cookie': f'BBCLIPSESSION={self.__apiKey}'})


        except requests.exceptions.HTTPError as e:
            raise RMSBQLError(f"Bloomberg API returned an error: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise RMSBQLError(f"Request timed out: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise RMSBQLError(f"Connection failed: {str(e)}")
        except (KeyError, requests.exceptions.RequestException) as e:
            raise RMSBQLError(f"Failed to build credentials: {str(e)}")
        
    def __refresh_credentials(self) -> None:
        """
        Refresh authentication tokens if they've expired. This method rebuilds the credentials
        by making a new request to the Bloomberg API synchronizer endpoint.
        
        Raises:
            RMSBQLError: If credentials cannot be refreshed
        """

        try:
            # We reuse the buildCredentials method, but we need to preserve our session
            old_session = self.__session
            self.__buildCredentials()
            # Restore our session but with the new credentials
            self.__session = old_session
            self.__session.headers.update({'Cookie': f'BBCLIPSESSION={self.__apiKey}'})

        except RMSBQLError as e:
            raise RMSBQLError(f"Failed to refresh credentials: {str(e)}")

    def _make_request(self, url: str, timeout: int = 120) -> requests.Response:
        """
        Make an HTTP request with automatic token refresh on authorization errors.
        This method wraps all API calls to handle token expiration automatically.
        
        Args:
            url: The URL to make the request to
            timeout: Request timeout in seconds
            
        Returns:
            Response object from the request
            
        Raises:
            RMSBQLError: If the request fails even after token refresh
        """

        try:
            # Make the initial request
            response = self.__session.get(url, timeout=timeout)
            
            # Check if we got an unauthorized response (401)
            if response.status_code == 401:
                # Token might be expired, let's refresh and try again
                self.__refresh_credentials()
                # Retry the request with new credentials
                response = self.__session.get(url, timeout=timeout)
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            raise RMSBQLError(f"Request failed: {str(e)}")


    def submitBQLRequest(self, query: str, timeout: int = 120) -> Dict[str, Any]:
        """
        Submit a BQL query to the API
        
        Args:
            query: BQL query string
            timeout: Request timeout in seconds
            
        Returns:
            Dict containing the API response
            
        Raises:
            RMSBQLError: If the request fails or returns an error
        """

        try:
            query_encoded = urllib.parse.quote(query)
            bql_req = f'{self.__url}/download/queryBql?expression={query_encoded}&uuid={self.__uuid}'
            #response = requests.get(bql_req, headers=self.__headers, timeout=timeout)
            response = self._make_request(bql_req, timeout)
            #response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise RMSBQLError(f"Bloomberg API returned an error: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise RMSBQLError(f"Request timed out: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise RMSBQLError(f"Connection failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise RMSBQLError(f"Failed to execute BQL query: {str(e)}")
        
        

    def __process_response_item(self, item: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """
        Process a single response item into a DataFrame
        
        Args:
            item: Response item dictionary
            
        Returns:
            DataFrame containing the processed data or None if processing failed
        """
        if 'sirExceptions' in item:
            if 'partialErrorMap' in item['sirExceptions']:
                print(f'Partial Errors Exist for {item["name"]}')
                return None
                
            exception = item['sirExceptions']['responseExceptions'][0]
            print(f"Error: {exception['message']}")
            print(f"Internal Error: {exception['internalMessage']}")
            return None
            
        frame_data = {}
        for column in item['columns']:
            key = column['name']
            values = next(iter(next(iter(column['values']['typedValues'].values())).values()))
            frame_data[key] = values
            
        return pd.DataFrame(frame_data).rename(columns={'VALUE': item['name']})
    
    def executeBQLRequest(self, query: str) -> Dict[str, pd.DataFrame]:
        """
        Execute a BQL query and process the results
        
        Args:
            query: BQL query string
            
        Returns:
            Dictionary mapping result names to DataFrames
            
        Raises:
            RMSBQLError: If query execution fails
        """
        
        bql_res = self.submitBQLRequest(query)
        
        if 'errorMessages' in bql_res:
            print(f"Error: {bql_res['errorMessages']}")
            return {}
            
        response_frames_dict = {}
        for item in bql_res.get('results', []):
            frame = self.__process_response_item(item)
            if frame is not None:
                response_frames_dict[item['name']] = frame
                
        return response_frames_dict
    

    
    