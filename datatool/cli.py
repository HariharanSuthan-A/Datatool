import argparse

from datatool import DataAnalyzer


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple CSV Data Analyzer")
    parser.add_argument("--file", "-f", default="data.csv", help="Path to CSV file")
    parser.add_argument("--cmd", "-c", help="Single command to run, e.g., 'describe()'")
    parser.add_argument("--repl", action="store_true", help="Start interactive command loop")
    args = parser.parse_args()

    analyzer = DataAnalyzer(args.file)

    if args.cmd:
        out = analyzer.run(args.cmd)
        print(out)
        return

    if args.repl or not args.cmd:
        print("Type 'help' to list commands. Press Ctrl+C to exit.")
        try:
            while True:
                raw = input(">> ").strip()
                if not raw:
                    continue
                out = analyzer.run(raw)
                print(out)
        except KeyboardInterrupt:
            print("\n👋 Goodbye")


