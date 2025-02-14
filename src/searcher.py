from typing import Dict, List, Any, Protocol
from huggingface_hub import HfApi

class Provider(Protocol):
    """Protocol defining the interface for cloud providers"""
    name: str
    def check_compatibility(self, model_info: Dict[str, Any]) -> bool: ...

class ModelSearcher:
    def __init__(self, provider: Provider, config: Dict[str, Any]):
        self.provider = provider
        self.config = config
        self.api = HfApi()

    def search_models(self, scenario: str, limit: int = None) -> List[Dict[str, Any]]:
        scenario_config = self.config.get_scenario_config(scenario)
        
        # If scenario is "all", merge results from all scenarios
        if scenario == "all":
            all_models = []
            all_scenarios = self.config.scenarios.get("scenarios", {})
            # Skip the "all" scenario itself when processing all scenarios
            for scenario_name, scenario_conf in all_scenarios.items():
                models = self._search_with_config(scenario_conf, limit)
                all_models.extend(models)
            return all_models
            
        # Single scenario search
        return self._search_with_config(scenario_config, limit)
        
    def _search_with_config(self, config: Dict[str, Any], limit: int = None) -> List[Dict[str, Any]]:
        if not config.get("sort") or "direction" not in config:
            raise ValueError("Scenario must specify 'sort' and 'direction'")
            
        base_params = {
            "limit": limit or self.config.scenarios.get("default_limit", 10),
            "sort": config["sort"],
            "direction": config["direction"]
        }
        
        all_models = []
        tasks = config.get("tasks", [None])
        tags = config.get("tags", [None])
        
        # Do cartesian product of tasks and tags
        for task in tasks:
            for tag in tags:
                search_params = base_params.copy()
                if task:
                    search_params["task"] = task
                if tag:
                    search_params["tags"] = tag
                    
                models = self.api.list_models(**search_params)
                
                # Add compatibility information
                for model in models:
                    model_info = {
                        'modelId': model.modelId,
                        'tags': model.tags,
                        'pipeline_tag': model.pipeline_tag,
                        'library_name': model.library_name,
                        'downloads': model.downloads,
                        'likes': model.likes,
                        'search_task': task,
                        'search_tag': tag
                    }
                    model_info[f"{self.provider.name}_compatible"] = self.provider.check_compatibility(model_info)
                    all_models.append(model_info)
                    
        return all_models 