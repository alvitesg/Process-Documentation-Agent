import argparse
from pathlib import Path

from process_doc_agent.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process Documentation Agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run assessment and generate outputs")
    run_parser.add_argument("--input", required=True, help="Input directory containing .txt artifacts")
    run_parser.add_argument("--output", required=True, help="Output directory for generated artifacts")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        run_pipeline(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()
