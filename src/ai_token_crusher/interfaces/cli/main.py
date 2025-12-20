import argparse
import sys
from ...core import create_engine, PROFILES

def run_cli(argv=None):
    parser = argparse.ArgumentParser(description="AI Token Crusher - CLI Mode")
    parser.add_argument("-f", "--file", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-p", "--profile", choices=PROFILES.keys(), default="aggressive")
    parser.add_argument("-t", "--terminal", action="store_true", help="Force terminal mode")

    args = parser.parse_args(argv)

    options = PROFILES[args.profile]
    text = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("No input provided.")
        return

    engine = create_engine()
    result = engine.apply(text, options)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result.optimized_text)
        print(f"Saved to {args.output}")
    else:
        print(result.optimized_text)

    print(f"\nSaved {result.total_saved_percent:.1f}% ({result.total_saved_chars} chars) in {result.total_time_ms:.2f}ms")

if __name__ == "__main__":
    run_cli()
