import argparse
from src.config import SearchConfig, ProviderConfig
from src.searcher import ModelSearcher

def parse_args():
    parser = argparse.ArgumentParser(description="Model Selection Tool")
    parser.add_argument("--provider", type=str, default="gcp,aws",
                      help="Comma-separated list of providers (gcp,aws)")
    parser.add_argument('--search_scenario_file', type=str, default='configs/search_scenarios.yaml', 
                        help='Name of the YAML file containing search scenarios.')
    return parser.parse_args()

def main():
    args = parse_args()
    search = SearchConfig(args.search_scenario_file)

    providers = args.provider.split(",")

    for provider_name in providers:
        provider = ProviderConfig(provider_name).get_provider_instance()

        searcher = ModelSearcher(provider, search)
        searcher.search_models()
        searcher.save()

if __name__ == "__main__":
    main()