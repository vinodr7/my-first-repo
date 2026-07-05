import json
import pickle
import pandas as pd
import requests

class DataIngestor:
    """A unified manager to source data from various local and remote formats."""
    
    def __init__(self):
        # Setting up standard session configuration for API calls
        self.session = requests.Session()

    # --- 1. Tabular Formats ---
    
    def read_csv(self, file_path, **kwargs):
        """Reads a CSV file into a Pandas DataFrame."""
        try:
            print(f"[CSV] Reading: {file_path}")
            return pd.read_csv(file_path, **kwargs)
        except Exception as e:
            print(f"[Error] CSV ingestion failed: {e}")
            return None

    def read_excel(self, file_path, sheet_name=0, **kwargs):
        """Reads an Excel file (.xlsx) into a Pandas DataFrame."""
        try:
            print(f"[Excel] Reading: {file_path} | Sheet: {sheet_name}")
            # Uses openpyxl engine automatically behind the scenes
            return pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
        except Exception as e:
            print(f"[Error] Excel ingestion failed: {e}")
            return None

    # --- 2. Semi-Structured & Serialized Formats ---

    def read_json(self, file_path):
        """Parses a local JSON file into native Python dictionaries or lists."""
        try:
            print(f"[JSON] Reading: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Error] JSON ingestion failed: {e}")
            return None

    def read_pickle(self, file_path):
        """Deserializes local Python objects from a binary pickle file."""
        try:
            print(f"[Pickle] Reading: {file_path}")
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"[Error] Pickle ingestion failed: {e}")
            return None

    # --- 3. Remote Web API Ingestion ---

    def read_api(self, url, method="GET", params=None, json_payload=None, headers=None):
        """
        Fetches data from an external REST API endpoint.
        Supports automatic JSON decoding.
        """
        try:
            print(f"[API] Fetching: {url} ({method})")
            
            # Dynamically switch between standard HTTP verbs
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json_payload,
                headers=headers,
                timeout=10 # Prevents your program from hanging indefinitely
            )
            
            # Throws an HTTPError if the remote server returned an error code (4xx, 5xx)
            response.raise_for_status()
            
            # Attempt to return decoded JSON; fallback to text if not JSON
            try:
                return response.json()
            except ValueError:
                return response.text
                
        except requests.exceptions.RequestException as e:
            print(f"[Error] API request failed: {e}")
            return None

# ==========================================
# HOW TO USE THE FRAMEWORK
# ==========================================
if __name__ == "__main__":
    # Create sample assets to run locally immediately
    setup_sample_data()
    
    # 1. Initialize the framework
    ingestor = DataIngestor()
    
    # 2. Extract Data from Tabular Files (Returns DataFrames)
    csv_df = ingestor.read_csv("sample.csv")
    excel_df = ingestor.read_excel("sample.xlsx")
    
    # 3. Extract Data from Structured/Binary Files (Returns Dicts/Lists)
    json_data = ingestor.read_json("sample.json")
    pickle_data = ingestor.read_pickle("sample.pkl")
    
    # 4. Extract Data from an API Endpoint (Returns Dict/List or Text)
    # Using a free public testing API endpoint
    api_endpoint = "https://typicode.com"
    api_data = ingestor.read_api(api_endpoint)
    
    # Quick sanity check printouts
    print("\n--- INGESTION RESULTS CHECK ---")
    print(f"CSV Loaded Rows: {len(csv_df) if csv_df is not None else 0}")
    print(f"JSON Structure Type: {type(json_data)}")
    print(f"API Extracted Title: {api_data.get('title') if isinstance(api_data, dict) else 'N/A'}")


def setup_sample_data():
    """Helper setup script to ensure code executes without missing dependencies."""
    mock_dict = {"status": "success", "framework": "DataIngestorV1", "active": True}
    
    # Save local JSON & Pickle
    with open("sample.json", "w") as f:
        json.dump(mock_dict, f)
    with open("sample.pkl", "wb") as f:
        pickle.dump(mock_dict, f)
        
    # Save local CSV & Excel
    df = pd.DataFrame([{"A": 1, "B": 2}, {"A": 3, "B": 4}])
    df.to_csv("sample.csv", index=False)
    df.to_excel("sample.xlsx", index=False)
