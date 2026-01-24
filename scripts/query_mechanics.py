#!/usr/bin/env python3
"""
Mechanics-Aware Query CLI — Option 2A

Behavior-first retrieval over segment × primitive units.
Filters by interaction mechanics, ranks by semantic similarity.

Usage:
    python query_mechanics.py --model_family Claude --require SYNTHESIZE --text_query "config"
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

# Ensure CPU-only
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# Configuration
BASE_DIR = Path(__file__).parent.parent
INDICES_DIR = BASE_DIR / 'indices'
REGISTRY_PATH = BASE_DIR / 'segment_registry.jsonl'
SIGNATURES_PATH = BASE_DIR / 'primitive_signatures.jsonl'

# Embedding model (must match index build)
EMBEDDING_MODEL = 'intfloat/e5-small-v2'


def load_signatures() -> dict:
    """
    Load primitive signatures into memory.
    Returns dict keyed by (corpus_id, session_id, segment_id).
    """
    signatures = {}
    with open(SIGNATURES_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                record = json.loads(line)
                key = (record['corpus_id'], record['session_id'], record['segment_id'])
                signatures[key] = record
    return signatures


def load_registry() -> dict:
    """
    Load segment registry into memory.
    Returns dict keyed by (corpus_id, session_id, segment_id).
    """
    registry = {}
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                record = json.loads(line)
                key = (record['corpus_id'], record['session_id'], record['segment_id'])
                registry[key] = record
    return registry


def load_semantic_meta() -> list:
    """
    Load semantic index metadata.
    Returns list of metadata records in index order.
    """
    meta_path = INDICES_DIR / 'semantic' / 'meta.jsonl'
    meta = []
    with open(meta_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                meta.append(json.loads(line))
    return meta


def apply_structural_filters(
    signatures: dict,
    model_family: Optional[str],
    require_primitives: list,
    exclude_primitives: list,
    signature_contains: Optional[str]
) -> set:
    """
    Apply structural filters to signatures.
    Returns set of (corpus_id, session_id, segment_id) keys that pass all filters.
    """
    candidates = set()

    for key, record in signatures.items():
        # Model family filter
        if model_family and model_family != 'ALL':
            if record.get('model_family') != model_family:
                continue

        # Get primitive tags
        tags = set(record.get('primitive_tags', []))
        signature = record.get('primitive_signature', '')

        # Require primitives filter
        if require_primitives:
            if not all(prim in tags for prim in require_primitives):
                continue

        # Exclude primitives filter
        if exclude_primitives:
            if any(prim in tags for prim in exclude_primitives):
                continue

        # Signature contains filter
        if signature_contains:
            if signature_contains.upper() not in signature.upper():
                continue

        candidates.add(key)

    return candidates


def get_candidate_indices(candidates: set, meta: list) -> list:
    """
    Map candidate keys to their indices in the FAISS index.
    Returns list of (index_position, key) tuples.
    """
    result = []
    for idx, m in enumerate(meta):
        key = (m['corpus_id'], m['session_id'], m['segment_id'])
        if key in candidates:
            result.append((idx, key))
    return result


def semantic_search(
    query_text: str,
    candidate_indices: list,
    top_k: int
) -> list:
    """
    Perform semantic search over candidate segments.
    Returns list of (key, score) tuples sorted by descending score.
    """
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}", file=sys.stderr)
        print("Install with: pip install faiss-cpu sentence-transformers", file=sys.stderr)
        sys.exit(1)

    # Load model
    model = SentenceTransformer(EMBEDDING_MODEL, device='cpu')

    # Encode query with passage prefix for e5 models
    query_embedding = model.encode(
        [f"query: {query_text}"],
        normalize_embeddings=True
    )[0].astype('float32')

    # Load FAISS index
    index_path = INDICES_DIR / 'semantic' / 'faiss.index'
    index = faiss.read_index(str(index_path))

    # Search entire index
    k = min(index.ntotal, 1000)  # Search more than we need
    distances, indices = index.search(query_embedding.reshape(1, -1), k)

    # Filter to candidates and collect scores
    candidate_idx_set = {idx for idx, key in candidate_indices}
    idx_to_key = {idx: key for idx, key in candidate_indices}

    results = []
    for i, idx in enumerate(indices[0]):
        if idx in candidate_idx_set:
            results.append((idx_to_key[idx], float(distances[0][i])))

    # Sort by score descending and limit
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


def format_excerpt(text: str, max_len: int = 300) -> str:
    """Format text excerpt for display."""
    # Clean up whitespace
    text = ' '.join(text.split())
    if len(text) > max_len:
        text = text[:max_len] + '...'
    return text


def print_result(
    rank: int,
    key: tuple,
    score: Optional[float],
    signatures: dict,
    registry: dict,
    no_text: bool = False
):
    """Print a single result in the specified format."""
    corpus_id, session_id, segment_id = key

    sig_record = signatures.get(key, {})
    reg_record = registry.get(key, {})

    model_family = sig_record.get('model_family', 'Unknown')
    segment_type = sig_record.get('segment_type', 'UNASSIGNED')
    primitive_signature = sig_record.get('primitive_signature', 'NONE')

    score_str = f"{score:.4f}" if score is not None else "N/A"

    if no_text:
        # Compact output without text excerpt
        print(f"Corpus: {corpus_id} | Model: {model_family} | Session: {session_id} | Segment: {segment_id}")
        print(f"  Type: {segment_type} | Signature: {primitive_signature} | Score: {score_str}")
    else:
        is_terminal = reg_record.get('is_terminal', False)
        text = reg_record.get('text', '')
        print("─" * 50)
        print(f"Rank: {rank}")
        print(f"Score: {score_str}")
        print(f"Corpus: {corpus_id}")
        print(f"Model: {model_family}")
        print(f"Session: {session_id}")
        print(f"Segment: {segment_id}")
        print(f"Segment Type: {segment_type}")
        print(f"Primitive Signature: {primitive_signature}")
        print(f"Terminal: {str(is_terminal).lower()}")
        print(f"Excerpt: {format_excerpt(text)}")
        print("─" * 50)


def main():
    parser = argparse.ArgumentParser(
        description='Mechanics-aware query over segment × primitive indices',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find Claude segments with SYNTHESIZE primitive
  python query_mechanics.py --model_family Claude --require SYNTHESIZE

  # Find GPT segments with EXPLORE but not DERAIL
  python query_mechanics.py --model_family GPT --require EXPLORE --exclude DERAIL

  # Semantic search within CORRECT segments
  python query_mechanics.py --require CORRECT --text_query "permission denied" --top_k 3
"""
    )

    parser.add_argument('--model_family', type=str, choices=['GPT', 'Claude', 'ALL'],
                        default='ALL', help='Filter by model family')
    parser.add_argument('--require', action='append', dest='require_primitives',
                        metavar='PRIMITIVE', default=[],
                        help='Require primitive tag (repeatable)')
    parser.add_argument('--exclude', action='append', dest='exclude_primitives',
                        metavar='PRIMITIVE', default=[],
                        help='Exclude primitive tag (repeatable)')
    parser.add_argument('--signature_contains', type=str,
                        help='Filter signatures containing this substring')
    parser.add_argument('--text_query', type=str,
                        help='Semantic query text for ranking')
    parser.add_argument('--top_k', type=int, default=5,
                        help='Number of results to return (default: 5)')
    parser.add_argument('--list_primitives', action='store_true',
                        help='List all known primitives and exit')
    parser.add_argument('--no_text', action='store_true',
                        help='Suppress text excerpt in output (compact mode)')

    args = parser.parse_args()

    # List primitives mode
    if args.list_primitives:
        print("Known primitives:")
        print("  Shared:      INITIATE, CORRECT, SEQUENCE, REFERENCE")
        print("  Claude-only: SYNTHESIZE, ELEVATE, EXTEND")
        print("  GPT-only:    EXPLORE, DERAIL, RESYNC, OVERFLOW, TRUNCATE")
        print("  Reference:   REFERENCE_INTERNAL (GPT), REFERENCE_EXTERNAL (Claude)")
        return 0

    # Validate inputs
    if not SIGNATURES_PATH.exists():
        print(f"ERROR: Signatures file not found: {SIGNATURES_PATH}", file=sys.stderr)
        return 1
    if not REGISTRY_PATH.exists():
        print(f"ERROR: Registry file not found: {REGISTRY_PATH}", file=sys.stderr)
        return 1

    # Load data
    print("Loading signatures...", file=sys.stderr)
    signatures = load_signatures()
    print(f"  Loaded {len(signatures)} signature records", file=sys.stderr)

    print("Loading registry...", file=sys.stderr)
    registry = load_registry()
    print(f"  Loaded {len(registry)} registry records", file=sys.stderr)

    # Apply structural filters
    print("Applying structural filters...", file=sys.stderr)
    candidates = apply_structural_filters(
        signatures,
        args.model_family if args.model_family != 'ALL' else None,
        args.require_primitives,
        args.exclude_primitives,
        args.signature_contains
    )
    print(f"  {len(candidates)} candidates after filtering", file=sys.stderr)

    if not candidates:
        print("\nNo segments match the specified filters.", file=sys.stderr)
        return 0

    # Semantic ranking or registry order
    if args.text_query:
        print(f"Performing semantic search for: '{args.text_query}'", file=sys.stderr)

        # Load metadata for index mapping
        meta = load_semantic_meta()
        candidate_indices = get_candidate_indices(candidates, meta)

        if not candidate_indices:
            print("\nNo indexed candidates found.", file=sys.stderr)
            return 0

        results = semantic_search(args.text_query, candidate_indices, args.top_k)

        print(f"\n=== Results ({len(results)} of {len(candidates)} candidates) ===\n")
        for rank, (key, score) in enumerate(results, 1):
            print_result(rank, key, score, signatures, registry, args.no_text)

    else:
        # Return in deterministic registry order
        # Sort candidates by (corpus_id, session_id, segment_index)
        sorted_candidates = sorted(
            candidates,
            key=lambda k: (k[0], k[1], signatures.get(k, {}).get('segment_index', 0))
        )[:args.top_k]

        print(f"\n=== Results ({len(sorted_candidates)} of {len(candidates)} candidates) ===\n")
        for rank, key in enumerate(sorted_candidates, 1):
            print_result(rank, key, None, signatures, registry, args.no_text)

    return 0


if __name__ == '__main__':
    sys.exit(main())
