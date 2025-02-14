# Model Selection Tool

A configurable tool to aggregate and filter model candidates from Hugging Face Hub based on cloud provider compatibility and various search scenarios.

## Features

1. **Provider-specific Model Selection**
   - Support for multiple cloud providers (GCP, AWS)
   - Provider-specific compatibility checks
   - Separate output files for each provider

2. **Flexible Search Scenarios**
   - Trending models
   - Most used models
   - Overall rankings
   - Task-specific searches
   - Industry vertical filtering

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
pip install huggingface-hub pyyaml pandas
```

## Configuration

The tool uses YAML configuration files located in the `configs/` directory:

- `search_scenarios.yaml`: Define search scenarios and default parameters
- `providers/`: Provider-specific compatibility rules
  - `gcp.yaml`: Google Cloud Platform configuration
  - `aws.yaml`: Amazon Web Services configuration
- `industries.yaml`: Industry vertical configurations and filters

### Customizing Configurations

1. **Search Scenarios**
   - Modify `configs/search_scenarios.yaml` to adjust search parameters
   - Configure sorting criteria and default limits

2. **Provider Compatibility**
   - Update provider YAML files in `configs/providers/`
   - Define compatible tags, tasks, and pipelines

3. **Industry Verticals**
   - Edit `configs/industries.yaml` to define industry-specific filters
   - Configure relevant tasks and use cases

## Usage

Basic usage:

```bash
python main.py --provider gcp,aws --scenario trending --limit 10
```

### Command Line Arguments

- `--provider`: Comma-separated list of providers (gcp,aws)
- `--scenario`: Search scenario (trending,most_used,overall)
- `--industry`: Industry vertical (finance,healthcare,retail)
- `--limit`: Number of models to retrieve (default: 10)

### Examples

1. Search trending models for GCP:
```bash
python main.py --provider gcp --scenario trending
```

2. Get most used models for AWS in finance:
```bash
python main.py --provider aws --scenario most_used --industry finance
```

3. Combined search across providers:
```bash
python main.py --provider gcp,aws --scenario trending,most_used --limit 20
```

## Output

The tool generates CSV files in the `output/` directory:
- `gcp_models.csv`: Models compatible with Google Cloud Platform
- `aws_models.csv`: Models compatible with Amazon Web Services

Each CSV file contains:
- Model ID
- Provider Compatibility
- Trending Score
- Downloads
- Likes
- Tags
- Tasks
- License
- Pipeline Compatibility
- Industry Relevance (if applicable)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]
