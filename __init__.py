# from pathlib import Path

# # Export the root directory path
# BLOOMBERG_APIS_ROOT = Path(__file__).parent.absolute()

# # Import and expose the RMS API functionality
# from .rms_api import (
#     initialize_rmsbql_client,
#     initialize_docretrieval_client,
#     initialize_clients
# )

from pathlib import Path

# Export the root directory path
BLOOMBERG_APIS_ROOT = Path(__file__).parent.absolute()

# Import and expose the RMS API functionality
from .rms_api import (
    RMSBQL,
    DocumentRetriever,
    CDEUploader,
    NotePublisher,
    initialize_rmsbql_client,
    initialize_docretrieval_client,
    initialize_cdeuploader_client,
    initialize_notepublisher_client,
    initialize_clients,
    get_config_dir
)
