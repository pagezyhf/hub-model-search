from typing import Dict, Any

class GCPProvider:
    def __init__(self, config: Dict[str, Any]):
        self.name = "gcp"
        self.config = config
        compatibility = config.get("compatibility", {})
        
        # Get configurations from yaml
        self.inference_tags = compatibility.get("inference_tags")
        self.transformers_compatible_pipelines = compatibility.get("transformers_pipelines")
        self.diffusers_compatible_tasks = compatibility.get("diffusers_tasks")
        self.diffusers_compatible_pipelines = compatibility.get("diffusers_pipelines")

    def check_compatibility(self, model_info: Dict[str, Any]) -> bool:
        # Check for inference tags
        if any(tag in (model_info.get('tags') or []) for tag in self.inference_tags):
            return True
            
        # Check for transformers library with specific pipeline tags
        has_transformers = "transformers" in (model_info.get('library_name') or [])
        has_compatible_transformers_pipeline = model_info.get('pipeline_tag') in self.transformers_compatible_pipelines
        
        if has_transformers and has_compatible_transformers_pipeline:
            return True
            
        # Check for diffusers library with text-to-image task and specific pipelines
        has_diffusers = "diffusers" in (model_info.get('library_name') or [])
        has_compatible_diffusers_task = model_info.get('pipeline_tag') in self.diffusers_compatible_pipelines_compatible_pipelines
        has_compatible_diffusers_pipeline = any(
            tag in (model_info.get('tags') or []) 
            for tag in self.diffusers_compatible_pipelines
        )
        if has_diffusers and has_compatible_diffusers_task and has_compatible_diffusers_pipeline:
            return True
            
        return False 