import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis("off")
fig.patch.set_facecolor("#f8f9fa")

def box(ax, x, y, w, h, label, sublabel="", color="#ffffff", border="#333333", fontsize=10):
    rect = mpatches.FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.1",
        linewidth=1.5,
        edgecolor=border,
        facecolor=color,
        zorder=3,
    )
    ax.add_patch(rect)
    ax.text(x, y + (0.15 if sublabel else 0), label, ha="center", va="center",
            fontsize=fontsize, fontweight="bold", color="#1a1a1a", zorder=4)
    if sublabel:
        ax.text(x, y - 0.28, sublabel, ha="center", va="center",
                fontsize=7.5, color="#555555", zorder=4)

def arrow(ax, x1, y1, x2, y2, label="", color="#555555"):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4),
        zorder=2,
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.08, my, label, ha="left", va="center",
                fontsize=7.5, color="#333333",
                bbox=dict(fc="#f8f9fa", ec="none", pad=1), zorder=5)

# ── Nodes ──────────────────────────────────────────────────────────────────
box(ax,  7.0, 9.0, 2.4, 0.8, "[ Player ]",               color="#dff0d8", border="#4cae4c")
box(ax,  7.0, 7.3, 2.8, 0.8, "Streamlit UI",  "app.py", color="#d9edf7", border="#2980b9")
box(ax,  3.2, 5.5, 2.8, 0.8, "Logic Utils",   "logic_utils.py", color="#d9edf7", border="#2980b9")
box(ax,  7.0, 5.5, 2.8, 0.8, "AI Coach",      "ai_coach.py",    color="#e8d5f5", border="#8e44ad")
box(ax, 10.8, 5.5, 2.4, 0.8, "Claude API",    "claude-haiku",   color="#f5e6ff", border="#9b59b6")
box(ax,  7.0, 3.5, 2.8, 0.8, "Logger",        "glitch_detective.log", color="#f5f5f5", border="#95a5a6")
box(ax,  3.2, 1.8, 2.8, 0.8, "Reliability Tester", "test_reliability.py", color="#fef9e7", border="#f39c12")
box(ax,  7.0, 1.8, 2.4, 0.8, "[ Developer ]",           color="#dff0d8", border="#4cae4c")

# ── Arrows ─────────────────────────────────────────────────────────────────
arrow(ax,  7.0, 8.6,  7.0, 7.7,  "enters guess")
arrow(ax,  6.0, 7.1,  4.6, 5.9,  "raw input")
arrow(ax,  4.6, 5.1,  6.0, 7.0,  "Win / Too High / Too Low")
arrow(ax,  7.0, 6.9,  7.0, 5.9,  "history, range,\nattempts left")
arrow(ax,  8.4, 5.5, 9.6, 5.5,   "prompt")
arrow(ax,  9.6, 5.2, 8.4, 5.2,   "coaching hint")
arrow(ax,  7.0, 5.1,  7.0, 3.9,  "logs call + response")
arrow(ax,  7.0, 6.9,  7.0, 7.7)   # hint back up — handled by return arrow below
arrow(ax,  7.3, 7.7,  7.3, 8.6,  "outcome + hint")
arrow(ax,  3.2, 2.2,  7.0, 5.1,  "test scenarios")
arrow(ax,  7.0, 5.1,  4.6, 2.2,  "AI responses")
arrow(ax,  4.6, 1.8,  6.0, 1.8,  "pass/fail report")

# ── Legend ─────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(facecolor="#d9edf7", edgecolor="#2980b9", label="Game Layer"),
    mpatches.Patch(facecolor="#e8d5f5", edgecolor="#8e44ad", label="AI Coach Layer"),
    mpatches.Patch(facecolor="#fef9e7", edgecolor="#f39c12", label="Testing Layer"),
    mpatches.Patch(facecolor="#f5f5f5", edgecolor="#95a5a6", label="Logger / Guardrail"),
]
ax.legend(handles=legend_items, loc="lower right", fontsize=8.5,
          framealpha=0.9, edgecolor="#cccccc")

ax.set_title("Game Glitch Investigator — System Architecture",
             fontsize=13, fontweight="bold", pad=12, color="#1a1a1a")

out = "/Users/harrisonpark16/Desktop/claude/ai110-module1show-gameglitchinvestigator-starter-main/assets/architecture.png"
plt.tight_layout()
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {out}")
