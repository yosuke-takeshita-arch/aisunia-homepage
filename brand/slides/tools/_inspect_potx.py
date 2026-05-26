import zipfile
import sys
import io
import re
from lxml import etree

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

POTX = r"C:\Users\Panasonic\Documents\Projects\homepage-builder\brand\slides\outputs\Aisunia_Template.potx"

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def emu_to_cm(emu):
    if emu is None:
        return None
    return round(int(emu) / 360000, 2)


def describe_layout(z, name):
    xml = z.read(name)
    root = etree.fromstring(xml)
    cSld = root.find("p:cSld", NS)
    layout_name = cSld.get("name") if cSld is not None else "(no name)"
    print(f"\n[{name}] name='{layout_name}'  type='{root.get('type')}'")
    spTree = cSld.find("p:spTree", NS)
    for sp in spTree.findall("p:sp", NS):
        nvSpPr = sp.find("p:nvSpPr", NS)
        nvPr = nvSpPr.find("p:nvPr", NS) if nvSpPr is not None else None
        ph = nvPr.find("p:ph", NS) if nvPr is not None else None
        cNvPr = nvSpPr.find("p:cNvPr", NS) if nvSpPr is not None else None
        shape_name = cNvPr.get("name") if cNvPr is not None else ""
        spPr = sp.find("p:spPr", NS)
        xfrm = spPr.find("a:xfrm", NS) if spPr is not None else None
        off = xfrm.find("a:off", NS) if xfrm is not None else None
        ext = xfrm.find("a:ext", NS) if xfrm is not None else None
        pos = ""
        if off is not None or ext is not None:
            x = emu_to_cm(off.get("x")) if off is not None else "-"
            y = emu_to_cm(off.get("y")) if off is not None else "-"
            cx = emu_to_cm(ext.get("cx")) if ext is not None else "-"
            cy = emu_to_cm(ext.get("cy")) if ext is not None else "-"
            pos = f" pos=({x},{y}) size=({cx}x{cy})"
        # テキスト取得
        txBody = sp.find("p:txBody", NS)
        text_preview = ""
        if txBody is not None:
            texts = []
            for t in txBody.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"):
                if t.text:
                    texts.append(t.text)
            joined = " | ".join(texts)
            if joined:
                text_preview = f" text='{joined[:60]}'"
        if ph is not None:
            ph_type = ph.get("type", "(body)")
            ph_idx = ph.get("idx", "-")
            print(f"  [PH] type={ph_type} idx={ph_idx} name='{shape_name}'{pos}{text_preview}")
        else:
            print(f"  [SP] name='{shape_name}'{pos}{text_preview}")


with zipfile.ZipFile(POTX) as z:
    names = sorted([n for n in z.namelist() if "slideLayouts/slideLayout" in n and n.endswith(".xml")])
    for n in names:
        describe_layout(z, n)
    # マスタも見る
    describe_layout(z, "ppt/slideMasters/slideMaster1.xml")
