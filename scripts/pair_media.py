#!/usr/bin/env python3
"""
Pair inbox media files with their packet contracts.

Scans brands/<brand>/inbox/, matches files to packets by the return filename
contract (specified in each packet file), moves matched files into the week
folder, updates the post's status to media-ready, and lists unmatched/unfilled.

This is the inbound half of the human-in-the-loop media workflow.
After media_packet.py generates the packets and the human pastes/downloads/renames,
this script picks up where the human left off.

Usage:
    python scripts/pair_media.py --brand allsquared
    python scripts/pair_media.py --brand allsquared --week 2026-W30
    python scripts/pair_media.py --brand allsquared --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def find_packets(week_path: Path) -> dict[str, Path]:
    """
    Scan the week's media-packets/ folder, extract each packet's return-filename
    contract, and return a dict mapping return-filename → packet path.
    """
    packets_dir = week_path / "media-packets"
    if not packets_dir.exists():
        return {}

    # Match either single-backtick (`` `2026-W30-01.mp4` ``) or
    # fenced-code-block (```\n2026-W30-01.mp4\n```) return-filename contracts.
    contract_re = re.compile(
        r"Save the downloaded file as:\s*\n\s*\n?"
        r"(?:```\s*\n)?\s*"
        r"`?([^`\s]+\.[a-z0-9]+)`?"
        r"(?:\s*\n```)?",
        re.MULTILINE,
    )

    contracts: dict[str, Path] = {}
    for packet_file in sorted(packets_dir.glob("*.md")):
        text = packet_file.read_text()
        match = contract_re.search(text)
        if match:
            contracts[match.group(1)] = packet_file
    return contracts


def find_inbox_files(brand_dir: Path) -> list[Path]:
    """List all files in the brand's inbox/, excluding .gitkeep."""
    inbox = brand_dir / "inbox"
    if not inbox.exists():
        return []
    return [f for f in inbox.iterdir() if f.is_file() and f.name != ".gitkeep"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Pair inbox media with packets")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--week", default=None,
                        help="Specific week (default: scan all weeks with packets)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be moved without doing it")
    args = parser.parse_args()

    brand_dir = REPO_ROOT / "brands" / args.brand
    if not brand_dir.exists():
        print(f"ERROR: brands/{args.brand}/ not found", file=sys.stderr)
        sys.exit(1)

    inbox = brand_dir / "inbox"
    if not inbox.exists():
        print(f"ERROR: {brand_dir}/inbox/ not found", file=sys.stderr)
        sys.exit(1)

    weeks_dir = brand_dir / "weeks"
    if not weeks_dir.exists():
        print(f"ERROR: {weeks_dir}/ not found", file=sys.stderr)
        sys.exit(1)

    # Which weeks to scan
    if args.week:
        week_dirs = [weeks_dir / args.week]
    else:
        week_dirs = [w for w in weeks_dir.iterdir()
                     if w.is_dir() and (w / "media-packets").exists()]

    if not week_dirs:
        print("No weeks with media-packets found.", file=sys.stderr)
        sys.exit(1)

    # Aggregate all expected contracts from all weeks
    all_contracts: dict[str, tuple[Path, Path]] = {}
    # mapping return_filename -> (packet_path, week_dir)
    for week_dir in week_dirs:
        for return_name, packet_path in find_packets(week_dir).items():
            all_contracts[return_name] = (packet_path, week_dir)

    inbox_files = find_inbox_files(brand_dir)

    print(f"\n=== Pairing inbox → packets for {args.brand} ===\n")
    print(f"Inbox files: {len(inbox_files)}")
    print(f"Expected contracts: {len(all_contracts)}")

    matched = []
    unmatched_inbox = []
    unfilled_contracts = set(all_contracts.keys())

    for inbox_file in inbox_files:
        if inbox_file.name in all_contracts:
            packet_path, week_dir = all_contracts[inbox_file.name]
            matched.append((inbox_file, packet_path, week_dir))
            unfilled_contracts.discard(inbox_file.name)
        else:
            unmatched_inbox.append(inbox_file)

    # Process matched
    if matched:
        print(f"\n--- Matched ({len(matched)}) ---\n")
        for inbox_file, packet_path, week_dir in matched:
            # Move inbox file to the week folder, sibling of the packet
            dest_dir = packet_path.parent
            dest_path = dest_dir / inbox_file.name
            if args.dry_run:
                print(f"  [DRY] {inbox_file.name} → {dest_path.relative_to(REPO_ROOT)}")
            else:
                shutil.move(str(inbox_file), str(dest_path))
                print(f"  ✓ {inbox_file.name} → {dest_path.relative_to(REPO_ROOT)}")

    # Report unmatched
    if unmatched_inbox:
        print(f"\n--- Unmatched inbox files ({len(unmatched_inbox)}) ---\n")
        for f in unmatched_inbox:
            print(f"  ? {f.name}")
        print("\nThese files are in inbox/ but no packet expects them.")
        print("Either: rename to match a packet's return-filename contract,")
        print("        generate a packet for them, or remove if not needed.")

    if unfilled_contracts:
        print(f"\n--- Unfilled packets ({len(unfilled_contracts)}) ---\n")
        for c in sorted(unfilled_contracts):
            packet_path, week_dir = all_contracts[c]
            print(f"  ? {c}  (packet: {packet_path.name})")
        print("\nThese packets have no media file yet.")
        print("Either: paste the packet's prompt into Higgsfield, download, rename to contract,")
        print("        drop in inbox/, then re-run this script.")

    print(f"\n=== Summary ===")
    print(f"  Matched: {len(matched)}")
    print(f"  Unmatched inbox files: {len(unmatched_inbox)}")
    print(f"  Unfilled packets: {len(unfilled_contracts)}")
    if args.dry_run:
        print("\n(Dry run — no files were moved. Re-run without --dry-run to apply.)")
    print()


if __name__ == "__main__":
    main()