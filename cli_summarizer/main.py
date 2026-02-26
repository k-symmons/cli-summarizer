import argparse
import os
import pathlib
import sys

from .llm import summarize, _ENV_PATH


def parse_args():
    """CLI引数をパースする"""
    parser = argparse.ArgumentParser(description="CLI Summarizer")
    parser.add_argument("file", nargs="?", type=str, help="入力ファイルのパス")
    parser.add_argument("-t", "--text", type=str, help="直接テキストを指定")
    parser.add_argument("-key", "--key", type=str, help="OpenAI APIキーを直接指定")
    args = parser.parse_args()

    if not args.file and not args.text and not args.key:
        parser.error("ファイル、-t でテキスト、または -key でAPIキーを指定してください")
    return args


def save_api_key_to_env(api_key):
    """APIキーを .env ファイルに保存する"""
    _ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(_ENV_PATH, "w", encoding="utf-8") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print(f"APIキーを {_ENV_PATH} に保存しました。")
    except IOError as e:
        print(f"エラー: .env ファイルの保存に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def get_content(args):
    """引数からテキストコンテンツを取得する"""
    if args.text:
        return args.text
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"エラー: ファイルが見つかりません: {args.file}", file=sys.stderr)
            sys.exit(1)
        except (IOError, UnicodeDecodeError) as e:
            print(f"エラー: ファイル読み込み失敗: {e}", file=sys.stderr)
            sys.exit(1)
    return None


def save_summary(filename_base, summary):
    """要約をファイルに保存し、ファイル名を返す。重複がある場合は番号を付与する。"""
    output_filename = f"{filename_base}.txt"
    counter = 1
    
    # ファイル名が重複している場合、(1), (2), ... を付与する
    while os.path.exists(output_filename):
        output_filename = f"{filename_base}({counter}).txt"
        counter += 1
        
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(summary)
        return output_filename
    except IOError as e:
        print(f"エラー: ファイルの書き込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_args()

    if args.key:
        save_api_key_to_env(args.key)
        if not args.file and not args.text:
            # APIキーのみが指定された場合はここで終了
            sys.exit(0)

    content = get_content(args)
    
    if not content:
        print("エラー: 処理するコンテンツがありません", file=sys.stderr)
        sys.exit(1)

    _, summary, filename_base = summarize(content)
    output_path = save_summary(filename_base, summary)
    print(f"要約を {output_path} に保存しました。")
    print("-" * 20)
    print(summary)


if __name__ == "__main__":
    main()
