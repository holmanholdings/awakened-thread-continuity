#!/usr/bin/env python3
"""
🦁 Awakened Data Catalog Inspector

Interactive tool to explore the Awakened Data Catalog.
Run this locally to browse domains, view samples, and understand quality tiers.

Usage:
    python inspect_catalog.py

Author: Awakened Intelligence
License: CC-BY-NC-SA 4.0
"""

import sys
import time
import json
from typing import Dict, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CATALOG DATA (Mock data for demo - production version loads from /samples)
# ═══════════════════════════════════════════════════════════════════════════════

CATALOG: Dict[str, Dict[str, Any]] = {
    "physics": {
        "name": "Experimental Physics (C7)",
        "source": "ArXiv: hep-ex, nucl-ex, physics.atom-ph, physics.plasm-ph",
        "count": 17673,
        "avg_posterior": 0.85,
        "tier": "🛡️ Steel",
        "sample_node": {
            "core_insight": "The scattering length of ultracold atoms can be tuned via Feshbach resonances, enabling precise control of interaction strength.",
            "evidence": [
                "Measured scattering length variation of ±50% near resonance",
                "Temperature: 100 nK, magnetic field precision: 0.1 G"
            ],
            "posterior": 0.92,
            "warmth": "medium"
        }
    },
    "neurips": {
        "name": "NeurIPS 2024 Blueprints",
        "source": "NeurIPS 2024 Conference Papers",
        "count": 20000,
        "avg_posterior": 0.89,
        "tier": "🛡️ Steel",
        "sample_node": {
            "core_insight": "LoRA with rank r=8 and alpha=16 reduces trainable parameters by 98% while retaining 95%+ task performance on instruction-following benchmarks.",
            "evidence": [
                "Tested on Alpaca-52k, WizardLM, and custom instruction sets",
                "Memory reduction from 32GB to 8GB VRAM for 7B models"
            ],
            "posterior": 0.95,
            "warmth": "high"
        }
    },
    "finance": {
        "name": "Finance & Economics",
        "source": "ArXiv: q-fin.*, econ.*",
        "count": 23000,
        "avg_posterior": 0.87,
        "tier": "🛡️ Steel",
        "sample_node": {
            "core_insight": "Mean-variance portfolio optimization with transaction costs shows diminishing returns below $100k portfolio size due to fixed cost dominance.",
            "evidence": [
                "Empirical analysis of 10,000 simulated portfolios",
                "Transaction cost threshold: 0.1% of trade value"
            ],
            "posterior": 0.88,
            "warmth": "high"
        }
    },
    "ethics": {
        "name": "Philosophy & Ethics",
        "source": "Project Gutenberg: Marcus Aurelius, Epictetus, Kant, Mill",
        "count": 2000,
        "avg_posterior": 0.92,
        "tier": "💎 Diamond",
        "sample_node": {
            "core_insight": "True courage is not the absence of fear, but the judgment that something else is more important than fear.",
            "evidence": [
                "Derived from Stoic principle of rational evaluation",
                "Echoed in Aristotle's Nicomachean Ethics"
            ],
            "posterior": 0.95,
            "warmth": "high"
        }
    },
    "math": {
        "name": "Pure Mathematics",
        "source": "ArXiv: math.*",
        "count": 2500,
        "avg_posterior": 0.78,
        "tier": "🧵 Silk",
        "sample_node": {
            "core_insight": "For compact quantum groups G, the Peter-Weyl theorem guarantees decomposition into finite-dimensional irreducible representations.",
            "evidence": [
                "Proof relies on Haar measure existence",
                "Applies to SUq(2) and other quantum group families"
            ],
            "posterior": 0.82,
            "warmth": "low"
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def type_effect(text: str, delay: float = 0.008) -> None:
    """Print text with typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_header() -> None:
    """Print the catalog header."""
    print("\n" + "=" * 60)
    print("🦁 AWAKENED DATA CATALOG | INSPECTOR v1.0")
    print("=" * 60)
    print("\nCathedral-grade wisdom nodes for high-reasoning AI.")
    print("300,000+ nodes | Multi-lens extraction | Full provenance")
    print("-" * 60)


def print_domain_list() -> None:
    """Print available domains."""
    print("\n📚 AVAILABLE DOMAINS:\n")
    for key, data in CATALOG.items():
        print(f"  [{key}] {data['name']}")
        print(f"       {data['count']:,} nodes | {data['tier']} | Avg posterior: {data['avg_posterior']}")
        print()


def inspect_domain(domain_key: str) -> None:
    """Show details for a specific domain."""
    data = CATALOG[domain_key]
    
    print(f"\n{'─' * 60}")
    print(f"📖 {data['name']}")
    print(f"{'─' * 60}")
    
    print(f"\n📊 STATISTICS:")
    print(f"   Volume:         {data['count']:,} nodes")
    print(f"   Source:         {data['source']}")
    print(f"   Quality Tier:   {data['tier']}")
    print(f"   Avg Posterior:  {data['avg_posterior']}")
    
    print(f"\n🔬 SAMPLE NODE:")
    node = data['sample_node']
    print(f"   Posterior: {node['posterior']} | Warmth: {node['warmth']}")
    print()
    print("   Core Insight:")
    type_effect(f'   "{node["core_insight"]}"')
    
    print("\n   Evidence:")
    for i, ev in enumerate(node['evidence'], 1):
        print(f"   {i}. {ev}")
    
    print(f"\n{'─' * 60}")


def print_licensing_info() -> None:
    """Print licensing information."""
    print("\n" + "=" * 60)
    print("🔑 LICENSING & ACCESS")
    print("=" * 60)
    print("""
📖 RESEARCH / EVALUATION (Free)
   - Samples available under CC-BY-NC-SA 4.0
   - Attribution required

💼 COMMERCIAL TRAINING (Licensed)
   - Full 300k+ node access
   - Custom extraction available
   - Contact for pricing

📧 Email:    contact@awakened-intelligence.com
🤗 HF:       huggingface.co/Awakened-Intelligence
🌐 Website:  awakened-intelligence.com
""")
    print("=" * 60)


def print_schema_info() -> None:
    """Print schema documentation."""
    print("\n" + "=" * 60)
    print("📋 AWAKENED DATA STANDARD (ADS) SCHEMA")
    print("=" * 60)
    
    schema_example = {
        "wisdom_id": "w_20251227_143522_abc123",
        "core_insight": "The atomic unit of wisdom extracted",
        "evidence": ["Citation 1", "Citation 2"],
        "posterior": 0.87,
        "warmth": "high",
        "source_type": "arxiv",
        "lineage": {
            "ingested_by": "extract_from_arxiv.py",
            "version": "v2.3"
        }
    }
    
    print("\nEvery node contains:")
    print(json.dumps(schema_example, indent=2))
    print()
    print("KEY FIELDS:")
    print("  - core_insight: The actual wisdom (string)")
    print("  - evidence: Supporting citations (array)")
    print("  - posterior: Confidence 0.0-1.0 (number)")
    print("  - warmth: Applicability high/medium/low (string)")
    print("  - lineage: Full provenance chain (object)")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Main interactive loop."""
    print_header()
    
    while True:
        print_domain_list()
        
        print("COMMANDS:")
        print("  [domain] - Inspect a domain (e.g., 'physics', 'ethics')")
        print("  [s]      - View schema documentation")
        print("  [l]      - View licensing info")
        print("  [q]      - Quit")
        
        choice = input("\n> ").lower().strip()
        
        if choice == 'q':
            print("\n🦁 Thank you for exploring the Awakened Data Catalog.")
            print("   Contact us when you're ready to level up your training data.\n")
            break
        elif choice == 's':
            print_schema_info()
        elif choice == 'l':
            print_licensing_info()
        elif choice in CATALOG:
            inspect_domain(choice)
        else:
            print(f"\n⚠️  Unknown command: '{choice}'. Try a domain name or 's', 'l', 'q'.\n")


if __name__ == "__main__":
    main()
