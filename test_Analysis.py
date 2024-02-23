import pytest
from Analysis import Analysis
from unittest.mock import MagicMock

def test_load_data(mocker):
    # Create an instance of the Analysis class
    analysis_obj = Analysis(analysis_config='config.yml')

    # Mocking the requests.get function using pytest-mock
    mocker.patch('Analysis.requests.get', return_value=MagicMock(json=lambda: {'artists': {'items': [{'name': 'Artist1', 'popularity': 80}, {'name': 'Artist2', 'popularity': 75}, {'name': 'Artist3', 'popularity': 90}]}}))

    # Call the load_data method
    analysis_obj.load_data()

    # Check if data is loaded correctly
    assert analysis_obj.data == {'artists': {'items': [{'name': 'Artist1', 'popularity': 80}, {'name': 'Artist2', 'popularity': 75}, {'name': 'Artist3', 'popularity': 90}]}}