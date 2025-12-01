import os
from elevenlabs import ElevenLabs, VoiceSettings

# APIキーの設定（環境変数から取得するか、ここに直接入力してください）
# 例: os.environ["ELEVENLABS_API_KEY"] = "your_api_key_here"
api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    print("⚠️ APIキーが見つかりません。環境変数 ELEVENLABS_API_KEY を設定するか、スクリプト内に直接記述してください。")
    print("デモモードとして動作します。（実際の音声生成は行われません）")

# 野洲のおっさんのボイスID（ElevenLabsで作成したVoice IDをここに入れます）
# 仮のIDを入れています
voice_id = "JBFqnCBsd6RMkjVDRqzb" # 例: George という既存のボイスID

input_file = "TestVoice_Imashuku_JP.mp3"
output_file = "Ossan_Voice_JP.mp3"

def convert_voice():
    if not api_key:
        return

    client = ElevenLabs(api_key=api_key)

    print(f"Converting {input_file} to {output_file}...")
    
    try:
        # Speech to Speech 変換を実行
        audio_generator = client.speech_to_speech.convert(
            voice_id=voice_id,
            audio=open(input_file, "rb"),
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.35,       # 低め＝感情豊か
                similarity_boost=0.75, # 元の声にどれだけ似せるか
                style=0.0,
                use_speaker_boost=True
            )
        )

        # 音声データを保存
        with open(output_file, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        print(f"✅ 変換完了！ {output_file} が保存されました。")

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    convert_voice()

