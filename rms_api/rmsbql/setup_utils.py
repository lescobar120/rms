# rms_api/rmsbql/setup_utils.py

import sys
from pathlib import Path

def find_project_root(current_dir: Path = None) -> Path:
    """
    Find the project root directory by looking for the __init__.py file
    that marks the rms_api package root.
    
    Args:
        current_dir: Directory to start searching from. Defaults to current directory.
        
    Returns:
        Path to the project root directory
        
    Raises:
        FileNotFoundError: If project root cannot be found
    """
    if current_dir is None:
        current_dir = Path().absolute()
    
    # Look for __init__.py in parent directories
    current_path = current_dir
    while current_path.parent != current_path:  # Stop at root directory
        if (current_path / '__init__.py').exists() and current_path.name == 'rms_api':
            return current_path
        current_path = current_path.parent
        
    raise FileNotFoundError(
        "Could not find project root directory (rms_api). "
        "Make sure you're running this from within the project structure."
    )

def setup_rms_api_imports():
    """
    Set up the Python path to allow imports from rms_api package.
    This function will work from any depth in the directory structure.
    
    Returns:
        Path to the project root directory
    """
    # Find the project root
    project_root = find_project_root()
    
    # Get the parent directory of the project root
    parent_dir = project_root.parent
    
    # Add to Python path if not already there
    if str(parent_dir) not in sys.path:
        sys.path.append(str(parent_dir))
        print(f"Added {parent_dir} to Python path")
    
    return project_root

def get_relative_notebook_path():
    """
    Get the relative path of the current notebook from the project root.
    Useful for understanding where you are in the project structure.
    
    Returns:
        Path object representing the relative path
    """
    current_dir = Path().absolute()
    project_root = find_project_root()
    return current_dir.relative_to(project_root)