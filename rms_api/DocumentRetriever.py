from typing import Dict, List, Optional, Any, Union
import requests
import json
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from .config_helper import ConfigHelper, ConfigurationError


class DocumentRetrieverError(Exception):
    """Base exception for DocumentRetriever errors"""
    pass

# class ConfigurationError(Exception):
#     """Custom exception for configuration-related errors"""
#     pass

@dataclass
class DocumentProcessResult:
    """
    Holds the result of processing a single document
    """
    doc_id: str
    success: bool
    saved_attachments: Optional[List[str]] = None
    error_message: Optional[str] = None

class DocumentRetriever:

    # def __init__(self, config_path: str) -> None:
    #     """
    #     Initialize DocumentRetriever with configuration file and establish a session
        
    #     Args:
    #         config_path: Path to JSON configuration file
            
    #     Raises:
    #         DocumentRetrieverError: If config file is invalid or missing
    #     """
    #     self.__config_path = config_path
    #     # Create a session that will be reused for all requests
    #     self.__session = requests.sessions.Session()

    #     try:
    #         self.__buildConfig()
    #         self.__buildCredentials()
    #     except Exception as e:
    #         raise DocumentRetrieverError(f"Failed to initialize: {str(e)}")
        
    
    # def __buildConfig(self) -> None:
    #     """
    #     Build configuration from JSON file
        
    #     Raises:
    #         DocumentRetrieverError: If config file cannot be read or parsed
    #     """
    #     try:
    #         with open(self.__config_path, "r") as config_file:
    #             self.__config = json.load(config_file)
                
    #         required_keys = {'key', 'uuid'}
    #         if not all(key in self.__config for key in required_keys):
    #             raise DocumentRetrieverError(f"Config must contain keys: {required_keys}")
                
    #     except (json.JSONDecodeError, OSError) as e:
    #         raise DocumentRetrieverError(f"Failed to load config: {str(e)}")
        

    # def __init__(self, config_dir: Union[str, Path] = None, environment: str = 'bbg') -> None:
    #     """
    #     Initialize DocumentRetriever with a configuration directory and environment name and establish a session
        
    #     Args:
    #         config_dir: Path to the directory containing configuration files. 
    #                If None, uses default config directory from project root
    #         environment: Which environment config to use ('development' or 'production')

    #     Raises:
    # #         DocumentRetrieverError: If config file is invalid or missing
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
    #         raise DocumentRetrieverError(f"Failed to initialize: {str(e)}")
        
    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        config_dir: Optional[Union[str, Path]] = None,
        environment: str = 'bbg'
    ) -> None:
        """
        Initialize DocumentRetriever with either a specific config file or directory-based configuration.
        
        Args:
            config_path: Path to a specific config file (takes precedence if provided)
            config_dir: Directory containing configuration files
            environment: Environment name for loading specific config ('bbg' by default)
            
        Raises:
            DocumentRetrieverError: If configuration is invalid or cannot be loaded
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
            raise DocumentRetrieverError(f"Failed to initialize: {str(e)}")


    def __buildConfig(self) -> None:
        """
        Builds configuration from JSON files by combining:
        1. Base configuration (rms_config.json)
        2. Environment-specific configuration (rms_config.{env}.json)
        
        For example, if environment is 'development':
        - First loads settings from rms_config.json
        - Then overlays settings from rms_config.development.json

        Raises:
    #         ConfigurationError: If config file cannot be read or parsed
        """
        try:
            # Step 1: Load base configuration
            base_config = self._load_config_file(self.__config_dir / 'rms_config.json')
            config = base_config.copy()
            
            # Step 2: Load environment-specific configuration
            env_config_path = self.__config_dir / f'rms_config.{self.__environment}.json'
            if env_config_path.exists():
                env_config = self._load_config_file(env_config_path)
                # Environment config overrides base config
                config.update(env_config)
                print(f"Loaded {self.__environment} configuration")
            else:
                print(f"Warning: No configuration found for environment: {self.__environment}")
            
            # Step 3: Validate the final configuration
            self._validate_config(config)
            self.__config = config
            
        except Exception as e:
            raise ConfigurationError(f"Failed to build configuration: {str(e)}")
        
    def _load_config_file(self, path: str) -> Dict[str, Any]:
        """
        Loads and parses a JSON configuration file.
        
        Args:
            path: Path to the configuration file
            
        Returns:
            Dictionary containing configuration settings
            
        Raises:
            ConfigurationError: If file cannot be read or parsed
        """

        try:
            with open(path, "r") as config_file:
                return json.load(config_file)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in config file {path}: {str(e)}")
        except OSError as e:
            raise ConfigurationError(f"Could not read config file {path}: {str(e)}")
        
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validates the configuration to ensure all required values are present
        and have appropriate types.
        
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

    def __buildCredentials(self, timeout: int = 60) -> None:
        """
        Retrieve credentials and tokens from Bloomberg
        
        Args:
            timeout: Request timeout in seconds
            
        Raises:
            DocumentRetrieverError: If credentials cannot be retrieved
        """
        try:
            self.__apiKey = self.__config['key']
            self.__uuid = self.__config['uuid']
            self.__url = self.__config['url']
            #self.__headers = {'Cookie': f'BBCLIPSESSION={self.__apiKey}'}

            # response = requests.get(
            #     f'{self.__url}ClipServ/upload/synchronizer',
            #     headers=self.__headers,
            #     timeout=timeout
            # )

            # Update session headers instead of creating new headers for each request
            self.__session.headers.update({'Cookie': f'BBCLIPSESSION={self.__apiKey}'})

            response = self.__session.get(
                f'{self.__url}upload/synchronizer',
                timeout=timeout
            )

            response.raise_for_status()
            tokens = response.json()
            
            self.__synchronizerToken = tokens['synchronizerToken']
            self.__synchronizerUri = tokens['synchronizerUri']

        except requests.exceptions.HTTPError as e:
            raise DocumentRetrieverError(f"Bloomberg API returned an error: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise DocumentRetrieverError(f"Request timed out: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise DocumentRetrieverError(f"Connection failed: {str(e)}")
        except (KeyError, requests.exceptions.RequestException) as e:
            raise DocumentRetrieverError(f"Failed to build credentials: {str(e)}")
        

    def __refresh_credentials(self) -> None:
        """
        Refresh authentication tokens if they've expired. This method rebuilds the credentials
        by making a new request to the Bloomberg API synchronizer endpoint.
        
        Raises:
            DocumentRetrieverError: If credentials cannot be refreshed
        """

        try:
            # We reuse the buildCredentials method, but we need to preserve our session
            old_session = self.__session
            self.__buildCredentials()
            # Restore our session but with the new credentials
            self.__session = old_session
            self.__session.headers.update({'Cookie': f'BBCLIPSESSION={self.__apiKey}'})
        except DocumentRetrieverError as e:
            raise DocumentRetrieverError(f"Failed to refresh credentials: {str(e)}")

    def _make_request(self, url: str, timeout: int = 30) -> requests.Response:
        """
        Make an HTTP request with automatic token refresh on authorization errors.
        This method wraps all API calls to handle token expiration automatically.
        
        Args:
            url: The URL to make the request to
            timeout: Request timeout in seconds
            
        Returns:
            Response object from the request
            
        Raises:
            DocumentRetrieverError: If the request fails even after token refresh
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
            raise DocumentRetrieverError(f"Request failed: {str(e)}")
        
    
    def getDocMetaData(self, docID: str, timeout: int = 60) -> Dict[str, Any]:
        """
        Retrieve document metadata for a provided Note ID using the session
        Includes automatic token refresh if needed
        
        Args:
            docID: Document ID to retrieve
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary containing document metadata
            
        Raises:
            DocumentRetrieverError: If metadata cannot be retrieved
        """
        try:
            url = f'{self.__url}download/getDocMetadata?docId={docID}&uuid={self.__uuid}'
            #response = requests.get(url, headers=self.__headers, timeout=timeout)
            # Use session instead of requests.get
            # response = self.__session.get(url, timeout=timeout)
            #response.raise_for_status()
            #return response.json()

            response = self._make_request(url, timeout)
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            raise DocumentRetrieverError(f"Bloomberg API returned an error: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise DocumentRetrieverError(f"Request timed out: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise DocumentRetrieverError(f"Connection failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise DocumentRetrieverError(f"Failed to get document metadata: {str(e)}")

        
    def getDocAttachments(self, metaDataSearchResults: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Retrieve attachment objects from document metadata
        
        Args:
            metaDataSearchResults: Document metadata dictionary
            
        Returns:
            List of attachment dictionaries
        """
        return metaDataSearchResults.get('attachments', [])
        
    
    def getDocument(self, docID: str, fileID: str, timeout: int = 30) -> requests.Response:
        """
        Retrieve file object for a provided Note ID and Attachment ID using the session
        Includes automatic token refresh if needed
        
        Args:
            docID: Document ID
            fileID: File ID to retrieve
            timeout: Request timeout in seconds
            
        Returns:
            Response object containing the file
            
        Raises:
            DocumentRetrieverError: If document cannot be retrieved
        """
        try:
            url = f'{self.__url}download/getDocAttachment?uuid={self.__uuid}&docId={docID}&attachmentId={fileID}'
            #response = requests.get(url, headers=self.__headers, timeout=timeout)

            # Use session instead of requests.get
            # response = self.__session.get(url, timeout=timeout)
            # response.raise_for_status()
            # return response
        
            return self._make_request(url, timeout)
        
        except requests.exceptions.HTTPError as e:
            raise DocumentRetrieverError(f"Bloomberg API returned an error: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise DocumentRetrieverError(f"Request timed out: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise DocumentRetrieverError(f"Connection failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise DocumentRetrieverError(f"Failed to get document: {str(e)}")


    def saveFile(self, response: requests.Response, path: str) -> None:
        """
        Write file content to specified path
        
        Args:
            response: Response object containing file content
            path: Path to save file
            
        Raises:
            DocumentRetrieverError: If file cannot be saved
        """
        try:
            Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as file:
                file.write(response.content)
        except OSError as e:
            raise DocumentRetrieverError(f"Failed to save file: {str(e)}")


    def transplantDocAttachments(
        self, 
        doc: str, 
        base_path: str, 
        file_types: Union[str, List[str]] = 'All'
    ) -> Optional[List[str]]:
        """
        Retrieve document attachments and save them to specified path
        
        Args:
            doc: ID of note available on Bloomberg
            base_path: Directory path to save attachments
            file_types: File types to save (string or list of extensions starting with '.')
            
        Returns:
            List of saved attachment IDs or None if no attachments were saved
            
        Raises:
            DocumentRetrieverError: If operation fails
            ValueError: If file_types parameter is invalid
        """
        try:
            metaDataSearchResults = self.getDocMetaData(doc)
            attachments = self.getDocAttachments(metaDataSearchResults)

            print(f"{len(attachments)} attachments were retrieved from document {doc}")

            if not attachments:
                return None

            # Filter attachments by file type
            if file_types != 'All':
                if isinstance(file_types, (str, list)):
                    file_types = [file_types] if isinstance(file_types, str) else file_types
                    attachments = [a for a in attachments if a['extension'] in file_types]
                else:
                    raise ValueError(f"file_types must be a string or list, not {type(file_types)}")

            print(f"{len(attachments)} attachments met retrieval criteria\n")
            
            saved_attachments = []
            for attachment in attachments:
                file_id = attachment['fileId']
                if not file_id:
                    print(f"Attachment {attachment['name']} ({attachment['extension']}) has no file ID\n")
                    continue
                    
                print(f"Retrieving {file_id}...")
                response = self.getDocument(doc, file_id)
                print(f"Saving {file_id}...\n")
                
                path = os.path.join(base_path, file_id)
                self.saveFile(response, path)
                saved_attachments.append(file_id)

            num_saved = len(saved_attachments)
            if num_saved > 0:
                print(f"{num_saved} document attachment{'s' if num_saved > 1 else ''} saved")
                return saved_attachments
            else:
                print("No document attachments were approved to be saved")
                return None
                
        except (DocumentRetrieverError, ValueError) as e:
            raise DocumentRetrieverError(f"Failed to transplant attachments: {str(e)}")
        
    def process_single_document(
        self, 
        doc: str, 
        base_path: str,
        file_types: Union[str, List[str]] = 'All'
    ) -> DocumentProcessResult:
        """
        Process a single document and return its result
        
        Args:
            doc: Document ID
            base_path: Base path for saving attachments
            file_types: Types of files to process
            
        Returns:
            DocumentProcessResult containing processing outcome
        """
        try:
            saved_attachments = self.transplantDocAttachments(doc, base_path, file_types)
            return DocumentProcessResult(
                doc_id=doc,
                success=True,
                saved_attachments=saved_attachments if saved_attachments else []
            )
        except Exception as e:
            return DocumentProcessResult(
                doc_id=doc,
                success=False,
                error_message=str(e)
            )
        
    def batch_process_documents(
        self,
        docs: List[str],
        base_path: str,
        file_types: Union[str, List[str]] = 'All',
        max_workers: int = 4
    ) -> Dict[str, DocumentProcessResult]:
        """
        Process multiple documents in parallel using a thread pool
        
        Args:
            docs: List of document IDs to process
            base_path: Base directory for saving attachments
            file_types: Types of files to process
            max_workers: Maximum number of concurrent threads
            
        Returns:
            Dictionary mapping document IDs to their processing results
        """
        # Create the base directory if it doesn't exist
        Path(base_path).mkdir(parents=True, exist_ok=True)
        
        results = {}
        total_docs = len(docs)
        
        print(f"Starting batch processing of {total_docs} documents...")
        
        # Process documents in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a dictionary to track future objects
            future_to_doc = {
                executor.submit(
                    self.process_single_document, 
                    doc, 
                    base_path, 
                    file_types
                ): doc for doc in docs
            }
            
            # Process completed futures as they finish
            for i, future in enumerate(as_completed(future_to_doc), 1):
                doc = future_to_doc[future]
                try:
                    result = future.result()
                    results[doc] = result
                    
                    # Print progress
                    print(f"Progress: {i}/{total_docs} documents processed")
                    
                    # Print success/failure details
                    if result.success:
                        attachment_count = len(result.saved_attachments or [])
                        print(f"Successfully processed document {doc} "
                              f"({attachment_count} attachments saved)")
                    else:
                        print(f"Failed to process document {doc}: {result.error_message}")
                        
                except Exception as e:
                    print(f"Error processing document {doc}: {str(e)}")
                    results[doc] = DocumentProcessResult(
                        doc_id=doc,
                        success=False,
                        error_message=str(e)
                    )
        
        # Print summary
        successful = sum(1 for r in results.values() if r.success)
        failed = total_docs - successful
        print(f"\nBatch processing complete:")
        print(f"- Total documents: {total_docs}")
        print(f"- Successfully processed: {successful}")
        print(f"- Failed: {failed}")
        
        return results

    def generate_batch_report(
        self, 
        results: Dict[str, DocumentProcessResult]
    ) -> str:
        """
        Generate a detailed report of batch processing results
        
        Args:
            results: Dictionary of processing results
            
        Returns:
            Formatted string containing the report
        """
        report_lines = ["Batch Processing Report", "=" * 22, ""]
        
        # Overall statistics
        total = len(results)
        successful = sum(1 for r in results.values() if r.success)
        failed = total - successful
        
        report_lines.extend([
            "Summary Statistics:",
            f"- Total documents processed: {total}",
            f"- Successfully processed: {successful}",
            f"- Failed: {failed}",
            "",
            "Detailed Results:",
            "-" * 15
        ])
        
        # Group results by success/failure
        successful_docs = []
        failed_docs = []
        
        for doc_id, result in results.items():
            if result.success:
                attachment_info = (f"{len(result.saved_attachments)} attachments" 
                                 if result.saved_attachments else "no attachments")
                successful_docs.append(f"- {doc_id} ({attachment_info})")
            else:
                failed_docs.append(f"- {doc_id}: {result.error_message}")
        
        if successful_docs:
            report_lines.extend(["", "Successfully Processed Documents:", *successful_docs])
        
        if failed_docs:
            report_lines.extend(["", "Failed Documents:", *failed_docs])
            
        return "\n".join(report_lines)

        
    def __del__(self) -> None:
        """
        Cleanup method to ensure the session is closed when the object is destroyed
        """
        if hasattr(self, '_DocumentRetriever__session'):
            self.__session.close()