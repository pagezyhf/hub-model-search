from typing import Dict, Any

class AWSProvider:
    def check_compatibility(self, model_info: Dict[str, Any]) -> bool:
        # Check tags
        if not self.check_tags(model_info.get("tags", [])):
            return False

        # Check tasks
        if not self.check_tasks(model_info.get("tasks", [])):
            return False

        return True 