import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.scenarios = self._load_yaml("search_scenarios.yaml")
        self.industries = self._load_yaml("industries.yaml")
        self.providers = self._load_providers()

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        with open(self.config_dir / filename, 'r') as f:
            return yaml.safe_load(f)

    def _load_providers(self) -> Dict[str, Any]:
        providers = {}
        provider_dir = self.config_dir / "providers"
        for provider_file in provider_dir.glob("*.yaml"):
            provider_config = self._load_yaml(f"providers/{provider_file.name}")
            providers[provider_file.stem] = provider_config
        return providers

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        return self.providers.get(provider, {})

    def get_scenario_config(self, scenario: str) -> Dict[str, Any]:
        return self.scenarios.get("scenarios", {}).get(scenario, {})

    def get_industry_config(self, industry: str) -> Dict[str, Any]:
        return self.industries.get("industries", {}).get(industry, {}) 