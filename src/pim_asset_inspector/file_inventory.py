from pathlib import Path



def inventory_files(asset_folder: Path) -> list[Path]:
    """Return a list of files from an asset folder."""

    if not asset_folder.exists():
        raise FileNotFoundError(f"Asset folder not found:  {asset_folder}")
    
    if not asset_folder.is_dir():
        raise NotADirectoryError(f"Asset path is not a folder: {asset_path}")
    
    return [
        file_path
        for file_path in asset_folder.iterdir()
        if file_path.is_file()
    ]