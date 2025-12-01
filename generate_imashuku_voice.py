import os
import requests
import json

# APIキーの設定
api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    print("⚠️ APIキーが見つかりません。環境変数 ELEVENLABS_API_KEY を設定してください。")
    print("（処理を中断します）")
    exit()

# 設定
CHUNK_SIZE = 1024
url_base = "https://api.elevenlabs.io/v1"
headers = {
    "xi-api-key": api_key
}

# 読み上げさせたいテキスト
text_to_speak = "こんにちは！これはAIによって生成された今宿の声です。野洲のおっさんプロジェクトのプロトタイプテストを行っています。"

# 学習用音声ファイル
training_file = "TestVoice_Imashuku_JP.mp3"
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

def create_voice(name, file_path):
    """ボイスクローン（新規作成）"""
    url = f"{url_base}/voices/add"
    
    files = {
        'files': (file_path, open(file_path, 'rb'), 'audio/mpeg')
    }
    data = {
        'name': name,
        'description': 'Prototype voice of Imashuku-san'
    }
    
    print(f"🆕 新しいボイスモデル '{name}' を作成中...")
    response = requests.post(url, headers=headers, data=data, files=files)
    
    if response.status_code == 200:
        voice_id = response.json()['voice_id']
        print(f"✅ ボイスモデル作成完了！ ID: {voice_id}")
        return voice_id
    else:
        print(f"❌ ボイス作成エラー: {response.status_code} - {response.text}")
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
    
    print(f"🗣️ 音声を生成中: 「{text}」")
    headers_json = headers.copy()
    headers_json["Content-Type"] = "application/json"
    
    response = requests.post(url, json=payload, headers=headers_json)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        print(f"🎉 生成完了！ '{output_path}' を再生してください。")
    else:
        print(f"❌ 音声生成エラー: {response.status_code} - {response.text}")

def main():
    # 1. 既存チェック
    voice_id = get_voice_id_by_name(voice_name)
    
    if voice_id:
        print(f"✅ 既存のボイスモデルが見つかりました: {voice_name} (ID: {voice_id})")
    else:
        # 2. 新規作成
        voice_id = create_voice(voice_name, training_file)
        
    if not voice_id:
        print("❌ ボイスIDが取得できなかったため、処理を終了します。")
        return

    # 3. 生成
    generate_audio(voice_id, text_to_speak, "Imashuku_Generated_Speech.mp3")

if __name__ == "__main__":
    main()
