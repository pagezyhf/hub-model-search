import yaml
from pathlib import Path
from typing import Dict, Any
from src.providers import AWSProvider, GCPProvider, AzureProvider

PROVIDERS_MAP = {
    'aws': AWSProvider,
    'gcp': GCPProvider,
    'azure': AzureProvider
}

def load_yaml(self, filename: str) -> Dict[str, Any]:
    with open(self.config_dir / filename, 'r') as f:
        return yaml.safe_load(f)

class SearchConfig:
    def __init__(self, search_scenario: str = "configs/search_scenarios.yaml"):
        self.config_dir = Path(__file__).resolve().parent.parent
        self.configs = self._load_yaml(search_scenario)
        self.limit = self.configs.get("default_limit", 10)
        self.scenarios = self.configs.get("scenarios", [])

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        with open(self.config_dir / filename, 'r') as f:
            return yaml.safe_load(f)
    
    def _validate_scenario(scenario):
        required_keys = ['sort', 'direction']
        for key in required_keys:
            if key not in scenario:
                raise ValueError(f"Scenario missing required key: {key}")

    def get_scenarios_config(self) -> Dict[str, Any]:
        for scenario in self.scenarios:
            self._validate_scenario(scenario)
        return self.scenarios.get("scenarios", {})
    
class ProviderConfig:
    def __init__(self, provider_name: str):
        self.config_dir = Path(__file__).resolve().parent.parent
        self.provider_name = provider_name
        self.providers = self._load_providers()

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        with open(self.config_dir / filename, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_providers(self) -> Dict[str, Any]:
        providers = {}
        provider_dir = self.config_dir / "configs" / "providers"
        for provider_file in provider_dir.glob("*.yaml"):
            provider_config = self._load_yaml(f"configs/providers/{provider_file.name}")
            providers[provider_file.stem] = provider_config
        return providers

    def get_provider_instance(self):
        provider_config = self.providers.get(self.provider_name, {})
        provider_instance = PROVIDERS_MAP[self.provider_name](provider_config)
        return provider_instance