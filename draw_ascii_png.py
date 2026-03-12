import matplotlib
import csv
import sys

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.font_manager import FontProperties

if len(sys.argv) < 2:
    print("Usage: python draw_ascii_png.py <input.csv>")
    sys.exit(1)

csv_path = sys.argv[1]
with open(csv_path, newline='') as f:
    reader = csv.reader(f)
    col_labels = next(reader)
    data = [row for row in reader]
fontsize = 12
dpi = 180

# Measure actual pixel widths using renderer
tmp_fig = plt.figure(figsize=(1, 1), dpi=dpi)
canvas = FigureCanvasAgg(tmp_fig)
renderer = canvas.get_renderer()


def get_text_width_inches(s, props):
    t = tmp_fig.text(0, 0, s, fontproperties=props)
    bb = t.get_window_extent(renderer=renderer)
    t.remove()
    return bb.width / dpi


fp = FontProperties(size=fontsize)
fp_mono_bold = FontProperties(size=fontsize, weight='bold', family='monospace')

# Max width per column + 2 spaces padding
max_w0 = max(get_text_width_inches(t + "  ", fp_mono_bold) for t in [col_labels[0]] + [r[0] for r in data])
max_w1 = max(get_text_width_inches(t + "  ", fp) for t in [col_labels[1]] + [r[1] for r in data])
max_w2 = max(get_text_width_inches(t + "  ", fp) for t in [col_labels[2]] + [r[2] for r in data])

plt.close(tmp_fig)

total_w = max_w0 + max_w1 + max_w2
fig_width = total_w + 0.3
nrows = len(data) + 1
row_height = 0.3
fig_height = nrows * row_height

w0_ratio = max_w0 / total_w
w1_ratio = max_w1 / total_w
w2_ratio = max_w2 / total_w

fig = plt.figure(figsize=(fig_width, fig_height))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

table = ax.table(
    cellText=data,
    colLabels=col_labels,
    cellLoc='left',
    loc='center',
    colWidths=[w0_ratio, w1_ratio, w2_ratio],
)

table.auto_set_font_size(False)
table.set_fontsize(fontsize)

ncols = len(col_labels)

for i in range(nrows):
    for j in range(ncols):
        cell = table[i, j]
        cell.set_height(1.0 / nrows)
        cell.PAD = 0.01

# Header: no shading, no bold, center aligned
for j in range(ncols):
    cell = table[0, j]
    cell.set_facecolor('white')
    cell.set_edgecolor('#dddddd')
    cell.set_text_props(ha='center', fontsize=fontsize)

# Data rows
for i in range(1, len(data) + 1):
    for j in range(ncols):
        table[i, j].set_facecolor('white')
        table[i, j].set_edgecolor('#dddddd')
    table[i, 0].set_text_props(fontweight='bold', fontfamily='monospace')
    table[i, 1].set_text_props(ha='right')
    table[i, 2].set_text_props(ha='left')

out = "./"
fig.savefig(out, dpi=dpi, pad_inches=0, facecolor='white')
print(f"Saved to {out}")
print(f"Fig size: {fig_width:.1f} x {fig_height:.1f} inches")