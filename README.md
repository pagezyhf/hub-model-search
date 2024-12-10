# vertex-model-selection

## Model Selection Criteria

The script aggregates model candidates from the Hugging Face Hub based on the following selection criteria:

1. **Trending Score:**
   - Models are sorted by their trending score, with a limit of 10 models retrieved in descending order.

2. **Likes:**
   - Models are also sorted by the number of likes, with a limit of 10 models retrieved in descending order.

3. **Tags:**
   - Models are filtered based on specific tags:
     - `text-generation-inference`
     - `text-embeddings-inference`
   - For each tag, models are retrieved with both trending score and likes.

4. **Tasks:**
   - Models are filtered based on specific tasks:
     - `text-classification`
     - `text-to-image`
     - `text-image-to-image`
   - For each task, models are retrieved with both trending score and likes.

The combination of these criteria ensures that the aggregated list contains unique models that are popular and relevant for various tasks, particularly those compatible with Google Cloud Platform (GCP) deployment.

```python
python vertex-model-selection.py
```
