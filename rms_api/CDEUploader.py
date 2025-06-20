from typing import Dict, List, Optional, Any, Union
import requests
import json
from pathlib import Path
import pandas as pd
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from .config_helper import ConfigHelper, ConfigurationError

@dataclass
class CDEUploadResult:
    """
    Holds the result of processing a single CDE upload request
    """
    parsekey: str
    field: str
    value: Any
    date: str
    success: bool
    error_message: Optional[str] = None
    response: Optional[requests.Response] = None

class CDEUploaderError(Exception):
    """Base exception for CDEUploader errors"""
    pass

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors"""
    pass

class CDEUploader:

    def __init__(
            self,
            config_path: Optional[Union[str, Path]] = None,
            config_dir: Union[str, Path] = None, 
            environment: str = 'bbg'
            ) -> None:
        """
        Initialize CDEUploader with configuration directory and environment name
        
        Args:
            config_dir: Path to the directory containing configuration files.
                       If None, uses default config directory from project root
            environment: Which environment config to use ('development' or 'production')
        """
        # Create a session with retry logic and connection pooling
        self.__session = requests.Session()
        
        # Configure retry strategy with exponential backoff
        retry_strategy = Retry(
            total=3,  # maximum number of retries
            backoff_factor=0.5,  # wait 0.5, 1, 2 seconds between retries
            status_forcelist=[500, 502, 503, 504, 429],  # HTTP status codes to retry on
        )
        
        # Configure connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=20,  # number of connection pools to cache
            pool_maxsize=20,  # maximum number of connections to save in the pool
            pool_block=True  # whether to block when pool is full
        )
        
        # Mount the adapter for both HTTP and HTTPS
        self.__session.mount("http://", adapter)
        self.__session.mount("https://", adapter)
        try:
            self.__config = ConfigHelper.load_and_validate_config(
                config_path=config_path,
                config_dir=config_dir,
                environment=environment
            )
            self.__buildCredentials()
        except Exception as e:
            raise CDEUploaderError(f"Failed to initialize: {str(e)}")
        
    # def __init__(
    #         self, config_dir: Union[str, Path] = None, environment: str = 'bbg'
    #         ) -> None:
    #     """
    #     Initialize CDEUploader with configuration directory and environment name
        
    #     Args:
    #         config_dir: Path to the directory containing configuration files.
    #                    If None, uses default config directory from project root
    #         environment: Which environment config to use ('development' or 'production')
    #     """
    #     if config_dir is None:
    #         from . import CONFIG_DIR
    #         self.__config_dir = CONFIG_DIR
    #     else:
    #         self.__config_dir = Path(config_dir)

    #     self.__environment = environment
        
    #     # Create a session with retry logic and connection pooling
    #     self.__session = requests.Session()
        
    #     # Configure retry strategy with exponential backoff
    #     retry_strategy = Retry(
    #         total=3,  # maximum number of retries
    #         backoff_factor=0.5,  # wait 0.5, 1, 2 seconds between retries
    #         status_forcelist=[500, 502, 503, 504, 429],  # HTTP status codes to retry on
    #     )
        
    #     # Configure connection pooling
    #     adapter = HTTPAdapter(
    #         max_retries=retry_strategy,
    #         pool_connections=20,  # number of connection pools to cache
    #         pool_maxsize=20,  # maximum number of connections to save in the pool
    #         pool_block=True  # whether to block when pool is full
    #     )
        
    #     # Mount the adapter for both HTTP and HTTPS
    #     self.__session.mount("http://", adapter)
    #     self.__session.mount("https://", adapter)
    #     try:
    #         self.__buildConfig()
    #         self.__buildCredentials()
    #     except Exception as e:
    #         raise CDEUploaderError(f"Failed to initialize: {str(e)}")

    # def __buildConfig(self) -> None:
    #     """
    #     Builds configuration from JSON files by combining base and environment configs
    #     """
    #     try:
    #         # Load base configuration
    #         base_config = self._load_config_file(self.__config_dir / 'rms_config.json')
    #         config = base_config.copy()
            
    #         # Load environment-specific configuration
    #         env_config_path = self.__config_dir / f'rms_config.{self.__environment}.json'
    #         if env_config_path.exists():
    #             env_config = self._load_config_file(env_config_path)
    #             config.update(env_config)
    #             print(f"Loaded {self.__environment} configuration")
    #         else:
    #             print(f"Warning: No configuration found for environment: {self.__environment}")
            
    #         self._validate_config(config)
    #         self.__config = config
            
    #     except Exception as e:
    #         raise ConfigurationError(f"Failed to build configuration: {str(e)}")

    # def _load_config_file(self, path: Path) -> Dict[str, Any]:
    #     """Loads and parses a JSON configuration file"""
    #     try:
    #         with open(path, "r") as config_file:
    #             return json.load(config_file)
    #     except json.JSONDecodeError as e:
    #         raise ConfigurationError(f"Invalid JSON in config file {path}: {str(e)}")
    #     except OSError as e:
    #         raise ConfigurationError(f"Could not read config file {path}: {str(e)}")

    # def _validate_config(self, config: Dict[str, Any]) -> None:
    #     """Validates the configuration"""
    #     required_keys = {
    #         'key': str,
    #         'uuid': int,
    #         'url': str
    #     }
        
    #     for key, expected_type in required_keys.items():
    #         if key not in config:
    #             raise ConfigurationError(f"Missing required configuration key: {key}")
    #         if not isinstance(config[key], expected_type):
    #             raise ConfigurationError(
    #                 f"Configuration key {key} must be of type {expected_type.__name__}"
    #             )

    def __buildCredentials(self, timeout: int = 60) -> None:

        try:
            self.__apiKey = self.__config['key']
            self.__uuid = self.__config['uuid']
            self.__url = self.__config['url']
            
            # Update session headers
            self.__session.headers.update({'Cookie': f'BBCLIPSESSION={self.__apiKey}'})

            # Get synchronizer tokens
            response = self.__session.get(
                f'{self.__url}/upload/synchronizer',
                timeout=timeout
            )
            response.raise_for_status()
            tokens = response.json()
            
            self.__synchronizerToken = tokens['synchronizerToken']
            self.__synchronizerUri = tokens['synchronizerUri']

        except requests.exceptions.RequestException as e:
            raise CDEUploaderError(f"Failed to build credentials: {str(e)}")

    def __refresh_credentials(self) -> None:
        """Refresh authentication tokens if they've expired"""

        try:
            old_session = self.__session
            self.__buildCredentials()
            self.__session = old_session
            self.__session.headers.update({'Cookie': f'BBCLIPSESSION={self.__apiKey}'})

        except CDEUploaderError as e:
            raise CDEUploaderError(f"Failed to refresh credentials: {str(e)}")

    def _make_request(self, data: Dict[str, Any], timeout: int = 120) -> requests.Response:
        """Make an HTTP request with automatic token refresh on authorization errors"""

        data['uuid'] = self.__uuid
        data['SYNCHRONIZER_TOKEN'] = self.__synchronizerToken
        data['SYNCHRONIZER_URI'] = self.__synchronizerUri

        try:
            response = self.__session.post(
                f'{self.__url}/upload/updateCde',
                data=data,
                timeout=timeout
            )
            
            if response.status_code == 401:
                self.__refresh_credentials()
                response = self.__session.post(
                    f'{self.__url}/upload/updateCde',
                    data=data,
                    timeout=timeout
                )
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            raise CDEUploaderError(f"Request failed: {str(e)}")

    def _build_request_body(self, row: pd.Series) -> Dict[str, Any]:
        """Build request body for a single CDE upload"""

        return {
            'uuid': self.__uuid,
            'SYNCHRONIZER_TOKEN': self.__synchronizerToken,
            'SYNCHRONIZER_URI': self.__synchronizerUri,
            'parsekey': row['parsekey'],
            'field': row['field'],
            'date': row['date'],
            'value': row['value']
        }
    
    def _build_delete_request_body(self, row: pd.Series) -> Dict[str, Any]:
        """Build request body for a single CDE upload"""

        return {
            'uuid': self.__uuid,
            'SYNCHRONIZER_TOKEN': self.__synchronizerToken,
            'SYNCHRONIZER_URI': self.__synchronizerUri,
            'parsekey': row['parsekey'],
            'field': row['field'],
            'date': row['date'],
            'delete': True
        }

    def upload_single_cde(self, data: Dict[str, Any]) -> CDEUploadResult:
        """Upload a single CDE entry"""

        try:
            response = self._make_request(data)
            return CDEUploadResult(
                parsekey=data['parsekey'],
                field=data['field'],
                value=data['value'],
                date=data['date'],
                success=True,
                response=response
            )
        except Exception as e:
            return CDEUploadResult(
                parsekey=data['parsekey'],
                field=data['field'],
                value=data['value'],
                date=data['date'],
                success=False,
                error_message=str(e)
            )
        
    def delete_single_cde(self, data: Dict[str, Any]) -> CDEUploadResult:
        """Upload a single CDE entry"""

        try:
            response = self._make_request(data)
            return CDEUploadResult(
                parsekey=data['parsekey'],
                field=data['field'],
                value='deleted',
                date=data['date'],
                success=True,
                response=response
            )
        except Exception as e:
            return CDEUploadResult(
                parsekey=data['parsekey'],
                field=data['field'],
                value='not deleted',
                date=data['date'],
                success=False,
                error_message=str(e)
            )
        
    def batch_delete_cde(
        self,
        df: pd.DataFrame,
        max_workers: int = 20,
        batch_size: int = 50,
        batch_delay: float = 0.5
    ) -> List[CDEUploadResult]:
        """
        Upload multiple CDE entries concurrently
        
        Args:
            df: DataFrame containing CDE data (must have parsekey, field, date, value columns)
            max_workers: Maximum number of concurrent uploads (default 100)
            
        Returns:
            List of CDEUploadResult objects
        """

        required_columns = {'parsekey', 'field', 'date', 'value'}
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"DataFrame must contain columns: {required_columns}")
        
        results = []
        total_entries = len(df)
        
        print(f"Starting batch delete of {total_entries} CDE entries in batches of {batch_size}...")
        
        # Split the dataframe into batches
        batches = [df[i:i + batch_size] for i in range(0, len(df), batch_size)]
        
        for batch_num, batch_df in enumerate(batches, 1):
            print(f"\nProcessing batch {batch_num}/{len(batches)}")
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_data = {
                    executor.submit(
                        self.delete_single_cde,
                        self._build_delete_request_body(row)
                    ): row for _, row in batch_df.iterrows()
                }
                
                for i, future in enumerate(as_completed(future_to_data), 1):
                    try:
                        result = future.result()
                        results.append(result)
                        
                        if i % 10 == 0 or i == len(batch_df):
                            print(f"Progress: {i}/{len(batch_df)} entries processed in current batch")
                        
                        if result.success:
                            print(f"Successfully deleted CDE for {result.parsekey}")
                        else:
                            print(f"Failed to delete CDE for {result.parsekey}: {result.error_message}")
                            
                    except Exception as e:
                        print(f"Error in batch processing: {str(e)}")
            
            # Add delay between batches
            if batch_num < len(batches):
                time.sleep(batch_delay)

        successful = sum(1 for r in results if r.success)
        failed = total_entries - successful
        print(f"\nBatch delete complete:")
        print(f"- Total entries: {total_entries}")
        print(f"- Successfully deleted: {successful}")
        print(f"- Failed: {failed}")
        
        return results

    def batch_upload_cde(
        self,
        df: pd.DataFrame,
        max_workers: int = 20,
        batch_size: int = 50,
        batch_delay: float = 0.5
    ) -> List[CDEUploadResult]:
        """
        Upload multiple CDE entries concurrently
        
        Args:
            df: DataFrame containing CDE data (must have parsekey, field, date, value columns)
            max_workers: Maximum number of concurrent uploads (default 100)
            
        Returns:
            List of CDEUploadResult objects
        """

        required_columns = {'parsekey', 'field', 'date', 'value'}
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"DataFrame must contain columns: {required_columns}")
        
        results = []
        total_entries = len(df)
        
        print(f"Starting batch upload of {total_entries} CDE entries in batches of {batch_size}...")
        
        # Split the dataframe into batches
        batches = [df[i:i + batch_size] for i in range(0, len(df), batch_size)]
        
        for batch_num, batch_df in enumerate(batches, 1):
            print(f"\nProcessing batch {batch_num}/{len(batches)}")
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_data = {
                    executor.submit(
                        self.upload_single_cde,
                        self._build_request_body(row)
                    ): row for _, row in batch_df.iterrows()
                }
                
                for i, future in enumerate(as_completed(future_to_data), 1):
                    try:
                        result = future.result()
                        results.append(result)
                        
                        if i % 10 == 0 or i == len(batch_df):
                            print(f"Progress: {i}/{len(batch_df)} entries processed in current batch")
                        
                        if result.success:
                            print(f"Successfully uploaded CDE for {result.parsekey}")
                        else:
                            print(f"Failed to upload CDE for {result.parsekey}: {result.error_message}")
                            
                    except Exception as e:
                        print(f"Error in batch processing: {str(e)}")
            
            # Add delay between batches
            if batch_num < len(batches):
                time.sleep(batch_delay)

        successful = sum(1 for r in results if r.success)
        failed = total_entries - successful
        print(f"\nBatch upload complete:")
        print(f"- Total entries: {total_entries}")
        print(f"- Successfully uploaded: {successful}")
        print(f"- Failed: {failed}")
        
        return results

    def generate_upload_report(self, results: List[CDEUploadResult]) -> str:
        """Generate a detailed report of upload results"""
        report_lines = ["CDE Upload Report", "=" * 16, ""]
        
        total = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total - successful
        
        report_lines.extend([
            "Summary Statistics:",
            f"- Total entries processed: {total}",
            f"- Successfully uploaded: {successful}",
            f"- Failed: {failed}",
            "",
            "Detailed Results:",
            "-" * 15
        ])
        
        for result in results:
            status = "Success" if result.success else f"Failed: {result.error_message}"
            entry_info = (
                f"- {result.parsekey} (Field: {result.field}, "
                f"Date: {result.date}, Value: {result.value}): {status}"
            )
            report_lines.append(entry_info)
            
        return "\n".join(report_lines)

    def __del__(self) -> None:
        """Cleanup method to close the session"""
        if hasattr(self, '_CDEUploader__session'):
            self.__session.close()