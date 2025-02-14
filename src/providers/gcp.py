from typing import Dict, Any

class GCPProvider:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get("name", "gcp").lower()
        
        compatibility = config.get("compatibility", {})
        
        # Get configurations from yaml
        self.inference_tags = compatibility.get("inference_tags", [
            "text-generation-inference",
            "text-embeddings-inference"
        ])
        
        self.transformers_compatible_pipelines = compatibility.get("transformers_pipelines", [
            "text-classification",
            "token-classification", 
            "fill-mask",
            "question-answering"
        ])
        
        self.diffusers_compatible_pipelines = compatibility.get("diffusers_pipelines", [
            "diffusers:FluxPipeline",
            "diffusers:IFPipeline", 
            "diffusers:KandinskyPipeline",
            "diffusers:KandinskyV22Pipeline",
            "diffusers:StableDiffusionControlNetPipeline",
            "diffusers:StableDiffusionPipeline",
            "diffusers:StableDiffusionXLPipeline"
        ])

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
        has_text_to_image_task = "text-to-image" in (model_info.get('pipeline_tag') or [])
        has_compatible_diffusers_pipeline = any(
            tag in (model_info.get('tags') or []) 
            for tag in self.diffusers_compatible_pipelines
        )
        
        if has_diffusers and has_text_to_image_task and has_compatible_diffusers_pipeline:
            return True
            
        return False 