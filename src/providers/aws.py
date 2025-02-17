from typing import Dict, Any

class AWSProvider:
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
        # Check tags
        if not self.check_tags(model_info.get("tags", [])):
            return False

        # Check tasks
        if not self.check_tasks(model_info.get("tasks", [])):
            return False

        return True 