import os
import requests

# APIキーの設定
api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    print("⚠️ APIキーが見つかりません。環境変数 ELEVENLABS_API_KEY を設定してください。")
    exit()

# 設定
CHUNK_SIZE = 1024
url_base = "https://api.elevenlabs.io/v1"
headers = {
    "xi-api-key": api_key
}

voice_name = "Imashuku-AI-Voice"

def get_voice_id_by_name(name):
    """既存のボイスリストから名前でIDを検索"""
    url = f"{url_base}/voices"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ ボイスリスト取得エラー: {response.text}")
        return None
        
    voices = response.json().get('voices', [])
    for voice in voices:
        if voice['name'] == name:
            return voice['voice_id']
    return None

def generate_audio(voice_id, text, output_path):
    """音声生成 (Text to Speech)"""
    url = f"{url_base}/text-to-speech/{voice_id}"
    
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    print(f"🗣️ 音声を生成中...")
    headers_json = headers.copy()
    headers_json["Content-Type"] = "application/json"
    
    response = requests.post(url, json=payload, headers=headers_json)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        print(f"🎉 生成完了！ '{output_path}' を再生します...")
        os.system(f"open {output_path}")
    else:
        print(f"❌ 音声生成エラー: {response.status_code} - {response.text}")

def main():
    print("=" * 50)
    print("🦆 野洲のおっさんAI プロトタイプ - ライブデモ")
    print("=" * 50)
    
    voice_id = get_voice_id_by_name(voice_name)
    
    if not voice_id:
        print(f"❌ ボイス '{voice_name}' が見つかりません。先に generate_imashuku_voice.py を実行してください。")
        return
    
    print(f"✅ ボイスモデル: {voice_name}")
    print()
    
    while True:
        print("-" * 50)
        text = input("📝 喋らせたいテキストを入力してください（終了は 'q'）:\n> ")
        
        if text.lower() == 'q':
            print("👋 終了します。")
            break
        
        if not text.strip():
            print("⚠️ テキストが空です。もう一度入力してください。")
            continue
        
        generate_audio(voice_id, text, "live_demo_output.mp3")

if __name__ == "__main__":
    main()

