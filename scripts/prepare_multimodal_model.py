from __future__ import annotations

import argparse

from huggingface_hub import snapshot_download


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download the Qwen3-VL base model into the Hugging Face cache."
    )
    parser.add_argument("--model", default="Qwen/Qwen3-VL-2B-Instruct")
    args = parser.parse_args()
    path = snapshot_download(args.model)
    print(f"Model ready: {path}")


if __name__ == "__main__":
    main()
