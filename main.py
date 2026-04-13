import argparse
import os

parser = argparse.ArgumentParser(
    prog="seqai",
    description="Make your logseq notes searchable with AI")
parser.add_argument("-i", "--index", action="store_true", help="Run the indexer")

def main():
    print("Hello, SeqAI!")

    args = parser.parse_args()

    db = LogseqDbAdapter("/Users/erica/notes")
    db.fetch_all("some query")

if __name__ == "__main__":
    main()
