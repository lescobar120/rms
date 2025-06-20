import requests
import base64
import json
import urllib.parse
import enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, ClassVar, Literal
from dataclasses import dataclass, field
import pydantic
from pydantic import BaseModel, Field, field_validator, model_validator

try:
    from .config_helper import ConfigHelper, ConfigurationError
except ImportError:
    # Fallback for when module is imported directly
    from config_helper import ConfigHelper, ConfigurationError


class NotePublisherError(Exception):
    """Base exception for NotePublisher errors"""
    pass


class AuthenticationError(NotePublisherError):
    """Authentication-related errors"""
    pass


class ValidationError(NotePublisherError):
    """Validation-related errors"""
    pass


class UserType(str, enum.Enum):
    WORKGROUPS = 'WORKGROUPS'
    PEOPLE = 'PEOPLE'
    AUTHORS = 'AUTHORS'


class ShareableType(str, enum.Enum):
    COMMUNITIES = 'COMMUNITIES'
    SHAREABLES = 'SHAREABLES'
    WORKGROUPS = 'WORKGROUPS'


class TagType(str, enum.Enum):
    CUSTOM = 'CUSTOM'
    SECURITIES = 'SECURITIES'
    PEOPLE = 'PEOPLE'
    AUTHORS = 'AUTHORS'


class SubType(str, enum.Enum):
    UUID = 'UUID'
    WORKGROUP = 'WORKGROUP'
    SPDL = 'SPDL'
    TAGLISTS = 'TAGLISTS'
    CORP = 'CORP'


# Pydantic Models
class BaseEntity(BaseModel):
    """Base model for all Bloomberg entities"""
    description: str
    key: str
    metadata: Optional[str] = None
    
    class Config:
        validate_assignment = True
        extra = 'forbid'


class CMTY(BaseEntity):
    """Community entity model"""
    subtype: Optional[Literal['WORKGROUP']] = None
    type: Literal["COMMUNITIES"] = "COMMUNITIES"
    
    @field_validator('subtype')
    @classmethod
    def validate_subtype(cls, v):
        if v is not None and v != 'WORKGROUP':
            raise ValueError(f"Invalid subtype: {v}. Must be 'WORKGROUP' or None")
        return v.upper() if v else v


class BBG_USER(BaseEntity):
    """Bloomberg User entity model"""
    subtype: Optional[Literal['UUID']] = None
    type: Literal['WORKGROUPS', 'PEOPLE', 'AUTHORS']
    
    @field_validator('type')
    @classmethod
    def normalize_type(cls, v):
        return v.upper()
    
    @field_validator('subtype')
    @classmethod
    def normalize_subtype(cls, v):
        return v.upper() if v else v
    
    @model_validator(mode='after')
    def validate_type_subtype_combination(self):
        if self.type == 'WORKGROUPS' and self.subtype != 'UUID':
            raise ValueError("WORKGROUPS type requires 'UUID' subtype")
        if self.type in ['PEOPLE', 'AUTHORS'] and self.subtype is not None:
            raise ValueError(f"{self.type} type requires subtype to be None")
        return self


class BBG_SPDL(BaseEntity):
    """Bloomberg SPDL entity model"""
    subtype: Literal["SPDL"] = "SPDL"
    type: Literal["SHAREABLES"] = "SHAREABLES"


class TAGLIST(BaseEntity):
    """Taglist entity model"""
    subtype: Literal["TAGLISTS"] = "TAGLISTS"
    type: Literal["CUSTOM"] = "CUSTOM"


class NOTE_SECURITY(BaseEntity):
    """Security entity model"""
    subtype: Optional[Literal['CORP']] = None
    type: Literal["SECURITIES"] = "SECURITIES"
    
    @field_validator('subtype')
    @classmethod
    def normalize_subtype(cls, v):
        return v.upper() if v else v


@dataclass
class NoteAttachment:
    """Data class for note attachments"""
    file_path: str
    attachment_id: Optional[str] = None
    file_size: Optional[int] = None


class NotePublisher:
    """
    Bloomberg Note Publisher API Client
    
    This class provides methods to create and publish research notes to Bloomberg RMS.
    """
    
    BASE_URL = 'https://rms.bloomberg.com/'
    DEFAULT_TIMEOUT = 60
    DEFAULT_PART_SIZE = 1024 * 1024  # 1MB chunks
    
    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        config_dir: Optional[Union[str, Path]] = None,
        environment: str = 'bbg'
    ) -> None:
        """
        Initialize NotePublisher with either a specific config file or directory-based configuration.
        
        Args:
            config_path: Path to a specific config file (takes precedence if provided)
            config_dir: Directory containing configuration files
            environment: Environment name for loading specific config ('bbg' by default)
            
        Raises:
            NotePublisherError: If initialization fails
        """
        # Create a session that will be reused for all requests
        self.session = requests.Session()
        
        # Initialize configuration using ConfigHelper
        try:
            self._config = ConfigHelper.load_and_validate_config(
                config_path=config_path,
                config_dir=config_dir,
                environment=environment
            )
            self._authenticate()
        except Exception as e:
            raise NotePublisherError(f"Failed to initialize: {str(e)}")
        
        # Initialize firm configurations
        self._firm_configs = {
            'shareable': ['BLOOMBERG'],
            'tagged': ['Bloomberg']
        }
    
    def _authenticate(self) -> None:
        """Authenticate with Bloomberg API and get tokens"""
        try:
            # Extract configuration values
            self._api_key = self._config['key']
            self._uuid = self._config['uuid']
            self._url = self._config['url']
            
            # Ensure URL ends with a slash
            if not self._url.endswith('/'):
                self._url += '/'
            
            # Set up session headers
            self.session.headers.update({
                'Cookie': f'BBCLIPSESSION={self._api_key}'
            })
            
            # Get synchronizer tokens - check if URL already contains ClipServ
            if 'ClipServ' in self._url:
                sync_url = f'{self._url}upload/synchronizer'
            else:
                sync_url = f'{self._url}ClipServ/upload/synchronizer'
            
            response = self.session.get(sync_url, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()
            
            tokens = response.json()
            self._credentials = {
                'synchronizer_token': tokens['synchronizerToken'],
                'synchronizer_uri': tokens['synchronizerUri'],
                'uuid': self._uuid
            }
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Failed to authenticate: {str(e)}")
    
    def _refresh_credentials(self) -> None:
        """
        Refresh authentication tokens if they've expired.
        
        Raises:
            NotePublisherError: If credentials cannot be refreshed
        """
        try:
            # Preserve the session but refresh authentication
            self._authenticate()
        except Exception as e:
            raise NotePublisherError(f"Failed to refresh credentials: {str(e)}")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make an authenticated request to the API with automatic token refresh.
        
        Args:
            method: HTTP method
            endpoint: API endpoint (should include ClipServ/ if needed)
            **kwargs: Additional request parameters
            
        Returns:
            Response object
            
        Raises:
            NotePublisherError: If request fails
        """
        # Construct URL - if endpoint doesn't start with ClipServ and URL doesn't contain it, add it
        if endpoint.startswith('ClipServ/') or 'ClipServ' in self._url:
            url = f'{self._url}{endpoint}'
        else:
            url = f'{self._url}ClipServ/{endpoint}'
        
        # Set default timeout if not provided
        kwargs.setdefault('timeout', self.DEFAULT_TIMEOUT)
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Handle authentication errors
            if response.status_code == 401:
                self._refresh_credentials()
                response = self.session.request(method, url, **kwargs)
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.HTTPError as e:
            # For debugging 500 errors, try to get more info
            if e.response.status_code == 500:
                error_detail = f"Server Error (500): {e.response.text if e.response.text else 'No details available'}"
                raise NotePublisherError(error_detail)
            raise NotePublisherError(f"HTTP Error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise NotePublisherError(f"Request failed: {str(e)}")
        

    # def __init__(self, config_dir: Union[str, Path] = None, environment: str = 'bbg'):
    #     """
    #     Initialize NotePublisher with configuration
        
    #     Args:
    #         config_dir: Path to configuration directory
    #         environment: Environment name (e.g., 'bbg', 'development')
            
    #     Raises:
    #         NotePublisherError: If initialization fails
    #     """
    #     if config_dir is None:
    #         from . import CONFIG_DIR
    #         self.config_dir = CONFIG_DIR
    #     else:
    #         self.config_dir = Path(config_dir)
            
    #     self.environment = environment
    #     self.session = requests.Session()
        
    #     # Initialize configuration
    #     self._config = {}
    #     self._credentials = {}
    #     self._firm_configs = {
    #         'shareable': ['BLOOMBERG'],
    #         'tagged': ['Bloomberg']
    #     }
        
    #     try:
    #         self._load_configuration()
    #         self._authenticate()
    #     except Exception as e:
    #         raise NotePublisherError(f"Failed to initialize: {str(e)}")
    
    # def _load_configuration(self) -> None:
    #     """Load configuration from JSON files"""
    #     try:
    #         # Load base configuration
    #         base_config_path = self.config_dir / 'rms_config.json'
    #         with open(base_config_path, 'r') as f:
    #             config = json.load(f)
            
    #         # Load environment-specific configuration
    #         env_config_path = self.config_dir / f'rms_config.{self.environment}.json'
    #         if env_config_path.exists():
    #             with open(env_config_path, 'r') as f:
    #                 env_config = json.load(f)
    #             config.update(env_config)
            
    #         # Validate configuration
    #         required_keys = {'key', 'uuid', 'url'}
    #         missing_keys = required_keys - set(config.keys())
    #         if missing_keys:
    #             raise ConfigurationError(f"Missing required config keys: {missing_keys}")
            
    #         self._config = config
            
    #     except json.JSONDecodeError as e:
    #         raise ConfigurationError(f"Invalid JSON in config file: {str(e)}")
    #     except OSError as e:
    #         raise ConfigurationError(f"Could not read config file: {str(e)}")
    
    # def _authenticate(self) -> None:
    #     """Authenticate with Bloomberg API and get tokens"""
    #     try:
    #         # Set up session headers
    #         self.session.headers.update({
    #             'Cookie': f'BBCLIPSESSION={self._config["key"]}'
    #         })
            
    #         # Get synchronizer tokens
    #         response = self.session.get(
    #             f'{self.BASE_URL}ClipServ/upload/synchronizer',
    #             timeout=self.DEFAULT_TIMEOUT
    #         )
    #         response.raise_for_status()
            
    #         tokens = response.json()
    #         self._credentials = {
    #             'synchronizer_token': tokens['synchronizerToken'],
    #             'synchronizer_uri': tokens['synchronizerUri'],
    #             'uuid': self._config['uuid']
    #         }
            
    #     except requests.exceptions.RequestException as e:
    #         raise AuthenticationError(f"Failed to authenticate: {str(e)}")

    
    def prepare_attachment(self, file_path: str) -> NoteAttachment:
        """
        Prepare a file for attachment to a note
        
        Args:
            file_path: Path to the file to attach
            
        Returns:
            NoteAttachment object with attachment ID
            
        Raises:
            NotePublisherError: If attachment preparation fails
        """
        attachment = NoteAttachment(file_path=file_path)
        
        try:
            # Read and encode file
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            encoded_content = base64.b64encode(file_content)
            attachment.file_size = len(encoded_content)
            
            # Prepare attachment
            response = self._make_request(
                'POST',
                'upload/prepareAttachment',
                data={
                    'uuid': self._credentials['uuid'],
                    'SYNCHRONIZER_TOKEN': self._credentials['synchronizer_token'],
                    'SYNCHRONIZER_URI': self._credentials['synchronizer_uri'],
                    'filesize': attachment.file_size,
                    'filename': Path(file_path).name
                }
            )
            
            result = response.json()
            attachment.attachment_id = result['attachmentId']
            part_size = result.get('partSize', self.DEFAULT_PART_SIZE)
            
            # Upload in chunks
            chunks = [
                encoded_content[i:i+part_size]
                for i in range(0, len(encoded_content), part_size)
            ]
            
            for part_index, chunk in enumerate(chunks):
                self._make_request(
                    'POST',
                    'upload/uploadAttachmentPart',
                    data={
                        'uuid': self._credentials['uuid'],
                        'SYNCHRONIZER_TOKEN': self._credentials['synchronizer_token'],
                        'SYNCHRONIZER_URI': self._credentials['synchronizer_uri'],
                        'attachmentId': attachment.attachment_id,
                        'partIndex': part_index,
                        'partData': chunk
                    }
                )
            
            return attachment
            
        except OSError as e:
            raise NotePublisherError(f"Failed to read file {file_path}: {str(e)}")
    
    def _search_entity(self, search_term: str, entity_type: str, endpoint: str) -> List[Dict[str, Any]]:
        """
        Generic method to search for entities
        
        Args:
            search_term: Search term
            entity_type: Type of entity to search for
            endpoint: API endpoint for search
            
        Returns:
            List of matching entities
        """
        response = self._make_request(
            'GET',
            endpoint,
            params={
                'sub': search_term,
                'uuid': self._credentials['uuid']
            }
        )
        
        data = response.json()
        return data.get(entity_type, [])
    
    def find_community(self, name: str) -> Optional[CMTY]:
        """Find a community by name"""
        results = self._search_entity(name, 'COMMUNITIES', 'upload/getSharesAutocomplete')
        
        for item in results:
            if item['key'] == name:
                item['type'] = 'COMMUNITIES'
                return CMTY(**item)
        
        return None
    
    def find_user(self, user_name: str, user_type: UserType) -> Optional[BBG_USER]:
        """Find a user by name and type"""
        if user_type == UserType.WORKGROUPS:
            endpoint = 'upload/getSharesAutocomplete'
            results = self._search_entity(user_name, user_type.value, endpoint)
            
            # Filter for valid workgroup users
            valid_firms = self._firm_configs['shareable'] + [user_name]
            for item in results:
                if (item.get('subtype') == 'UUID' and 
                    (item['description'] == user_name.title() or
                     (item['key'] == user_name.upper() and 
                      any(firm in item['description'] for firm in valid_firms)))):
                    item['type'] = user_type.value
                    return BBG_USER(**item)
        else:
            endpoint = 'upload/getTagsAutocomplete'
            results = self._search_entity(user_name, user_type.value, endpoint)
            
            # Filter for valid tagged users
            valid_firms = self._firm_configs['tagged'] + [user_name]
            for item in results:
                if (item['key'] == user_name.title() and 
                    any(firm in item['description'] for firm in valid_firms)):
                    item['type'] = user_type.value
                    return BBG_USER(**item)
        
        return None
    
    def find_taglist(self, taglist_name: str, enum_value: str) -> Optional[TAGLIST]:
        """Find a taglist enumeration"""
        results = self._search_entity(taglist_name, 'CUSTOM', 'upload/getTagsAutocomplete')
        results += self._search_entity(enum_value, 'CUSTOM', 'upload/getTagsAutocomplete')
        
        for item in results:
            if item['key'] == enum_value and item['description'] == taglist_name:
                item['type'] = 'CUSTOM'
                return TAGLIST(**item)
        
        return None
    
    def find_security(self, security_name: str) -> Optional[NOTE_SECURITY]:
        """Find a security by name"""
        results = self._search_entity(security_name, 'SECURITIES', 'upload/getTagsAutocomplete')
        
        for item in results:
            if item['key'] == security_name:
                item['type'] = 'SECURITIES'
                return NOTE_SECURITY(**item)
        
        return None
    
    def find_corp_ticker(self, ticker: str) -> Optional[NOTE_SECURITY]:
        """
        Find a corporate ticker
        
        Args:
            ticker: Ticker symbol (e.g., 'AAL' or 'AAL CORP')
            
        Returns:
            NOTE_SECURITY object or None
        """
        # Normalize ticker format
        ticker = ticker.upper()
        ticker_parts = ticker.split()
        
        # Validate ticker format
        if len(ticker_parts) > 2 or (len(ticker_parts) == 2 and 'CORP' not in ticker_parts):
            raise ValidationError(
                "Invalid corp ticker format. Use 'TICKER' or 'TICKER CORP'"
            )
        
        # Extract base ticker
        base_ticker = ticker_parts[0] if ticker_parts[0] != 'CORP' else ticker_parts[1]
        
        results = self._search_entity(ticker, 'SECURITIES', 'upload/getTagsAutocomplete')
        
        for item in results:
            if (item.get('metadata') == base_ticker and 
                item.get('subtype') == 'CORP'):
                item['type'] = 'SECURITIES'
                return NOTE_SECURITY(**item)
        
        return None
    
    def create_note(
        self,
        title: str,
        body: str,
        as_of_date: int,
        tags: Optional[List[BaseEntity]] = None,
        share_with: Optional[List[BaseEntity]] = None,
        attachments: Optional[List[str]] = None,
        html_body: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create and publish a note
        
        Args:
            title: Note title
            body: Note body text
            as_of_date: Date as Unix timestamp in milliseconds
            tags: List of tag entities
            share_with: List of shareable entities
            attachments: List of file paths to attach
            html_body: Optional HTML body
            
        Returns:
            API response
            
        Raises:
            NotePublisherError: If note creation fails
        """
        # Prepare attachments
        attachment_ids = []
        if attachments:
            for file_path in attachments:
                attachment = self.prepare_attachment(file_path)
                attachment_ids.append(attachment.attachment_id)
        
        # Build note payload
        note_data = {
            "title": title,
            "body": body,
            "date": as_of_date,
            "tags": [tag.model_dump() for tag in (tags or [])],
            "shareables": [entity.model_dump() for entity in (share_with or [])],
            "attachments": attachment_ids
        }
        
        if html_body:
            note_data["htmlBody"] = html_body
        
        # Create note - Bloomberg expects URL-encoded JSON in the URL itself
        encoded_data = urllib.parse.quote(json.dumps(note_data))
        
        # Build the complete URL with all parameters
        # Use the same URL logic as in _make_request
        if 'ClipServ' in self._url:
            base_url = f'{self._url}upload/createNote'
        else:
            base_url = f'{self._url}ClipServ/upload/createNote'
            
        url = (f'{base_url}?'
               f'uuid={self._credentials["uuid"]}&'
               f'doc={encoded_data}&'
               f'SYNCHRONIZER_TOKEN={self._credentials["synchronizer_token"]}&'
               f'SYNCHRONIZER_URI={self._credentials["synchronizer_uri"]}')
        
        # Make the POST request directly to the constructed URL
        try:
            response = self.session.post(url, timeout=self.DEFAULT_TIMEOUT)
            
            # Handle authentication errors
            if response.status_code == 401:
                self._refresh_credentials()
                response = self.session.post(url, timeout=self.DEFAULT_TIMEOUT)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise NotePublisherError(f"Failed to create note: {str(e)}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close session"""
        self.session.close()
    
    def close(self):
        """Close the session"""
        self.session.close()
    
    def __del__(self) -> None:
        """
        Cleanup method to ensure the session is closed when the object is destroyed
        """
        if hasattr(self, 'session'):
            self.session.close()