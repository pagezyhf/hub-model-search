from huggingface_hub import HfApi
import argparse
import csv
import os

def aggregate_model_candidates(search_params):
    """
    Aggregate models from multiple HF Hub API calls with different filter criteria.
    
    Args:
        search_params: List of dicts, where each dict contains parameters for api.list_models()
        
    Returns:
        List[ModelInfo]: Combined list of unique models from all API calls
    """
    api = HfApi()
    all_models = []
    
    for kwargs in search_params:
        models = api.list_models(**kwargs)
        # Convert models iterator to list and extend all_models
        all_models.extend(list(models))
    
    # Remove duplicates based on model IDs
    seen_ids = set()
    unique_models = []
    for model in all_models:
        if model.id not in seen_ids:
            seen_ids.add(model.id)
            unique_models.append(model)
            
    return unique_models


def is_gcp_compatible(model_info):
    """
    Check if a model is compatible with GCP deployment based on specific criteria.
    
    Args:
        model_info (ModelInfo): Model information from the Hugging Face Hub API
        
    Returns:
        bool: True if model meets GCP compatibility criteria, False otherwise
    """
    # Check for inference tags
    if any(tag in model_info.tags for tag in ["text-generation-inference", "text-embeddings-inference"]):
        return True
        
    # Check for transformers library with specific pipeline tags
    transformers_compatible_pipelines = [
        "text-classification",
        "token-classification", 
        "fill-mask",
        "question-answering"
    ]
    
    has_transformers = "transformers" in (model_info.library_name or [])
    has_compatible_transformers_pipeline = model_info.pipeline_tag in transformers_compatible_pipelines
    
    if has_transformers and has_compatible_transformers_pipeline:
        return True
        
    # Check for diffusers library with text-to-image task and specific pipelines
    diffusers_compatible_pipelines = [
        "diffusers:FluxPipeline",
        "diffusers:IFPipeline", 
        "diffusers:KandinskyPipeline",
        "diffusers:KandinskyV22Pipeline",
        "diffusers:StableDiffusionControlNetPipeline",
        "diffusers:StableDiffusionPipeline",
        "diffusers:StableDiffusionXLPipeline"
    ]
    
    has_diffusers = "diffusers" in (model_info.library_name or [])
    has_text_to_image_task = "text-to-image" in (model_info.pipeline_tag or [])
    has_compatible_diffusers_pipeline = any(tag in model_info.tags for tag in diffusers_compatible_pipelines)
    
    if has_diffusers and has_text_to_image_task and has_compatible_diffusers_pipeline:
        return True
        
    return False


def main(output_path):
    search_params = [
        {
            "sort": "trendingScore",
            "limit": 10,
            "direction": -1
        },
        {
            "sort": "likes",
            "limit": 10,
            "direction": -1
        },
        {
            "sort": "trendingScore",
            "limit": 10,
            "direction": -1,
            "tags": "text-generation-inference"
        },
        {
            "sort": "likes",
            "limit": 10,
            "direction": -1,
            "tags": "text-generation-inference"
        },
        {
            "sort": "likes",
            "limit": 10,
            "direction": -1,
            "tags": "text-embeddings-inference"
        },
        {
            "sort": "trendingScore",
            "limit": 10,
            "direction": -1,
            "tags": "text-embeddings-inference"
        },
        {
            "sort": "likes",
            "limit": 10,
            "direction": -1,
            "task": "text-classification"
        },
        {
            "sort": "trendingScore",
            "limit": 10,
            "direction": -1,
            "task": "text-classification"
        },
        {
            "sort": "likes",
            "limit": 10,
            "direction": -1,
            "task": "text-to-image"
        },
        {
            "sort": "trendingScore",
            "limit": 10,
            "direction": -1,
            "task": "text-to-image"
        },
        {
            "sort": "likes",
            "limit": 10,
            "direction": -1,
            "task": "text-image-to-image"
        },
        {
            "sort": "trendingScore",
            "limit": 10,
            "direction": -1,
            "task": "text-image-to-image"
        }
    ]   

    combined_models = aggregate_model_candidates(search_params=search_params)

    # Prepare data for CSV
    csv_data = []
    for model in combined_models:
        gcp_compatible = is_gcp_compatible(model)
        csv_data.append({'model_id': model.id, 'library_name': model.library_name, 'task': model.pipeline_tag, 'gcp_compatible': gcp_compatible})

    # Write to CSV file
    with open(output_path, mode='w', newline='') as csv_file:
        fieldnames = ['model_id', 'library_name', 'task', 'gcp_compatible']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)

    print(f"CSV file '{output_path}' created with {len(csv_data)} entries.")

# Add this block to handle command-line execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a CSV of GCP compatible models.')
    default_output_path = os.path.join(os.getcwd(), 'gcp_compatible_models.csv')  # Set default path
    parser.add_argument('output_path', type=str, nargs='?', default=default_output_path, help='Path to save the output CSV file (default: current directory + gcp_compatible_models.csv)')
    args = parser.parse_args()
    
    main(args.output_path)
