# brand/slides/ — Aisunia パワポテンプレート

Aisunia用のPowerPointテンプレート（.potx）と、それを生成・派生させるスクリプトの置き場。

## ディレクトリ構成

```
brand/slides/
├── tools/                   # 生成スクリプト
│   ├── create_potx_base.py        # スライドサイズ＋テーマ＋フォント設定済みの空.potx生成
│   ├── create_pptx_template.py    # 6レイアウト全部入りサンプル.pptx生成（参考用）
│   └── create_pptx_variants.py    # カラーバリアント7案.pptx生成
└── outputs/                 # 生成物
    ├── Aisunia_Template.potx              # ★本番用テンプレ
    ├── Aisunia_PowerPoint_Template.pptx   # サンプル全部入り
    └── Aisunia_PowerPoint_*.pptx          # カラー検討用バリアント7種
```

## 使い方

### 1. 空テンプレ.potxを再生成したいとき
```powershell
python brand\slides\tools\create_potx_base.py
```
→ `brand/slides/outputs/Aisunia_Template.potx` が生成される

### 2. サンプル全部入り.pptxを再生成したいとき
```powershell
python brand\slides\tools\create_pptx_template.py
```
→ `brand/slides/outputs/Aisunia_PowerPoint_Template.pptx` が生成される

### 3. カラーバリアント7案を再生成したいとき
```powershell
python brand\slides\tools\create_pptx_variants.py
```
→ `brand/slides/outputs/Aisunia_PowerPoint_A_brand.pptx` 〜 `G_burgundy.pptx` が生成される

## 必要なPythonパッケージ

```powershell
pip install python-pptx lxml
```

## .potxの編集（手作業）

`Aisunia_Template.potx` のスライドマスタ・レイアウトの整備は手作業が必要。

**重要：** 開くときは必ず「**ファイル → 開く → 参照**」で開く。ダブルクリックすると新規プレゼン作成になり、テンプレ自体が編集されない。タイトルバーが「**Aisunia_Template - PowerPoint**」になっとるか確認すること。

### 構造設計とベストプラクティス
作成手順・親マスタ／子レイアウトの設計思想・落とし穴は**必読**：
→ [`docs/powerpoint-master-best-practice.md`](../../docs/powerpoint-master-best-practice.md)

### 進捗管理
進行中のテンプレ構築の進捗・各レイアウト配置数値は、Claude Codeのメモリ `project_potx_template_creation.md` に保存。「続きから」と言えば再開できる。

## 配色

詳細：[`docs/design-system.md`](../../docs/design-system.md)

- 赤 `#BC002D` ／ 紺 `#1A2B4A` ／ スレートブルー `#5C7A99`
- フォント：BIZ UDPゴシック（日本語）／ BIZ UDPGothic（英数字）
- スライドサイズ：33.87cm × 19.05cm（標準16:9）
