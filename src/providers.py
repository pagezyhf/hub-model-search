from typing import Dict, Any, Protocol

class Provider(Protocol):
    """Protocol defining the interface for cloud providers"""
    name: str
    def check_compatibility(self, model_info: Dict[str, Any]) -> bool: ...

class AWSProvider:
    def __init__(self, config: Dict[str, Any]):
        self.name = "aws"
        self.config = config
        compatibility = config.get("compatibility", {})
        
        # Get configurations from yaml
        self.inference_tags = compatibility.get("inference_tags")
        self.transformers_compatible_pipelines = compatibility.get("transformers_pipelines")
        self.diffusers_compatible_pipelines = compatibility.get("diffusers_pipelines")

    def check_compatibility(self, model_info: Dict[str, Any]) -> bool:
        # Check for inference tags
        if any(tag in (model_info.get('tags') or []) for tag in self.inference_tags):
            return True

        # Check no custom code in transformers tags
        has_transformers = "transformers" in (model_info.get('library_name') or [])
        has_custom_code = "custom_code" in (model_info.get('tags') or [])

        if has_transformers and not has_custom_code:
            return True

        # Check for diffusers library with text-to-image task and specific pipelines
        has_diffusers = "diffusers" in (model_info.get('library_name') or [])
        has_text_to_image_task = "text-to-image" in (model_info.get('pipeline_tag') or [])
        has_compatible_diffusers_pipeline = any(
            tag in (model_info.get('tags') or []) 
            for tag in self.diffusers_compatible_pipelines
        )
        
        if has_diffusers and has_text_to_image_task and has_compatible_diffusers_pipeline:
            return True

        return False 
    
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
        has_compatible_diffusers_task = model_info.get('pipeline_tag') in self.diffusers_compatible_pipelines
        has_compatible_diffusers_pipeline = any(
            tag in (model_info.get('tags') or []) 
            for tag in self.diffusers_compatible_pipelines
        )
        if has_diffusers and has_compatible_diffusers_task and has_compatible_diffusers_pipeline:
            return True
            
        return False 

class AzureProvider:
    def __init__(self, config: Dict[str, Any]):
        self.name = "azure"
        self.config = config
        compatibility = config.get("compatibility", {})
        
        # Get configurations from yaml
        self.inference_tags = compatibility.get("inference_tags")
        self.transformers_compatible_pipelines = compatibility.get("transformers_pipelines")
        self.diffusers_compatible_pipelines = compatibility.get("diffusers_pipelines")

    def check_compatibility(self, model_info: Dict[str, Any]) -> bool:
        # flag
        has_custom_code = "custom_code" in (model_info.get('tags') or [])

        # Check for inference tags and no custom_code
        if any(tag in (model_info.get('tags') or []) for tag in self.inference_tags) and not has_custom_code:
            return True

        # Check no custom code in transformers tags
        # has_transformers = "transformers" in (model_info.get('library_name') or [])

        # # Check for diffusers library with text-to-image task and specific pipelines
        # has_diffusers = "diffusers" in (model_info.get('library_name') or [])
        # has_text_to_image_task = "text-to-image" in (model_info.get('pipeline_tag') or [])
        # has_compatible_diffusers_pipeline = any(
        #     tag in (model_info.get('tags') or []) 
        #     for tag in self.diffusers_compatible_pipelines
        # )
        
        # if has_diffusers and has_text_to_image_task and has_compatible_diffusers_pipeline:
        #     return True

        return False 