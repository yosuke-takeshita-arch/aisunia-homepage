# Aisunia 公式サイト — プロジェクト情報

## インフラ（確定済み・変更不要）

- **GitHubリポジトリ**：`yosuke-takeshita-arch/aisunia-homepage`
  - ローカルフォルダ名は `homepage-builder`（リポジトリ名と異なるので注意）
- **ホスティング**：GitHub Pages（設定済み・稼働中）
- **公開URL**：`https://aisunia.com/`（カスタムドメイン・DNS切り替え済み）
- **デプロイ方法**：`git push origin master` するだけで自動反映
- **コンタクトフォーム**：Formspree実装済み（`js/main.js` 59行目）
  - エンドポイント：`https://formspree.io/f/mvzveqaz`
  - Netlify Formsは使っていない。デプロイ先を変えてもフォームはそのまま動く

## デザイン方針

- コーポレートカラー：日の丸赤 `#BC002D`
- サブカラー：信頼の紺 `#1A2B4A`
- フォント：Noto Sans JP
- コンセプト：「誠実 × 先進」
- キャッチコピー：「AI時代の中小企業に、信頼できるITパートナーを。」

## サービス3本柱

1. Claudeコンサル
2. DXコンサル
3. 業務自動化

## ファイル構成

- `index.html` — 全セクション（HEADER/HERO/ABOUT/SERVICE/FLOW/WORKS/NEWS/CONTACT/FOOTER）
- `css/style.css` — デザイン全体
- `css/animation.css` — スクロールアニメーション
- `js/main.js` — メニュー・スクロール・フォームバリデーション・Formspree送信
