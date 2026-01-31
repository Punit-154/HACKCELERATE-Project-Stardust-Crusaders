"""
Universal Data Loader
Supports multiple file formats (CSV, JSON, Excel, XML) and data sources
"""

import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional
import glob


class UniversalDataLoader:
    """Load data from multiple sources and formats"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize with configuration file"""
        if config_path is None:
            # Check current directory first
            current_dir = Path(__file__).resolve().parent
            local_config = current_dir / "data_config.json"
            
            if local_config.exists():
                config_path = local_config
                self.base_dir = current_dir
            else:
                # Fallback to original logic
                base_dir = Path(__file__).resolve().parents[2]
                config_path = base_dir / "data" / "config" / "data_config.json"
                self.base_dir = base_dir
        else:
            self.base_dir = Path(config_path).parent

        if not Path(config_path).exists():
             raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, 'r') as f:
            self.config = json.load(f)
    
    def load_csv(self, file_path: Path) -> pd.DataFrame:
        """Load CSV file"""
        return pd.read_csv(file_path)
    
    def load_json(self, file_path: Path) -> pd.DataFrame:
        """Load JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    
    def load_excel(self, file_path: Path) -> pd.DataFrame:
        """Load Excel file"""
        return pd.read_excel(file_path)
    
    def load_xml(self, file_path: Path) -> pd.DataFrame:
        """Load XML file and convert to DataFrame"""
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        data = []
        for child in root:
            record = {}
            for elem in child:
                record[elem.tag] = elem.text
            data.append(record)
        
        return pd.DataFrame(data)
    
    def load_file(self, file_path: Path) -> pd.DataFrame:
        """Auto-detect format and load file"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.csv':
            return self.load_csv(file_path)
        elif suffix == '.json':
            return self.load_json(file_path)
        elif suffix in ['.xlsx', '.xls']:
            return self.load_excel(file_path)
        elif suffix == '.xml':
            return self.load_xml(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def find_files(self, patterns: List[str]) -> List[Path]:
        """Find all files matching the given patterns"""
        files = []
        for pattern in patterns:
            full_pattern = str(self.base_dir / pattern)
            matched_files = glob.glob(full_pattern)
            files.extend([Path(f) for f in matched_files])
        
        return files
    
    def load_data_source(self, source_name: str) -> pd.DataFrame:
        """Load all data for a specific source (materials, transport, energy)"""
        if source_name not in self.config['data_sources']:
            raise ValueError(f"Unknown data source: {source_name}")
        
        source_config = self.config['data_sources'][source_name]
        
        if not source_config.get('enabled', True):
            print(f"[WARN] Data source '{source_name}' is disabled")
            return pd.DataFrame()
        
        # Find all matching files
        files = self.find_files(source_config['locations'])
        
        if not files:
            print(f"[WARN] No files found for data source '{source_name}'")
            return pd.DataFrame()
        
        # Load and combine all files
        all_data = []
        for file_path in files:
            try:
                print(f"[LOAD] Loading {file_path.name}...")
                df = self.load_file(file_path)
                
                # Add source file information
                df['_source_file'] = file_path.name
                all_data.append(df)
                
            except Exception as e:
                print(f"[ERROR] Error loading {file_path}: {e}")
        
        if not all_data:
            return pd.DataFrame()
        
        # Combine all dataframes
        combined_df = pd.concat(all_data, ignore_index=True)
        
        print(f"[OK] Loaded {len(combined_df)} records from {len(all_data)} file(s)")
        
        return combined_df
    
    def normalize_data(self, df: pd.DataFrame, source_name: str) -> pd.DataFrame:
        """Normalize data according to schema configuration"""
        schema = self.config['data_sources'][source_name]['schema']
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Create normalized dataframe with standard column names
        normalized = df.copy()
        
        # Map configured fields to standard names
        for standard_name, config_field in schema.items():
            if config_field in df.columns:
                # Keep original column but ensure it exists
                pass
            else:
                # Check if column exists with different case
                matching_cols = [col for col in df.columns if col.lower() == config_field.lower()]
                if matching_cols:
                    normalized.rename(columns={matching_cols[0]: config_field}, inplace=True)
        
        return normalized
    
    def load_all_sources(self) -> Dict[str, pd.DataFrame]:
        """Load all enabled data sources"""
        all_data = {}
        
        for source_name in self.config['data_sources'].keys():
            print(f"\n{'='*50}")
            print(f"Loading {source_name.upper()} data...")
            print(f"{'='*50}")
            
            df = self.load_data_source(source_name)
            
            if not df.empty:
                df = self.normalize_data(df, source_name)
                all_data[source_name] = df
        
        return all_data
    
    def get_schema(self, source_name: str) -> Dict[str, str]:
        """Get schema configuration for a data source"""
        return self.config['data_sources'][source_name]['schema']
    
    def get_emission_factors(self, category: str) -> Dict[str, str]:
        """Get emission factors for a category"""
        return self.config['emission_factors'].get(category, {})
    
    def get_api_config(self) -> Dict[str, str]:
        """Get API configuration"""
        return self.config['api']


# Test the loader
if __name__ == "__main__":
    print("[START] Testing Universal Data Loader\n")
    
    loader = UniversalDataLoader()
    
    # Load all data sources
    all_data = loader.load_all_sources()
    
    # Display summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    
    for source_name, df in all_data.items():
        print(f"\n{source_name.upper()}:")
        print(f"  Records: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        if not df.empty:
            print(f"  Preview:")
            print(df.head(2).to_string(index=False))
