import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def draw_node(ax, text, xy, boxstyle="round,pad=0.3", color="lightblue"):
    ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle=boxstyle, facecolor=color, edgecolor="black"))

def draw_arrow(ax, start, end, label=""):
    ax.annotate(label, xy=end, xytext=start,
                arrowprops=dict(arrowstyle="->", lw=1.5),
                ha="center", va="center", fontsize=9)

fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].set_title("Loan Approval Decision Tree")
axs[1].set_title("Disease Diagnosis Decision Tree")

# Loan Approval Tree
draw_node(axs[0], "Income Level?", (0.5, 0.9))
draw_node(axs[0], "Credit Score?", (0.3, 0.6))
draw_node(axs[0], "Credit Score?", (0.7, 0.6))
draw_node(axs[0], "No", (0.2, 0.3), color="salmon")
draw_node(axs[0], "Yes", (0.4, 0.3), color="lightgreen")
draw_node(axs[0], "No", (0.6, 0.3), color="salmon")
draw_node(axs[0], "Yes", (0.8, 0.3), color="lightgreen")

draw_arrow(axs[0], (0.5, 0.9), (0.3, 0.6), "Low/Medium")
draw_arrow(axs[0], (0.5, 0.9), (0.7, 0.6), "High")
draw_arrow(axs[0], (0.3, 0.6), (0.2, 0.3), "Poor")
draw_arrow(axs[0], (0.3, 0.6), (0.4, 0.3), "Good")
draw_arrow(axs[0], (0.7, 0.6), (0.6, 0.3), "Poor")
draw_arrow(axs[0], (0.7, 0.6), (0.8, 0.3), "Good")

axs[0].axis("off")

# Disease Diagnosis Tree
draw_node(axs[1], "Fever?", (0.5, 0.9))
draw_node(axs[1], "Cough?", (0.3, 0.6))
draw_node(axs[1], "Cough?", (0.7, 0.6))
draw_node(axs[1], "No", (0.2, 0.3), color="salmon")
draw_node(axs[1], "Yes", (0.4, 0.3), color="lightgreen")
draw_node(axs[1], "No", (0.6, 0.3), color="salmon")
draw_node(axs[1], "Yes", (0.8, 0.3), color="lightgreen")

draw_arrow(axs[1], (0.5, 0.9), (0.3, 0.6), "No")
draw_arrow(axs[1], (0.5, 0.9), (0.7, 0.6), "Yes")
draw_arrow(axs[1], (0.3, 0.6), (0.2, 0.3), "No")
draw_arrow(axs[1], (0.3, 0.6), (0.4, 0.3), "Yes")
draw_arrow(axs[1], (0.7, 0.6), (0.6, 0.3), "No")
draw_arrow(axs[1], (0.7, 0.6), (0.8, 0.3), "Yes")

axs[1].axis("off")

plt.tight_layout()
plt.show()