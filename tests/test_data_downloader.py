# tests/test_data_downloader.py
import pytest
from unittest.mock import patch, MagicMock
from src.data.data_downloader import download_file, extract_data, cleanup_downloaded_file
from src.utils.config import Config
import os

@patch('src.data.data_downloader.gdown.download')
@patch('src.data.data_downloader.os.path.getsize')
def test_download_file(mock_getsize, mock_download):
    mock_getsize.return_value = 1024 * 1024  # 1 MB
    download_file()
    mock_download.assert_called_once_with(f"https://drive.google.com/uc?id={Config.FILE_ID}", Config.OUTPUT_ZIP, quiet=False)

@patch('src.data.data_downloader.zipfile.ZipFile')
def test_extract_data(mock_zipfile):
    mock_zipfile.return_value.__enter__.return_value.extractall.return_value = None
    extract_data()
    mock_zipfile.assert_called_once_with(Config.OUTPUT_ZIP, 'r')

@patch('src.data.data_downloader.os.remove')
@patch('src.data.data_downloader.os.path.exists')
def test_cleanup_downloaded_file(mock_exists, mock_remove):
    mock_exists.return_value = True
    cleanup_downloaded_file()
    mock_remove.assert_called_once_with(Config.OUTPUT_ZIP)