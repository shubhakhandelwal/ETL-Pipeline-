import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from etl_pipeline import extract_data, transform_data, load_data

# Sample mock API response data
MOCK_API_RESPONSE = [
    {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz",
        "address": {"city": "Gwenborough"},
        "company": {"name": "Romaguera-Crona"}
    }
]

@patch("etl_pipeline.requests.get")
def test_extract_data_success(mock_get):
    """Test API data extraction when HTTP call is successful."""
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_API_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = extract_data("https://fakeapi.com")
    assert result == MOCK_API_RESPONSE
    mock_get.assert_called_once_with("https://fakeapi.com", timeout=10)

def test_transform_data():
    """Test data transformation and standardization logic."""
    df = transform_data(MOCK_API_RESPONSE)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "user_id" in df.columns
    assert df.loc[0, "city"] == "Gwenborough"
    # Ensure email normalization (lowercase) worked
    assert df.loc[0, "email"] == "sincere@april.biz" 

def test_load_data(tmp_path):
    """Test saving DataFrame to CSV file."""
    df = pd.DataFrame([{"user_id": 1, "name": "John Doe"}])
    output_file = tmp_path / "test_output.csv"
    
    load_data(df, str(output_file))
    
    assert output_file.exists()
    saved_df = pd.read_csv(output_file)
    assert len(saved_df) == 1
    assert saved_df.loc[0, "name"] == "John Doe"

def test_load_data_empty_raises_error(tmp_path):
    """Test that attempting to load an empty DataFrame raises an error."""
    empty_df = pd.DataFrame()
    output_file = tmp_path / "test_output.csv"
    
    with pytest.raises(ValueError, match="Cannot load empty DataFrame"):
        load_data(empty_df, str(output_file))