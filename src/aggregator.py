import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

class ModelAggregator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def aggregate_to_csv(self, models: List[Dict[str, Any]], provider: str):
        if not models:
            return

        df = pd.DataFrame(models)
        
        # Ensure compatibility column is present
        compatibility_col = f"{provider}_compatible"
        if compatibility_col not in df.columns:
            df[compatibility_col] = False
            
        # Reorder columns to put compatibility information near the front
        cols = df.columns.tolist()
        cols.insert(1, cols.pop(cols.index(compatibility_col)))
        df = df[cols]
        
        output_file = self.output_dir / f"model_results.csv"
        
        # If file exists, append to it, otherwise create new
        if output_file.exists():
            existing_df = pd.read_csv(output_file)
            df = pd.concat([existing_df, df], ignore_index=True)
            df = df.drop_duplicates(subset=['modelId'], keep='last')
            
        df.to_csv(output_file, index=False) 