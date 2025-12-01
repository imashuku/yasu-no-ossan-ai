const fs = require('fs');
const path = require('path');

// 環境変数を取得
const API_KEY = process.env.ELEVENLABS_API_KEY || '';
const VOICE_ID = process.env.ELEVENLABS_VOICE_ID || '';

// index.html を読み込み
const htmlPath = path.join(__dirname, 'index.html');
let html = fs.readFileSync(htmlPath, 'utf8');

// プレースホルダーを環境変数の値に置換
html = html.replace("const DEFAULT_API_KEY = '';", `const DEFAULT_API_KEY = '${API_KEY}';`);
html = html.replace("const DEFAULT_VOICE_ID = '';", `const DEFAULT_VOICE_ID = '${VOICE_ID}';`);

// 出力ディレクトリを作成
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir);
}

// dist/index.html に出力
fs.writeFileSync(path.join(distDir, 'index.html'), html);

// 他の静的ファイルもコピー
const filesToCopy = ['ossan_character.png'];
filesToCopy.forEach(file => {
    const src = path.join(__dirname, file);
    const dest = path.join(distDir, file);
    if (fs.existsSync(src)) {
        fs.copyFileSync(src, dest);
    }
});

console.log('✅ Build complete! Output in dist/');
console.log(`   API_KEY: ${API_KEY ? '設定済み' : '未設定'}`);
console.log(`   VOICE_ID: ${VOICE_ID ? '設定済み' : '未設定'}`);

