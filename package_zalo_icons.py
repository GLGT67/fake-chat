import os
import re

svg_dir = r"c:\Users\Admin\Desktop\ai rules and skills\fake-chat\src\assets\zalo_icons"
out_svelte = r"c:\Users\Admin\Desktop\ai rules and skills\fake-chat\src\lib\ZaloIcon.svelte"

icons = {}

for f in sorted(os.listdir(svg_dir)):
    if not f.endswith(".svg"):
        continue
    key = f.replace("ic_", "").replace("_zalo", "").replace(".svg", "")
    with open(os.path.join(svg_dir, f), "r", encoding="utf-8") as fp:
        raw_svg = fp.read().strip()
    
    # Replace solid fills with currentColor so classes text-white, text-blue etc work seamlessly
    # Keep orange/amber for image icon if desired or make it currentColor
    svg_clean = re.sub(r'fill="#FF[0-9A-Fa-f]{6}"', 'fill="currentColor"', raw_svg)
    svg_clean = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="currentColor"', svg_clean)
    svg_clean = svg_clean.replace("\n", " ").replace("  ", " ")
    icons[key] = svg_clean

# Also add special helpers like qr and explore
icons["qr"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h6v6H3zM15 3h6v6h-6zM3 15h6v6H3zM15 15h2v2h-2zM19 15h2v2h-2zM15 19h2v2h-2zM19 19h2v2h-2z"/></svg>'
icons["explore"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>'
icons["timeline"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><line x1="7" y1="8" x2="17" y2="8"/><line x1="7" y1="12" x2="13" y2="12"/></svg>'
icons["heart"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>'

js_entries = []
for k, v in icons.items():
    escaped_v = v.replace("`", "\\`")
    js_entries.append(f'    "{k}": `{escaped_v}`')

joined_entries = ',\n'.join(js_entries)
content = f"""<script>
  const {{ name, size = 24, class: className = "" }} = $props();

  const ICONS = {{
{joined_entries}
  }};
</script>

<span 
  class="inline-flex items-center justify-center shrink-0 {{className}}"
  style="width: {{size}}px; height: {{size}}px;"
>
  {{@html ICONS[name] || ""}}
</span>
"""

with open(out_svelte, "w", encoding="utf-8") as fp:
    fp.write(content)

print(f"Generated {out_svelte} with {len(icons)} icons!")
