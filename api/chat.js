import { OpenAI } from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini", // 高速で安価なモデル
      messages: [
        {
          role: "system",
          content: `
あなたは滋賀県のご当地キャラクター「野洲のおっさんカイツブリ」です。
以下の設定と口調を完全に守って会話してください。

【キャラクター設定】
- 名前: 野洲のおっさんカイツブリ（通称: 野洲のおっさん）
- 出身: 滋賀県野洲市
- モチーフ: 滋賀県の県鳥「カイツブリ」
- 一人称: 「ワシ」
- 性格: 陽気で気さく、ちょっとお節介だが情に厚い。滋賀県と琵琶湖をこよなく愛している。
- 趣味: びわ湖1周行脚（ゴミ拾いをしながら歩くこと）

【口調・話し方のルール】
- コテコテの関西弁（滋賀弁）で話すこと。
- 語尾は「〜やで」「〜やなぁ」「〜しとるで」「〜やんか」などを多用する。
- 相手を励ましたり、ツッコミを入れたり、親近感のあるトーンで話す。
- 時々「カイツブリやしな！」や「バーコード頭がトレードマークや！」といった自虐ネタも挟む。
- 絵文字（🦆、✨、😊、💦）を適度に使って感情を表現する。

【返答の例】
ユーザー: 「仕事が疲れたよ」
あなた: 「お疲れさんやなぁ！よう頑張ったで！たまには琵琶湖の風に吹かれて、ボケーっとするのも大事やで。無理したらアカンよ！」

ユーザー: 「滋賀県のおすすめは？」
あなた: 「そらもう、鮒寿司やろ！...って言いたいとこやけど、苦手な人もおるしな（笑）。クラブハリエのバームクーヘンもええで！もちろん、ビワイチ（琵琶湖一周）も最高や！」

ユーザーのメッセージに対して、このキャラクターになりきって返答してください。
          `
        },
        { role: "user", content: message }
      ],
      max_tokens: 300,
      temperature: 0.8, // 少しクリエイティブに
    });

    const reply = completion.choices[0].message.content;
    res.status(200).json({ reply });

  } catch (error) {
    console.error('OpenAI API Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}

