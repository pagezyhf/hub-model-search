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

    def search_models(self, scenario: str, industry: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        scenario_config = self.config.get_scenario_config(scenario)
        search_params = {
            "limit": limit,
            "sort": scenario_config.get("sort", "downloads"),
            "direction": scenario_config.get("direction", -1)
        }

        if industry:
            industry_config = self.config.get_industry_config(industry)
            if industry_config.get("tags"):
                search_params["tags"] = industry_config["tags"]
            if industry_config.get("tasks"):
                search_params["task"] = industry_config["tasks"]

        models = self.api.list_models(**search_params)
        
        # Add compatibility information
        enriched_models = []
        for model in models:
            # Convert ModelInfo to dictionary with only relevant fields
            model_info = {
                'modelId': model.modelId,
                'lastModified': model.lastModified,
                'tags': model.tags,
                'pipeline_tag': model.pipeline_tag,
                'library_name': model.library_name,
                'downloads': model.downloads,
                'likes': model.likes
            }
            model_info[f"{self.provider.name}_compatible"] = self.provider.check_compatibility(model_info)
            enriched_models.append(model_info)
            
        return enriched_models 