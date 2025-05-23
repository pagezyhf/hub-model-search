from typing import Dict, List, Any
from huggingface_hub import HfApi
from src.config import SearchConfig
from src.providers import Provider
import pandas as pd
from pathlib import Path

class ModelSearcher:
    def __init__(self, provider: Provider, search: SearchConfig, output_dir: str = "output"):
        self.search = search
        self.provider = provider
        self.api = HfApi(token="")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def search_models(self) -> List[Dict[str, Any]]:
        all_models = []

        for scenario_name, scenario_conf in self.search.scenarios.items():
                models = self._search_with_config(scenario_name, scenario_conf)
                all_models.extend(models)
    
        self.models = all_models
    
    def save(self):
        df = pd.DataFrame(self.models)
        for column in df.columns:
            df[column] = df[column].apply(lambda x: tuple(x) if isinstance(x, list) else x)
        df.drop_duplicates(subset='modelId', keep='first', inplace=True) # keep first iteration of duplicates
        output_file = self.output_dir / f"{self.provider.name}_model_results.csv"
        df.to_csv(output_file, index=False)
        
    def _search_with_config(self, name, scenario_conf: Dict[str, Any]) -> List[Dict[str, Any]]:
            
        base_params = {
            "sort": scenario_conf["sort"],
            "direction": scenario_conf["direction"],
            "filter": scenario_conf.get("filter"),
        }
        
        all_models = []
        tasks = scenario_conf.get("tasks", [None])
        tags = scenario_conf.get("tags", [None])
        
        # Do cartesian product of tasks and tags
        for task in tasks:
            for tag in tags:
                search_params = base_params.copy()
                if task:
                    search_params["task"] = task
                if tag:
                    search_params["tags"] = tag
                    
                models = self.api.list_models(**search_params, limit = self.search.limit)
                
                # Add compatibility information
                for model in models:
                    model_info = {
                        'modelId': model.modelId,
                        'search_task': task,
                        'search_tag': tag, 
                        'search_scenario': name,
                        'downloads': model.downloads,
                        'likes': model.likes,
                        'tags': model.tags,
                        'pipeline_tag': model.pipeline_tag,
                        'library_name': model.library_name,
                        'license': [tag for tag in model.tags if tag.startswith("license:")],
                    }
                    model_info[f"{self.provider.name}_compatible"] = self.provider.check_compatibility(model_info)
                    all_models.append(model_info)
                    
        return all_models 