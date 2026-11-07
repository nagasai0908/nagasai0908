from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple


class ReportNode:
    def __init__(self, report_id: str, name: str, parent_id: Optional[str] = None):
        self.report_id = report_id
        self.name = name
        self.parent_id = parent_id
        self.children: List["ReportNode"] = []


def build_report_hierarchy(reports: Iterable[Tuple[str, str, Optional[str]]]) -> Dict[str, ReportNode]:
    """Build a hierarchy from a list of (report_id, name, parent_id) tuples."""
    nodes: Dict[str, ReportNode] = {}

    for report_id, name, parent_id in reports:
        nodes.setdefault(report_id, ReportNode(report_id, name, parent_id))
        nodes[report_id].name = name
        nodes[report_id].parent_id = parent_id

    for node in nodes.values():
        if node.parent_id and node.parent_id in nodes:
            nodes[node.parent_id].children.append(node)

    return nodes


def get_hierarchy_names(reports: Iterable[Tuple[str, str, Optional[str]]], separator: str = " > ") -> Dict[str, str]:
    """Return a mapping of report_id -> full hierarchical name."""
    nodes = build_report_hierarchy(reports)
    result: Dict[str, str] = {}

    def walk(node: ReportNode, current_path: List[str]) -> None:
        path = current_path + [node.name]
        result[node.report_id] = separator.join(path)

        for child in node.children:
            walk(child, path)

    for node in nodes.values():
        if node.parent_id is None or node.parent_id not in nodes:
            walk(node, [])

    return result


if __name__ == "__main__":
    sample_reports = [
        ("root", "Executive Reports", None),
        ("finance", "Finance", "root"),
        ("sales", "Sales", "root"),
        ("monthly", "Monthly Summary", "finance"),
        ("q1", "Q1 2026", "sales"),
        ("north", "North Region", "sales"),
        ("product", "Product Performance", "monthly"),
    ]

    hierarchy_names = get_hierarchy_names(sample_reports)
    for report_id, name in hierarchy_names.items():
        print(f"{report_id}: {name}")
