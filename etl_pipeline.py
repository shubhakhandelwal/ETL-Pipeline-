import requests
import pandas as pd

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_FILE = "transformed_users.csv"

def extract_data(url: str) -> list:
    """Fetches data from the REST API."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an error for bad HTTP responses
    return response.json()

def transform_data(raw_data: list) -> pd.DataFrame:
    """Transforms raw API JSON data into a cleaned pandas DataFrame."""
    if not raw_data:
        return pd.DataFrame()
    
    # Extract and flatten relevant fields
    flattened_data = []
    for item in raw_data:
        user_info = {
            "user_id": item.get("id"),
            "name": item.get("name"),
            "username": item.get("username"),
            "email": item.get("email") if item.get("email") else None,
            "city": item.get("address", {}).get("city"),
            "company_name": item.get("company", {}).get("name")
        }
        flattened_data.append(user_info)
        
    df = pd.DataFrame(flattened_data)
    
    # Data Cleaning / Standardization
    df["email"] = df["email"].str.lower()
    
    return df

def load_data(df: pd.DataFrame, output_path: str) -> None:
    """Saves DataFrame to a CSV file."""
    if df.empty:
        raise ValueError("Cannot load empty DataFrame to CSV.")
    df.to_csv(output_path, index=False)

def run_pipeline(url: str = API_URL, output_path: str = OUTPUT_FILE):
    """Executes the complete ETL pipeline."""
    print("Starting ETL pipeline...")
    data = extract_data(url)
    df = transform_data(data)
    load_data(df, output_path)
    print(f"ETL pipeline completed successfully. Saved to {output_path}")

if __name__ == "__main__":
    run_pipeline()