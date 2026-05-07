"""
Aisunia PowerPoint テンプレート（.potx）ベース生成スクリプト
B案：スライドサイズ・テーマカラー・フォントを設定済みの空テンプレ(.potx)を生成。
レイアウト削除と6レイアウト作成は PowerPoint 上で手作業。
"""

import os
import shutil
import zipfile

from pptx import Presentation
from pptx.util import Inches


W = Inches(13.333)
H = Inches(7.5)

THEME_SCHEME = {
    "name": "Aisunia",
    "dk1": "1A2B4A", "lt1": "FFFFFF",
    "dk2": "222222", "lt2": "F4F6F8",
    "accent1": "BC002D",
    "accent2": "1A2B4A",
    "accent3": "5C7A99",
    "accent4": "3D5C7A",
    "accent5": "7A8FA6",
    "accent6": "9CA3AF",
    "hlink": "BC002D",
    "folHlink": "551014",
}


def build_theme_xml(scheme):
    ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="{ns}" name="{scheme['name']}">
  <a:themeElements>
    <a:clrScheme name="{scheme['name']}">
      <a:dk1><a:srgbClr val="{scheme['dk1']}"/></a:dk1>
      <a:lt1><a:srgbClr val="{scheme['lt1']}"/></a:lt1>
      <a:dk2><a:srgbClr val="{scheme['dk2']}"/></a:dk2>
      <a:lt2><a:srgbClr val="{scheme['lt2']}"/></a:lt2>
      <a:accent1><a:srgbClr val="{scheme['accent1']}"/></a:accent1>
      <a:accent2><a:srgbClr val="{scheme['accent2']}"/></a:accent2>
      <a:accent3><a:srgbClr val="{scheme['accent3']}"/></a:accent3>
      <a:accent4><a:srgbClr val="{scheme['accent4']}"/></a:accent4>
      <a:accent5><a:srgbClr val="{scheme['accent5']}"/></a:accent5>
      <a:accent6><a:srgbClr val="{scheme['accent6']}"/></a:accent6>
      <a:hlink><a:srgbClr val="{scheme['hlink']}"/></a:hlink>
      <a:folHlink><a:srgbClr val="{scheme['folHlink']}"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="{scheme['name']}">
      <a:majorFont>
        <a:latin typeface="BIZ UDPGothic"/>
        <a:ea typeface="BIZ UDPゴシック"/>
        <a:cs typeface=""/>
      </a:majorFont>
      <a:minorFont>
        <a:latin typeface="BIZ UDPGothic"/>
        <a:ea typeface="BIZ UDPゴシック"/>
        <a:cs typeface=""/>
      </a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="{scheme['name']}">
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


def patch_theme_xml(pptx_path, scheme):
    theme_xml = build_theme_xml(scheme)
    target = "ppt/theme/theme1.xml"
    tmp = pptx_path + ".tmp"
    with zipfile.ZipFile(pptx_path, "r") as zin, \
         zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = theme_xml.encode("utf-8") if item.filename == target else zin.read(item.filename)
            zout.writestr(item, data)
    shutil.move(tmp, pptx_path)


def convert_pptx_to_potx(pptx_path, potx_path):
    """[Content_Types].xml の MIME を template に置換し、.potx として保存する。"""
    pptx_type = b"application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"
    potx_type = b"application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"

    tmp = pptx_path + ".tmp"
    with zipfile.ZipFile(pptx_path, "r") as zin, \
         zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(pptx_type, potx_type)
            zout.writestr(item, data)
    shutil.move(tmp, potx_path)
    if os.path.exists(pptx_path):
        os.remove(pptx_path)


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    os.makedirs(out_dir, exist_ok=True)
    pptx_tmp = os.path.join(out_dir, "_aisunia_base_temp.pptx")
    potx_out = os.path.join(out_dir, "Aisunia_Template.potx")

    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    prs.save(pptx_tmp)

    patch_theme_xml(pptx_tmp, THEME_SCHEME)
    convert_pptx_to_potx(pptx_tmp, potx_out)

    print(f"[OK] 生成完了: {potx_out}")
    print(f"     スライドサイズ: 33.87cm x 19.05cm（標準16:9）")
    print(f"     テーマ名: {THEME_SCHEME['name']}")
    print(f"     accent1=#{THEME_SCHEME['accent1']} (赤) / accent2=#{THEME_SCHEME['accent2']} (紺) / accent3=#{THEME_SCHEME['accent3']} (スレートブルー)")
    print(f"     フォント: BIZ UDPゴシック / BIZ UDPGothic")


if __name__ == "__main__":
    main()
