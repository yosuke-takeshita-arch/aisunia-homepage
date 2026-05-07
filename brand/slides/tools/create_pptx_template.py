"""
Aisunia PowerPoint テンプレート生成スクリプト
カラー: 赤 #BC002D / 紺 #1A2B4A / 白 #FFFFFF
"""

import os
import shutil
import zipfile
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGO_PATH       = os.path.join(BASE_DIR, "brand", "logos", "Aisunia_ロゴ.png")
LOGO_WHITE_PATH = os.path.join(BASE_DIR, "brand", "logos", "Aisunia_ロゴ_白.png")

RED   = RGBColor(0xBC, 0x00, 0x2D)
NAVY  = RGBColor(0x1A, 0x2B, 0x4A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY  = RGBColor(0xF4, 0xF6, 0xF8)
DARK  = RGBColor(0x22, 0x22, 0x22)
MID   = RGBColor(0x55, 0x55, 0x55)
LGRAY = RGBColor(0xCC, 0xCC, 0xCC)
LBLUE = RGBColor(0xAA, 0xBB, 0xCC)

FONT = "BIZ UDPゴシック"

W = Inches(13.33)
H = Inches(7.5)

FOOTER_H = Inches(0.38)
HEADER_H = Inches(1.1)


DEFAULT_SCHEME = {
    "name": "Aisunia",
    "dk1": "1A2B4A", "lt1": "FFFFFF",
    "dk2": "222222", "lt2": "F4F6F8",
    # D案：紺×赤×スレートブルー（KPMG／McKinsey系の知的・モダン配色）
    "accent1": "BC002D",  # 赤
    "accent2": "1A2B4A",  # 紺
    "accent3": "5C7A99",  # スレートブルー
    "accent4": "3D5C7A",  # ダークスレート
    "accent5": "7A8FA6",  # 明スレート
    "accent6": "9CA3AF",  # 明グレー
    "hlink": "BC002D", "folHlink": "551014",
}


def _build_theme_xml(scheme):
    """テーマXML文字列を組み立てる。"""
    s = dict(DEFAULT_SCHEME)
    if scheme:
        s.update(scheme)
    NSMAP = "http://schemas.openxmlformats.org/drawingml/2006/main"
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="{NSMAP}" name="{s['name']}">
  <a:themeElements>
    <a:clrScheme name="{s['name']}">
      <a:dk1><a:srgbClr val="{s['dk1']}"/></a:dk1>
      <a:lt1><a:srgbClr val="{s['lt1']}"/></a:lt1>
      <a:dk2><a:srgbClr val="{s['dk2']}"/></a:dk2>
      <a:lt2><a:srgbClr val="{s['lt2']}"/></a:lt2>
      <a:accent1><a:srgbClr val="{s['accent1']}"/></a:accent1>
      <a:accent2><a:srgbClr val="{s['accent2']}"/></a:accent2>
      <a:accent3><a:srgbClr val="{s['accent3']}"/></a:accent3>
      <a:accent4><a:srgbClr val="{s['accent4']}"/></a:accent4>
      <a:accent5><a:srgbClr val="{s['accent5']}"/></a:accent5>
      <a:accent6><a:srgbClr val="{s['accent6']}"/></a:accent6>
      <a:hlink><a:srgbClr val="{s['hlink']}"/></a:hlink>
      <a:folHlink><a:srgbClr val="{s['folHlink']}"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="{s['name']}">
      <a:majorFont><a:latin typeface="BIZ UDPGothic"/><a:ea typeface="BIZ UDPGothic"/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="BIZ UDPGothic"/><a:ea typeface="BIZ UDPGothic"/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="{s['name']}">
      <a:fillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:fillStyleLst>
      <a:lnStyleLst>
        <a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
      </a:lnStyleLst>
      <a:effectStyleLst>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
      </a:effectStyleLst>
      <a:bgFillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>"""


def apply_color_theme(prs, scheme=None):
    """互換ダミー（保存時に効かないため、実体は patch_theme_in_pptx で行う）。"""
    return  # 何もしない


def patch_theme_in_pptx(pptx_path, scheme=None):
    """保存済みpptxの ppt/theme/theme1.xml を直接書き換える。
    python-pptxの内部APIだとtheme置換が反映されないため、ZIP操作で確実に差し替える。
    円グラフ等のデフォルト配色がここで設定したaccent1〜6に従う。"""
    theme_xml = _build_theme_xml(scheme)
    target = "ppt/theme/theme1.xml"
    tmp_path = pptx_path + ".tmp"
    with zipfile.ZipFile(pptx_path, "r") as zin:
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == target:
                    zout.writestr(item, theme_xml.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))
    shutil.move(tmp_path, pptx_path)


def add_rect(slide, l, t, w, h, color):
    shape = slide.shapes.add_shape(1, l, t, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_textbox(slide, text, l, t, w, h, size,
                bold=False, color=WHITE, align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(l, t, w, h)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_logo(slide, l, t, h):
    """ロゴ画像をそのまま配置（明るい背景用）"""
    try:
        aspect = 3.0
        w = h * aspect
        return slide.shapes.add_picture(LOGO_PATH, l, t, w, h)
    except Exception:
        return None


def add_logo_white(slide, l, t, h):
    """白ロゴを直接配置（紺背景用・プレートなし）"""
    try:
        aspect = 3.0
        w = h * aspect
        return slide.shapes.add_picture(LOGO_WHITE_PATH, l, t, w, h)
    except Exception:
        return None


def add_logo_on_plate(slide, l, t, h):
    """白いプレートの上にロゴを配置（明るい背景に紺文字ロゴを使いたい場合用）"""
    try:
        aspect = 3.0
        logo_w = h * aspect
        pad_x = Inches(0.1)
        pad_y = Inches(0.06)
        plate = slide.shapes.add_shape(
            1, l - pad_x, t - pad_y, logo_w + pad_x * 2, h + pad_y * 2
        )
        plate.fill.solid()
        plate.fill.fore_color.rgb = WHITE
        plate.line.fill.background()
        slide.shapes.add_picture(LOGO_PATH, l, t, logo_w, h)
    except Exception:
        pass


def add_footer(slide, page_num, date_str=""):
    """共通フッター: 日付 | Aisunia All rights reserved. | ページ番号"""
    add_rect(slide, 0, H - FOOTER_H, W, FOOTER_H, NAVY)
    add_rect(slide, 0, H - FOOTER_H, Inches(0.05), FOOTER_H, RED)

    if date_str:
        add_textbox(slide, date_str,
                    Inches(0.3), H - FOOTER_H, Inches(3), FOOTER_H,
                    9, color=LBLUE)

    add_textbox(slide, "Aisunia All rights reserved.",
                0, H - FOOTER_H, W, FOOTER_H,
                9, color=LBLUE, align=PP_ALIGN.CENTER)

    add_textbox(slide, str(page_num),
                W - Inches(1.0), H - FOOTER_H, Inches(0.9), FOOTER_H,
                10, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)


def add_content_header(slide, title_text):
    """コンテンツスライド共通ヘッダー"""
    add_rect(slide, 0, 0, W, HEADER_H, NAVY)
    add_rect(slide, 0, HEADER_H, W, Inches(0.04), RED)
    add_textbox(slide, title_text,
                Inches(0.6), Inches(0.2), Inches(10), Inches(0.7),
                24, bold=True, color=WHITE)
    # ヘッダー右端にロゴ（小・白ロゴ直置き）
    add_logo_white(slide, W - Inches(2.6), Inches(0.2), Inches(0.62))


# =============================================================
# スライド1: 表紙
# =============================================================
def slide_title(prs, title="プレゼンテーションタイトル",
                subtitle="サブタイトル・説明文をここに入力",
                date_str="20XX年XX月XX日"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景：紺
    add_rect(slide, 0, 0, W, H, NAVY)

    # 右の赤縦バー
    add_rect(slide, W - Inches(0.35), 0, Inches(0.35), H, RED)

    # 左上ロゴ（大・白ロゴ直置き）
    add_logo_white(slide, Inches(0.9), Inches(0.55), Inches(1.1))

    # 水平区切りライン
    add_rect(slide, Inches(0.9), Inches(2.1), W - Inches(1.25), Inches(0.04), RED)

    # メインタイトル
    add_textbox(slide, title,
                Inches(0.9), Inches(2.3), Inches(11), Inches(1.4),
                34, bold=True, color=WHITE)

    # サブタイトル
    add_textbox(slide, subtitle,
                Inches(0.9), Inches(3.85), Inches(11), Inches(0.7),
                16, color=LBLUE)

    # 日付・担当者
    add_textbox(slide, f"{date_str}　Aisunia",
                Inches(0.9), Inches(6.35), Inches(8), Inches(0.5),
                11, color=RGBColor(0x88, 0x99, 0xAA))

    return slide


# =============================================================
# スライド2: 目次
# =============================================================
def slide_agenda(prs, items=None, page_num=1, date_str=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_content_header(slide, "目次")
    add_rect(slide, 0, HEADER_H + Inches(0.04), W, H - HEADER_H - Inches(0.04) - FOOTER_H, GRAY)
    add_footer(slide, page_num, date_str)

    if items is None:
        items = [
            ("01", "現状課題の整理"),
            ("02", "ご提案内容"),
            ("03", "導入効果・事例"),
            ("04", "スケジュール・費用"),
            ("05", "まとめ・次のステップ"),
        ]

    for i, (num, label) in enumerate(items):
        y = Inches(1.4) + i * Inches(0.9)
        # 番号ボックス
        add_rect(slide, Inches(0.7), y, Inches(0.65), Inches(0.62), RED)
        add_textbox(slide, num,
                    Inches(0.7), y, Inches(0.65), Inches(0.62),
                    15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        # 区切り縦線
        add_rect(slide, Inches(1.5), y + Inches(0.08), Inches(0.04), Inches(0.45), LGRAY)
        # ラベル
        add_textbox(slide, label,
                    Inches(1.65), y + Inches(0.1), Inches(10), Inches(0.5),
                    17, color=NAVY)

    return slide


# =============================================================
# スライド3: コンテンツ（本文）
# =============================================================
def slide_content(prs, title="スライドタイトル", bullets=None,
                  page_num=2, date_str=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_content_header(slide, title)
    add_rect(slide, 0, HEADER_H + Inches(0.04), W, H - HEADER_H - Inches(0.04) - FOOTER_H, WHITE)
    add_footer(slide, page_num, date_str)

    if bullets is None:
        bullets = [
            "ここに本文・箇条書きの内容を入力します",
            "2つ目のポイントをここに書きます",
            "3つ目のポイントをここに書きます",
            "4つ目のポイントをここに書きます",
        ]

    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.5), Inches(5.4))
    tf = txBox.text_frame
    tf.word_wrap = True

    for j, b in enumerate(bullets):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.space_before = Pt(10)
        # 赤い先頭マーク
        r1 = p.add_run()
        r1.text = "▌ "
        r1.font.name = FONT
        r1.font.size = Pt(17)
        r1.font.color.rgb = RED
        # 本文
        r2 = p.add_run()
        r2.text = b
        r2.font.name = FONT
        r2.font.size = Pt(17)
        r2.font.color.rgb = DARK

    return slide


# =============================================================
# スライド4: セクション区切り
# =============================================================
def slide_section(prs, num="01", section_title="セクションタイトル"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 左半分：紺
    add_rect(slide, 0, 0, W * 0.42, H, NAVY)
    # 右半分：白
    add_rect(slide, W * 0.42, 0, W * 0.58, H, WHITE)
    # 縦の赤区切りライン
    add_rect(slide, W * 0.42 - Inches(0.04), 0, Inches(0.08), H, RED)

    # 左：セクション番号
    add_textbox(slide, num,
                Inches(0.7), Inches(1.8), Inches(4), Inches(2.0),
                72, bold=True, color=RGBColor(0x3A, 0x5A, 0x8A))

    # 右：セクションタイトル
    add_rect(slide, W * 0.42 + Inches(0.6), Inches(3.1), Inches(6.5), Inches(0.04), RED)
    add_textbox(slide, section_title,
                W * 0.42 + Inches(0.6), Inches(2.0), Inches(7.0), Inches(1.2),
                30, bold=True, color=NAVY)

    return slide


# =============================================================
# スライド5: 2カラム
# =============================================================
def slide_two_col(prs, title="比較・2カラムスライド",
                  left_head="左カラム見出し", left_body="内容をここに入力します。",
                  right_head="右カラム見出し", right_body="内容をここに入力します。",
                  page_num=3, date_str=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_content_header(slide, title)
    add_rect(slide, 0, HEADER_H + Inches(0.04), W, H - HEADER_H - Inches(0.04) - FOOTER_H, GRAY)
    add_footer(slide, page_num, date_str)

    for i, (head, body, accent) in enumerate([
        (left_head,  left_body,  NAVY),
        (right_head, right_body, RED),
    ]):
        x = Inches(0.5) + i * Inches(6.45)
        # カードエリア
        add_rect(slide, x, Inches(1.35), Inches(6.1), Inches(5.5), WHITE)
        # 見出し帯
        add_rect(slide, x, Inches(1.35), Inches(6.1), Inches(0.6), accent)
        # アンダーライン
        add_rect(slide, x, Inches(1.95), Inches(6.1), Inches(0.025), accent)
        add_textbox(slide, head,
                    x + Inches(0.15), Inches(1.37), Inches(5.8), Inches(0.55),
                    15, bold=True, color=WHITE)
        add_textbox(slide, body,
                    x + Inches(0.2), Inches(2.1), Inches(5.7), Inches(4.5),
                    14, color=DARK)

    return slide


# =============================================================
# スライド6: エンドスライド
# =============================================================
def slide_end(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景：紺
    add_rect(slide, 0, 0, W, H, NAVY)
    # 右縦バー：赤
    add_rect(slide, W - Inches(0.35), 0, Inches(0.35), H, RED)
    # 中央の横ライン
    add_rect(slide, Inches(0.9), Inches(3.6), W - Inches(1.25), Inches(0.04), RED)

    # メッセージ
    add_textbox(slide, "ご清聴ありがとうございました",
                Inches(0.9), Inches(1.6), W - Inches(1.25), Inches(1.2),
                34, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_textbox(slide, "ご不明な点はお気軽にお問い合わせください",
                Inches(0.9), Inches(2.75), W - Inches(1.25), Inches(0.6),
                14, color=LBLUE, align=PP_ALIGN.CENTER)

    # ロゴ（中央・白ロゴ直置き）
    logo_h = Inches(1.0)
    logo_w = logo_h * 3.0
    add_logo_white(slide, (W - logo_w) / 2, Inches(3.9), logo_h)

    # 連絡先
    add_textbox(slide, "アイサニア・コンサルティング　｜　中小企業診断士 × freee × AI自動化",
                Inches(0.9), Inches(5.15), W - Inches(1.25), Inches(0.5),
                13, color=LBLUE, align=PP_ALIGN.CENTER)

    add_textbox(slide, "https://www.aisunia.com　｜　yosuke-takeshita@aisunia.com",
                Inches(0.9), Inches(5.65), W - Inches(1.25), Inches(0.5),
                12, color=RGBColor(0x88, 0xBB, 0xFF), align=PP_ALIGN.CENTER)

    return slide


# =============================================================
# メイン
# =============================================================
def main():
    if not os.path.exists(LOGO_PATH):
        print(f"[WARN] ロゴ画像が見つかりません: {LOGO_PATH}")

    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H

    apply_color_theme(prs)

    slide_title(prs)
    slide_agenda(prs)
    slide_content(prs, page_num=2)
    slide_section(prs)
    slide_two_col(prs, page_num=3)
    slide_end(prs)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Aisunia_PowerPoint_Template.pptx")
    prs.save(out_path)
    patch_theme_in_pptx(out_path)
    print(f"[OK] 保存完了: {out_path}")


if __name__ == "__main__":
    main()
