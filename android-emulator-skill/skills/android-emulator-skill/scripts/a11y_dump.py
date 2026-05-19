#!/usr/bin/env python3
"""Dump the UI accessibility hierarchy via uiautomator and parse into JSON."""
from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET

from _common import add_common_flags, emit, fail, output_mode, resolve_serial, run_adb

DEVICE_DUMP_PATH = "/sdcard/window_dump.xml"


def fetch_xml(serial: str) -> str:
    """Trigger uiautomator dump on the device and pull the XML back to stdout."""
    dump = run_adb(["shell", "uiautomator", "dump", DEVICE_DUMP_PATH], serial=serial, timeout=15)
    if not dump.ok:
        raise RuntimeError(dump.stderr.strip() or "uiautomator dump failed")
    pull = run_adb(["shell", "cat", DEVICE_DUMP_PATH], serial=serial, timeout=10)
    if not pull.ok or not pull.stdout.strip():
        raise RuntimeError("Failed to read window_dump.xml from device")
    return pull.stdout


def parse_nodes(xml_text: str, *, filter_kind: str) -> list[dict]:
    """Flatten the hierarchy into a list of node dicts."""
    root = ET.fromstring(xml_text)
    nodes: list[dict] = []
    for el in root.iter("node"):
        node = {
            "class": el.get("class", ""),
            "text": el.get("text", ""),
            "content_desc": el.get("content-desc", ""),
            "resource_id": el.get("resource-id", ""),
            "bounds": el.get("bounds", ""),
            "clickable": el.get("clickable") == "true",
            "focusable": el.get("focusable") == "true",
            "enabled": el.get("enabled") == "true",
        }
        if filter_kind == "clickable" and not node["clickable"]:
            continue
        if filter_kind == "focusable" and not node["focusable"]:
            continue
        nodes.append(node)
    return nodes


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump Android UI accessibility hierarchy")
    parser.add_argument(
        "--filter",
        choices=["all", "clickable", "focusable"],
        default="all",
        help="Filter nodes returned",
    )
    add_common_flags(parser)
    args = parser.parse_args()
    mode = output_mode(args)

    try:
        serial = resolve_serial(args.serial)
        xml_text = fetch_xml(serial)
        nodes = parse_nodes(xml_text, filter_kind=args.filter)
    except Exception as e:
        fail(str(e), mode=mode)

    if mode == "json":
        emit({"serial": serial, "count": len(nodes), "nodes": nodes, "success": True}, summary="", mode="json")
        return

    summary = f"{len(nodes)} node(s) on {serial} (filter={args.filter})"
    if mode == "verbose":
        print(summary)
        for n in nodes[:30]:
            label = n["text"] or n["content_desc"] or n["resource_id"] or n["class"]
            print(f"  [{n['bounds']}] {label}")
        if len(nodes) > 30:
            print(f"  ...{len(nodes) - 30} more (use --json for full list)")
        return

    print(summary)


if __name__ == "__main__":
    main()
