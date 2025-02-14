import argparse
from src.config import Config
from src.searcher import ModelSearcher
from src.aggregator import ModelAggregator
from src.providers.gcp import GCPProvider
from src.providers.aws import AWSProvider

def parse_args():
    parser = argparse.ArgumentParser(description="Model Selection Tool")
    parser.add_argument("--provider", type=str, default="gcp,aws",
                      help="Comma-separated list of providers (gcp,aws)")
    parser.add_argument("--scenario", type=str, default="all",
                      help="Search scenario (trending,most_used,overall,finance,healthcare,retail,all)")
    parser.add_argument("--limit", type=int,
                      help="Number of models to retrieve (default: from config)")
    return parser.parse_args()

def main():
    args = parse_args()
    config = Config()
    aggregator = ModelAggregator()

    providers = args.provider.split(",")
    scenarios = args.scenario.split(",")

    provider_classes = {
        "gcp": GCPProvider,
        "aws": AWSProvider
    }

    for provider_name in providers:
        provider_config = config.get_provider_config(provider_name)
        provider = provider_classes[provider_name](provider_config)
        searcher = ModelSearcher(provider, config)

        all_models = []
        for scenario in scenarios:
            models = searcher.search_models(
                scenario=scenario,
                limit=args.limit
            )
            all_models.extend(models)

        aggregator.aggregate_to_csv(all_models, provider_name)

if __name__ == "__main__":
    main() 