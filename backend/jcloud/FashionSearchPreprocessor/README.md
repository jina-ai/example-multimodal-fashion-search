# FashionSearchPreprocessor

For all fashion image Documents:

**On all requests**:
- Convert to tensor (if needed)
- Normalize and resize tensors to consistent size

**On `/index` request**:
- Add metadata including price range, rating range, path to file


## Usage

#### via Docker image (recommended)

```python
from jina import Flow
	
f = Flow().add(uses='jinahub+docker://FashionSearchPreprocessor')
```

#### via source code

```python
from jina import Flow
	
f = Flow().add(uses='jinahub://FashionSearchPreprocessor')
```

- To override `__init__` args & kwargs, use `.add(..., uses_with: {'key': 'value'})`
- To override class metas, use `.add(..., uses_metas: {'key': 'value})`
