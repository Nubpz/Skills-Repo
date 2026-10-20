#!/usr/bin/env python3
"""Validate an agent design spec and generate the Mermaid diagram and the animated HTML file.

Standard library only (skill sandboxes have no network access and cannot install packages).

Usage:
  python build_design.py design.json --out-dir .
  cat design.json | python build_design.py - --out-dir .

On success it writes design.mmd and architecture-flow.html to --out-dir and prints a JSON
result that includes the Mermaid text. On failure it prints the errors as JSON and exits 1.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

LAYERS = ["users", "agent", "connectors", "data"]
LAYER_LABELS = {
    "users": "Users and channels",
    "agent": "Agent",
    "connectors": "Approved connectors",
    "data": "Knowledge and systems",
}
TYPE_LAYERS = {
    "channel": {"users"},
    "agent": {"agent"},
    "connector": {"connectors"},
    "knowledge": {"data"},
    "system": {"data"},
    "human": {"users", "data"},
}
NEEDS_APPROVAL = {"connector", "knowledge"}
MAX_PER_LAYER = 4
MAX_NODES = 12
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def is_text(v, max_len=None):
    return isinstance(v, str) and v.strip() != "" and (max_len is None or len(v) <= max_len)


def validate(spec):
    errors, warnings = [], []
    if not isinstance(spec, dict):
        return ["The spec must be a JSON object."], warnings

    if not is_text(spec.get("title"), 80):
        errors.append("'title' is required (text, up to 80 characters).")
    if "summary" in spec and not is_text(spec["summary"], 200):
        errors.append("'summary' must be text up to 200 characters if present.")

    nodes = spec.get("nodes")
    edges = spec.get("edges")
    if not isinstance(nodes, list) or not nodes:
        errors.append("'nodes' must be a non-empty list.")
        nodes = []
    if not isinstance(edges, list) or not edges:
        errors.append("'edges' must be a non-empty list.")
        edges = []

    ids, by_id = set(), {}
    for i, n in enumerate(nodes):
        where = f"nodes[{i}]"
        if not isinstance(n, dict):
            errors.append(f"{where} must be an object.")
            continue
        nid = n.get("id")
        if not isinstance(nid, str) or not ID_RE.match(nid):
            errors.append(f"{where}: 'id' must start with a letter and use only letters, digits and underscores.")
            continue
        where = f"node '{nid}'"
        if nid in ids:
            errors.append(f"{where}: duplicate id.")
            continue
        ids.add(nid)
        by_id[nid] = n
        if not is_text(n.get("label"), 60):
            errors.append(f"{where}: 'label' is required (up to 60 characters).")
        layer, ntype = n.get("layer"), n.get("type")
        if layer not in LAYERS:
            errors.append(f"{where}: 'layer' must be one of {LAYERS}.")
        if ntype not in TYPE_LAYERS:
            errors.append(f"{where}: 'type' must be one of {sorted(TYPE_LAYERS)}.")
        elif layer in LAYERS and layer not in TYPE_LAYERS[ntype]:
            errors.append(f"{where}: type '{ntype}' belongs in layer {sorted(TYPE_LAYERS[ntype])}, not '{layer}'.")
        if ntype in NEEDS_APPROVAL:
            if not is_text(n.get("approved_by"), 80):
                errors.append(
                    f"{where}: a {ntype} must have 'approved_by' naming the governance knowledge file that "
                    f"confirms it is approved. Look it up in the knowledge sources; if it is not listed as "
                    f"approved, replace it with an approved alternative."
                )
            status = n.get("approval_status", "approved")
            if status != "approved":
                errors.append(f"{where}: approval_status is '{status}'. Only approved connectors and knowledge sources may be used.")
        if "note" in n and not is_text(n["note"], 160):
            errors.append(f"{where}: 'note' must be text up to 160 characters.")

    if nodes and not any(isinstance(n, dict) and n.get("layer") == "users" for n in nodes):
        errors.append("At least one node is needed in the 'users' layer (who or what starts the flow).")
    if nodes and not any(isinstance(n, dict) and n.get("type") == "agent" for n in nodes):
        errors.append("At least one node of type 'agent' is needed.")

    steps, used = [], set()
    for i, e in enumerate(edges):
        where = f"edges[{i}]"
        if not isinstance(e, dict):
            errors.append(f"{where} must be an object.")
            continue
        a, b = e.get("from"), e.get("to")
        if a not in by_id:
            errors.append(f"{where}: 'from' refers to unknown node '{a}'.")
        if b not in by_id:
            errors.append(f"{where}: 'to' refers to unknown node '{b}'.")
        if a == b and a in by_id:
            errors.append(f"{where}: an edge cannot start and end at the same node.")
        if not is_text(e.get("label"), 50):
            errors.append(f"{where}: 'label' is required (up to 50 characters).")
        step = e.get("step")
        if not isinstance(step, int) or isinstance(step, bool) or step < 1:
            errors.append(f"{where}: 'step' must be a whole number starting at 1.")
        else:
            steps.append(step)
        if "bidirectional" in e and not isinstance(e["bidirectional"], bool):
            errors.append(f"{where}: 'bidirectional' must be true or false.")
        if a in by_id and b in by_id:
            used.add(a)
            used.add(b)
            la, lb = by_id[a].get("layer"), by_id[b].get("layer")
            if la in LAYERS and lb in LAYERS and abs(LAYERS.index(la) - LAYERS.index(lb)) > 1:
                if "knowledge" not in (by_id[a].get("type"), by_id[b].get("type")):
                    warnings.append(
                        f"{where}: '{a}' to '{b}' skips a layer. Route it through the connectors layer so the diagram stays tidy."
                    )

    if steps and sorted(steps) != list(range(1, len(edges) + 1)):
        errors.append(f"Edge 'step' numbers must be unique and run 1 to {len(edges)} with no gaps. Found: {sorted(steps)}.")

    for nid in by_id:
        if nid not in used and edges:
            errors.append(f"node '{nid}' is not connected to anything. Connect it or remove it.")

    per_layer = {}
    for n in by_id.values():
        per_layer[n.get("layer")] = per_layer.get(n.get("layer"), 0) + 1
    for layer, count in per_layer.items():
        if count > MAX_PER_LAYER:
            warnings.append(f"Layer '{layer}' has {count} nodes (more than {MAX_PER_LAYER}). Group related items to keep the diagram uniform.")
    if len(by_id) > MAX_NODES:
        warnings.append(f"The design has {len(by_id)} nodes (more than {MAX_NODES}). Consider simplifying or splitting it.")

    for key in ("replaced",):
        items = spec.get(key, [])
        if not isinstance(items, list):
            errors.append(f"'{key}' must be a list.")
            continue
        for i, r in enumerate(items):
            if not isinstance(r, dict) or not all(is_text(r.get(f)) for f in ("requested", "reason", "used_instead")):
                errors.append(f"{key}[{i}] needs 'requested', 'reason' and 'used_instead' as text.")
    assumptions = spec.get("assumptions", [])
    if not isinstance(assumptions, list) or not all(is_text(a) for a in assumptions):
        errors.append("'assumptions' must be a list of text items if present.")

    return errors, warnings


def mm_text(s):
    s = re.sub(r"[\r\n]+", " ", str(s))
    s = s.replace('"', "'")
    s = re.sub(r"[<>`]", "", s)
    return s.strip()


def to_mermaid(spec):
    nodes, edges = spec["nodes"], sorted(spec["edges"], key=lambda e: e["step"])
    out = ["flowchart TB"]
    shapes = {
        "channel": ('(["', '"])'),
        "agent": ('("', '")'),
        "connector": ('[["', '"]]'),
        "knowledge": ('[("', '")]'),
        "system": ('["', '"]'),
        "human": ('{{"', '"}}'),
    }
    for layer in LAYERS:
        members = [n for n in nodes if n["layer"] == layer]
        if not members:
            continue
        out.append(f'  subgraph L_{layer}["{LAYER_LABELS[layer]}"]')
        for n in members:
            left, right = shapes[n["type"]]
            label = mm_text(n["label"]) + (" \u2713" if n["type"] in NEEDS_APPROVAL else "")
            out.append(f"    n_{n['id']}{left}{label}{right}")
        out.append("  end")
    for e in edges:
        arrow = "<-->" if e.get("bidirectional") else "-->"
        out.append(f'  n_{e["from"]} {arrow}|"{e["step"]}. {mm_text(e["label"])}"| n_{e["to"]}')
    classes = {
        "channel": "fill:#f1e8fd,stroke:#7c3aed,color:#111827",
        "agent": "fill:#e1ecff,stroke:#1a56db,color:#111827",
        "connector": "fill:#e2f5e9,stroke:#1e7e34,color:#111827",
        "knowledge": "fill:#fff1d6,stroke:#b45309,color:#111827",
        "system": "fill:#fff1d6,stroke:#b45309,color:#111827",
        "human": "fill:#fde4e4,stroke:#b91c1c,color:#111827",
    }
    for t, style in classes.items():
        members = [f"n_{n['id']}" for n in nodes if n["type"] == t]
        if members:
            out.append(f"  classDef {t} {style}")
            out.append(f"  class {','.join(members)} {t}")
    return "\n".join(out) + "\n"


def find_template():
    here = Path(__file__).resolve().parent
    for p in (here.parent / "assets" / "flow-template.html", here / "assets" / "flow-template.html",
              Path("assets") / "flow-template.html", Path("flow-template.html")):
        if p.is_file():
            return p
    return None


def to_html(spec):
    tpl_path = find_template()
    if tpl_path is None:
        raise FileNotFoundError("flow-template.html not found next to the skill's assets folder.")
    tpl = tpl_path.read_text(encoding="utf-8")
    payload = json.dumps(spec, ensure_ascii=False)
    payload = payload.replace("</", "<\\/").replace("<!--", "<\\!--").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return tpl.replace("__TITLE__", html.escape(spec["title"])).replace("__SPEC_JSON__", payload)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="Path to the design spec JSON file, or - to read it from standard input")
    ap.add_argument("--out-dir", default=".", help="Where to write design.mmd and architecture-flow.html")
    args = ap.parse_args()

    try:
        raw = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text(encoding="utf-8")
        spec = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [f"Could not read the spec as JSON: {exc}"], "warnings": []}, indent=2))
        return 1

    errors, warnings = validate(spec)
    if errors:
        print(json.dumps({"valid": False, "errors": errors, "warnings": warnings}, indent=2))
        return 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    mermaid = to_mermaid(spec)
    mmd_path = out_dir / "design.mmd"
    html_path = out_dir / "architecture-flow.html"
    mmd_path.write_text(mermaid, encoding="utf-8")
    try:
        html_path.write_text(to_html(spec), encoding="utf-8")
    except FileNotFoundError as exc:
        print(json.dumps({"valid": True, "errors": [], "warnings": warnings + [str(exc)],
                          "files": {"mermaid": str(mmd_path)}, "mermaid": mermaid}, indent=2))
        return 0

    layers = {}
    for n in spec["nodes"]:
        layers[n["layer"]] = layers.get(n["layer"], 0) + 1
    print(json.dumps({
        "valid": True,
        "errors": [],
        "warnings": warnings,
        "node_count": len(spec["nodes"]),
        "edge_count": len(spec["edges"]),
        "nodes_per_layer": layers,
        "files": {"mermaid": str(mmd_path), "html": str(html_path)},
        "mermaid": mermaid,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
