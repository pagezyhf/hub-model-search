# Hub Model Search

Aggregate and filter models from Hugging Face Hub based on a search scenario.

## TODO
1. Refactor to input a yaml to main.py instead of the actual nonsense
2. Work on a generic important_models.yaml search scenario for which we want to have CSP support / great doc
3. Work on a generic recommended_models.yaml to provide recommendations to CSP on their curated catalogs.
4. Add a component that can pull best models from leaderboards
5. Add a component that can pull from Merve's collections
6. Double check GCP compatibility and add AWS compatibility
7. Extract license from tags and add in the search results
8. Review README

## Features

1. **Provider-specific Model Selection**
   - Support for multiple cloud providers compatibility checks (GCP, AWS)

2. **Flexible Search Scenarios**
   - Trending models (sorted by trending score)
   - Most used models (sorted by downloads)
   - Industry-specific scenarios with customized tasks and tags:
     - Finance
     - Healthcare
     - Retail

3. **Configurable Architecture**
   - YAML-based configuration
   - Extensible provider system
   - Customizable search parameters

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Required dependencies:
- huggingface-hub: For accessing the Hugging Face model hub
- pyyaml: For configuration file parsing
- pandas: For data processing and CSV output

## Configuration

The tool uses YAML configuration files located in the `configs/` directory:

- `search_scenarios.yaml`: Define search scenarios with their parameters
- `providers/`: Provider-specific compatibility rules
  - `gcp.yaml`: Google Cloud Platform configuration
  - `aws.yaml`: Amazon Web Services configuration

### Search Scenarios Configuration

Each scenario in `search_scenarios.yaml` requires:
- `sort`: Field to sort results by (e.g., "downloads", "trendingScore")
- `direction`: Sort direction (-1 for descending, 1 for ascending)

Optional parameters:
- `tasks`: List of Hugging Face tasks to search for
- `tags`: List of tags to filter models

Example scenario configuration:
```yaml
finance:
  sort: "downloads"
  direction: -1
  tasks:
    - "text-classification"
    - "text-generation"
  tags:
    - "finance"
    - "fintech"
```

When both tasks and tags are specified, the tool performs searches for each combination of task and tag.

## Usage

Basic usage:

```bash
python main.py --provider gcp,aws --scenario trending --limit 10
```

### Command Line Arguments

- `--provider`: Comma-separated list of providers (gcp,aws)
- `--scenario`: Search scenario name or "all" for all scenarios (default: "all")
- `--limit`: Optional number of models to retrieve per search (default from config)

### Examples

1. Search trending models for GCP:
```bash
python main.py --provider gcp --scenario trending
```

2. Get finance-specific models for AWS:
```bash
python main.py --provider aws --scenario finance
```

3. Run all scenarios across providers:
```bash
python main.py --provider gcp,aws
```

## Output

The tool generates a consolidated CSV file in the `output/` directory with:
- Model ID
- Provider Compatibility (for each provider)
- Downloads
- Likes
- Tags
- Task
- Search Parameters Used (task and tag that found the model)
- Pipeline Compatibility
- Library Name

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
