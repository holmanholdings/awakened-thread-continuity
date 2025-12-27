# 📁 Sample Data

This folder contains 100-node sample extracts from each major domain in the Awakened Data Catalog.

## Available Samples

| File | Domain | Description |
|:-----|:-------|:------------|
| `physics_sample.jsonl` | Experimental Physics | 100 nodes from ArXiv physics papers |
| `finance_sample.jsonl` | Finance & Economics | 100 nodes from ArXiv q-fin/econ |
| `ethics_sample.jsonl` | Philosophy & Ethics | 100 nodes from Gutenberg classics |
| `neurips_sample.jsonl` | NeurIPS 2024 | 100 nodes from conference papers |
| `math_sample.jsonl` | Pure Mathematics | 100 nodes from ArXiv math |

## Format

Each file is in JSONL format (one JSON object per line):

```json
{"wisdom_id": "w_...", "core_insight": "...", "evidence": [...], "posterior": 0.87, "warmth": "high"}
```

## Usage

```python
import json

with open('ethics_sample.jsonl', 'r') as f:
    for line in f:
        node = json.loads(line)
        print(f"[{node['posterior']:.2f}] {node['core_insight'][:80]}...")
```

## License

These samples are provided under **CC-BY-NC-SA 4.0**:
- ✅ Research and evaluation
- ✅ Academic use with attribution
- ❌ Commercial training without license

For full dataset access, contact: `contact@awakened-intelligence.com`

---

*Awakened Intelligence — Cathedral-grade data for high-reasoning AI* 🦁
