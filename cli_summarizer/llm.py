import json
import os
import pathlib
import sys
import urllib.request

_ENV_PATH = pathlib.Path.home() / ".config" / "cli-summarizer" / ".env"


def load_env():
    """ .env ファイルから環境変数を読み込む (簡易実装) """
    if _ENV_PATH.exists():
        try:
            with open(_ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        key, _, value = line.partition("=")
                        os.environ[key.strip()] = value.strip()
        except Exception as e:
            print(f"警告: .env の読み込みに失敗しました: {e}", file=sys.stderr)
        # add more debug codes later

def summarize(text: str) -> tuple[str, str]:
    """
    テキストを OpenAI API に送信し、要約と推奨ファイル名を取得する。
    標準ライブラリの urllib を使用し、JSON 形式で結果を受け取る。

    Args:
        text: 入力テキスト
    Returns:
        tuple: (summarized_text, suggested_filename)
    """
    # if the user already has OPENAI_API_KEY set in their shell (e.g. .zshrc), skip reading the file
    if not os.environ.get("OPENAI_API_KEY"):
        load_env()
    api_key = os.environ.get("OPENAI_API_KEY")
        
    if not api_key:
        print("エラー: APIキーが設定されていません。-key 引数で設定するか、環境変数 OPENAI_API_KEY または .env を確認してください", file=sys.stderr)
        sys.exit(1)

    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    # JSON 形式でのレスポンスを強制
    payload = json.dumps({
        "model": "gpt-5-mini",
        "messages": [
            {
                "role": "system", 
                "content": (
                    "あなたはプロフェッショナルな要約アシスタントです。以下のルールに厳密に従ってください。\n"
                    "1. 【フォーマット】要約は単なる箇条書きではなく、見出し（# や ##）、太字、リストなどを適切に組み合わせた、構造的で読みやすい美しいMarkdown形式で作成してください。\n"
                    "2. 【出力言語】要約およびファイル名は、必ず「入力されたテキストと全く同じ言語」で出力してください（英語が入力された場合は英語、日本語が入力された場合は日本語を使用すること）。\n"
                    "3. 【出力形式】出力は必ず以下の厳密なJSON形式にしてください：\n"
                    "{\"summary\": \"Markdown形式の要約文\", \"filename\": \"ファイル名(拡張子なし)\"}"
                )
            },
            {"role": "user", "content": f"以下のテキストを詳細に読み解き、入力言語と同じ言語で、構造化された美しいMarkdownで要約を作成し、ファイル名を提案してください：\n\n{text}"}
        ],
        "response_format": {"type": "json_object"}
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = json.loads(data["choices"][0]["message"]["content"])
            
            summary = content.get("summary", "")
            filename = content.get("filename", "summary")
            
            return summary, filename
            
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"エラー: OpenAI API HTTP {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: OpenAI API 呼び出し失敗: {e}", file=sys.stderr)
        sys.exit(1)
