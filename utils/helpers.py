"""
Helper Functions
General utility functions for test automation.
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


def get_timestamp(format: str = "%Y%m%d_%H%M%S") -> str:
    """
    Get current timestamp in specified format.
    
    Args:
        format: Timestamp format string
        
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(format)


def ensure_directory_exists(directory_path: str):
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory_path: Path to directory
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def save_json(data: Dict[str, Any], file_path: str):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Path to JSON file
    """
    ensure_directory_exists(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load data from YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Loaded data
    """
    import yaml

    with open(file_path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load data from JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Loaded data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_env_variable(key: str, default: str = None) -> str:
    """
    Get environment variable value.
    
    Args:
        key: Environment variable key
        default: Default value if key not found
        
    Returns:
        Environment variable value
    """
    return os.environ.get(key, default)


def clean_old_files(directory: str, days: int = 7):
    """
    Clean files older than specified days.
    
    Args:
        directory: Directory to clean
        days: Number of days threshold
    """
    if not os.path.exists(directory):
        return
    
    now = datetime.now()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            if (now - file_modified).days > days:
                os.remove(file_path)

