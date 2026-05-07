# Aisunia ブランド統一プロジェクト — プロジェクト情報

> ホームページ・名刺・PowerPointのブランドデザインを統一して管理するリポジトリ。
> 当初はホームページ専用だったが、デザイン統一の必要性から名刺・パワポへ広がった経緯がある。

## インフラ（確定済み・変更不要）

- **GitHubリポジトリ**：`yosuke-takeshita-arch/aisunia-homepage`
  - ローカルフォルダ名は `homepage-builder`（リポジトリ名と異なるので注意・歴史的経緯）
- **ホスティング**：GitHub Pages（ルートデプロイ・稼働中）
- **公開URL**：`https://www.aisunia.com/`（カスタムドメイン・DNS切り替え済み）
- **デプロイ方法**：`git push origin master` するだけで自動反映
- **コンタクトフォーム**：Formspree実装済み（`js/main.js`）
  - エンドポイント：`https://formspree.io/f/mvzveqaz`
  - Netlify Formsは使っていない。デプロイ先を変えてもフォームはそのまま動く

## デザイン方針（要約）

- コーポレートカラー：日の丸赤 `#BC002D` ／ 信頼の紺 `#1A2B4A` ／ スレートブルー `#5C7A99`
- フォント：Noto Sans JP（HP）／ BIZ UDPゴシック（パワポ・名刺）
- コンセプト：「誠実 × 先進」
- キャッチコピー：「AI時代の中小企業に、信頼できるITパートナーを。」

**詳細**：[`docs/design-system.md`](docs/design-system.md) を参照。

## サービス3本柱（HP・名刺・パワポ統一済み）

1. **freee × AI自動化** — freee API × Claude連携による経理・労務・請求書処理の自動化
2. **Claude活用コンサル** — 社内AI組み込みの戦略・プロンプト設計・ロードマップ策定
3. **DX伴走支援** — DX現状診断から実行まで伴走（DXという言葉は必ず含める）

## ディレクトリ構成

```
homepage-builder/
├── index.html                       # HP本体（全セクション）
├── CNAME, robots.txt, sitemap.xml   # GitHub Pages関連
├── css/
│   ├── style.css                    # HPデザイン全体
│   └── animation.css                # スクロールアニメーション
├── js/
│   └── main.js                      # メニュー・スクロール・フォーム送信
├── images/                          # HP用画像（OGP・代表写真）
│
├── brand/                           # 非HP成果物（名刺・パワポ・ロゴ素材）
│   ├── logos/                       # ロゴ全種（カラー・白）
│   │   ├── Aisunia_ロゴ.png
│   │   └── Aisunia_ロゴ_白.png
│   ├── slides/                      # PowerPointテンプレート
│   │   ├── tools/                   # 自動化スクリプト（python-pptx）
│   │   ├── outputs/                 # 生成された.potx/.pptx
│   │   └── README.md                # パワポ運用手順
│   └── cards/                       # 名刺
│       ├── meishi.html              # デザイン基準（HTMLプレビュー）
│       └── README.md
│
├── docs/                            # 設計知識・ベストプラクティス
│   ├── powerpoint-master-best-practice.md   # ★パワポ作成の必読ガイド
│   ├── design-system.md             # 配色・フォント・サービス3本柱
│   └── README.md
│
├── .gitignore
└── CLAUDE.md                        # このファイル
```

## 新しい成果物を追加するとき

1. まず [`docs/design-system.md`](docs/design-system.md) で配色・フォントを確認
2. 配置場所：
   - HPに関わるもの → ルート直下（`images/` も）
   - 名刺・パワポ・ロゴなど → `brand/` 配下
   - 設計知識・学び → `docs/` 配下
3. 一般論と異なる固有の判断をしたら、`docs/` に学びを残す（再現度向上のため）

## 関連ドキュメント

- [`docs/design-system.md`](docs/design-system.md) — ブランド統一仕様
- [`docs/powerpoint-master-best-practice.md`](docs/powerpoint-master-best-practice.md) — パワポテンプレ作成のベストプラクティス
- [`brand/slides/README.md`](brand/slides/README.md) — パワポ運用手順
- [`brand/cards/README.md`](brand/cards/README.md) — 名刺運用手順
