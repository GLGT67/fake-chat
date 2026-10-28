import os
import xml.etree.ElementTree as ET
from androguard.core.axml import AXMLPrinter

drawable_dir = r"c:\Users\Admin\Desktop\ai rules and skills\extracted_apk\com_fakechat_unpacked\res\drawable"
out_svg_dir = r"c:\Users\Admin\Desktop\ai rules and skills\fake-chat\src\assets\zalo_icons"
os.makedirs(out_svg_dir, exist_ok=True)

android_ns = "{http://schemas.android.com/apk/res/android}"
zalo_files = [f for f in os.listdir(drawable_dir) if "zalo" in f and f.endswith(".xml")]

print(f"Decoding {len(zalo_files)} zalo drawables...")

for f in zalo_files:
    in_path = os.path.join(drawable_dir, f)
    try:
        with open(in_path, "rb") as fp:
            axml = AXMLPrinter(fp.read())
            xml_bytes = axml.get_xml()
        
        root = ET.fromstring(xml_bytes)
        if "vector" in root.tag:
            w = root.get(android_ns + "viewportWidth", "24")
            h = root.get(android_ns + "viewportHeight", "24")
            paths = []
            for child in root.iter():
                if child.tag.endswith("path"):
                    d = child.get(android_ns + "pathData")
                    fill = child.get(android_ns + "fillColor", "currentColor")
                    stroke = child.get(android_ns + "strokeColor", "none")
                    sw = child.get(android_ns + "strokeWidth", "0")
                    if d:
                        if fill and fill.startswith("@"):
                            fill = "currentColor"
                        paths.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" />')
            
            svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">\n' + "\n".join(paths) + "\n</svg>"
            svg_name = f.replace(".xml", ".svg")
            with open(os.path.join(out_svg_dir, svg_name), "w", encoding="utf-8") as out_f:
                out_f.write(svg_content)
            print(f"Converted: {f} -> {svg_name}")
    except Exception as e:
        print(f"Skip {f}: {e}")

