"""
Aisunia PowerPoint A/B/C 配色バリアント生成スクリプト

3案のpptxを一括生成して見比べる用：
  A案：ブランド純正（紺×赤×グレー）
  B案：金アクセント（紺×赤×ゴールド）
  C案：爽やか系（紺×赤×淡ブルーグレー）

実行:
  python brand/slides/tools/create_pptx_variants.py
"""

import os
from pptx import Presentation

from create_pptx_template import (
    apply_color_theme, patch_theme_in_pptx,
    slide_title, slide_agenda, slide_content,
    slide_section, slide_two_col, slide_end,
    W, H,
)


VARIANTS = [
    {
        "code": "A_brand",
        "label": "A案：ブランド純正（紺×赤×グレー）",
        "subtitle_extra": "紺 × 赤 × グレー（既存ブランド最優先）",
        "scheme": {
            "name": "Aisunia_A_Brand",
            "accent1": "BC002D",  # 赤（メイン）
            "accent2": "1A2B4A",  # 紺
            "accent3": "6B7280",  # ニュートラルグレー
            "accent4": "9CA3AF",  # 明グレー
            "accent5": "3A5A8A",  # 明紺
            "accent6": "8B0020",  # 暗赤
        },
    },
    {
        "code": "B_gold",
        "label": "B案：金アクセント（紺×赤×ゴールド）",
        "subtitle_extra": "紺 × 赤 × ゴールド（高級感・士業らしさ）",
        "scheme": {
            "name": "Aisunia_B_Gold",
            "accent1": "BC002D",  # 赤
            "accent2": "1A2B4A",  # 紺
            "accent3": "C9A961",  # ゴールド
            "accent4": "A8884A",  # 暗ゴールド
            "accent5": "3A5A8A",  # 明紺
            "accent6": "6B7280",  # グレー
            "folHlink": "8B0020",
        },
    },
    {
        "code": "C_lightblue",
        "label": "C案：爽やか系（紺×赤×淡ブルーグレー）",
        "subtitle_extra": "紺 × 赤 × 淡いブルーグレー（モダン・読みやすさ重視）",
        "scheme": {
            "name": "Aisunia_C_LightBlue",
            "accent1": "BC002D",  # 赤
            "accent2": "1A2B4A",  # 紺
            "accent3": "A8B5C8",  # 淡ブルーグレー
            "accent4": "7A8FA6",  # ミディアムブルーグレー
            "accent5": "3A5A8A",  # 明紺
            "accent6": "8B95A1",  # クールグレー
        },
    },
    {
        "code": "D_slateblue",
        "label": "D案：スレートブルー（紺×赤×濃ブルーグレー）",
        "subtitle_extra": "紺 × 赤 × スレートブルー（C案発展版・KPMG／McKinsey系）",
        "scheme": {
            "name": "Aisunia_D_SlateBlue",
            "accent1": "BC002D",  # 赤
            "accent2": "1A2B4A",  # 紺
            "accent3": "5C7A99",  # スレートブルー
            "accent4": "3D5C7A",  # ダークスレート
            "accent5": "7A8FA6",  # 明スレート
            "accent6": "9CA3AF",  # 明グレー
        },
    },
    {
        "code": "E_champagne",
        "label": "E案：シャンパンゴールド（紺×赤×くすみ金）",
        "subtitle_extra": "紺 × 赤 × シャンパンゴールド（士業の品格・老舗会計事務所系）",
        "scheme": {
            "name": "Aisunia_E_Champagne",
            "accent1": "BC002D",  # 赤
            "accent2": "1A2B4A",  # 紺
            "accent3": "C8A86B",  # シャンパンゴールド
            "accent4": "A88A4F",  # ダークゴールド
            "accent5": "3A5A8A",  # 明紺
            "accent6": "6B7280",  # ニュートラルグレー
        },
    },
    {
        "code": "F_forestgreen",
        "label": "F案：フォレストグリーン（紺×赤×深緑）",
        "subtitle_extra": "紺 × 赤 × フォレストグリーン（成熟・知的・誠実・BCG／Deloitte系）",
        "scheme": {
            "name": "Aisunia_F_ForestGreen",
            "accent1": "BC002D",  # 赤
            "accent2": "1A2B4A",  # 紺
            "accent3": "2D5F3F",  # フォレストグリーン
            "accent4": "1F4A2E",  # ダークグリーン
            "accent5": "3A5A8A",  # 明紺
            "accent6": "6B7280",  # グレー
        },
    },
    {
        "code": "G_burgundy",
        "label": "G案：バーガンディ・ラグジュアリー（深紅×紺×プラチナ）",
        "subtitle_extra": "バーガンディ × 紺 × プラチナグレー（ラグジュアリー・トーン低めの洗練）",
        "scheme": {
            "name": "Aisunia_G_Burgundy",
            "accent1": "800020",  # バーガンディ（深紅）
            "accent2": "1A2B4A",  # 紺
            "accent3": "BDC3C7",  # プラチナグレー
            "accent4": "95A5A6",  # シルバーグレー
            "accent5": "3A5A8A",  # 明紺
            "accent6": "7F8C8D",  # ダークグレー
            "hlink": "800020",
            "folHlink": "4A0010",
        },
    },
]


def build(variant):
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H

    apply_color_theme(prs, scheme=variant["scheme"])

    slide_title(
        prs,
        title=variant["label"],
        subtitle=variant["subtitle_extra"],
    )
    slide_agenda(prs)
    slide_content(prs, page_num=2)
    slide_section(prs)
    slide_two_col(prs, page_num=3)
    slide_end(prs)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"Aisunia_PowerPoint_{variant['code']}.pptx")
    prs.save(out_path)
    patch_theme_in_pptx(out_path, scheme=variant["scheme"])
    print(f"[OK] {variant['label']} -> {out_path}")


def main():
    for v in VARIANTS:
        build(v)
    print("\n3パターン生成完了。brand/slides/outputs/ フォルダのファイルを開いて見比べてください。")


if __name__ == "__main__":
    main()
