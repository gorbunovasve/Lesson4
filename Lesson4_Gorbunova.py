import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn
import plotly
import nbformat
import os
os.makedirs("images", exist_ok=True)
df = pd.read_csv('student_career_success_dataset.csv')

Salary = "Starting_Salary_USD"
Field = "Career_Field"
Average_Sal_Count = (
    df.groupby(Field)[Salary]
    .agg(Average_Salary="mean", Count="count")
    .reset_index()
    .round({"Average_Salary": 0})
    .astype({"Average_Salary": int})
    .sort_values(by="Average_Salary", ascending=False)
)
row_A = len(Average_Sal_Count)

Gender_Counts = pd.crosstab(df[Field], df["Gender"]).reset_index()
Average_Sal_Count = Average_Sal_Count.merge(Gender_Counts, on=Field).sort_values(
    by="Average_Salary", ascending=False)
row_C = len(Gender_Counts)
assert row_A == row_C
assert Average_Sal_Count["Count"].notna().all()

#print(Average_Sal_Count)
#print(Average_Sal_Count["Count"].describe().round(1))
#print("mean", round(Average_Sal_Count["Count"].mean(), 1))
#print("median", Average_Sal_Count["Count"].median())
rev = Gender_Counts[["Female", "Male"]].sum()
plt.bar(rev.index, rev.values, color="#1C6D5D")
plt.ylim(0, rev.max() * 1.1)
plt.title("Кількість жінок та чоловіків в виборці")
plt.ylabel("Кількість")
plt.show()


rev = Gender_Counts[["Female", "Male"]].sum()
total = rev.sum()  
plt.figure(figsize=(6, 5))
bars = plt.bar(rev.index, rev.values, color=["#AC0F60", "#2234D4"], width=0.5)
min_val = rev.min()
max_val = rev.max()
diff = max_val - min_val
plt.ylim(min_val - diff * 2, max_val + diff * 0.8)
plt.grid(axis="y", linestyle="--", alpha=0.5)
for bar in bars:
    height = bar.get_height()
    pct = (height / total) * 100
    count_str = f"{int(height):,}".replace(",", " ")
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + diff * 0.15,
        f"{count_str} ({pct:.1f}%)", 
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold",
    )
plt.title("Кількість жінок та чоловіків у вибірці", fontsize=13, pad=15)
plt.ylabel("Кількість")
plt.tight_layout()
plt.savefig("images/gender_distribution1.png", dpi=300, bbox_inches="tight")
plt.show()



df_sorted = Average_Sal_Count.sort_values(by="Count", ascending=True)
plt.figure(figsize=(10, len(df_sorted) * 0.55 + 2))
bars_f = plt.barh(
    df_sorted[Field],
    df_sorted["Female"],
    color="#E07A5F",
    height=0.6,
    label="Female",
)
bars_m = plt.barh(
    df_sorted[Field],
    df_sorted["Male"],
    left=df_sorted["Female"],
    color="#3D405B",
    height=0.6,
    label="Male",
)
max_val = df_sorted["Count"].max()

for i, (_, row) in enumerate(df_sorted.iterrows()):
    f_val = int(row["Female"])
    m_val = int(row["Male"])
    total_val = int(row["Count"])
    plt.text(
        f_val / 2,
        i,
        f"{f_val:,}".replace(",", " "),
        va="center",
        ha="center",
        color="white",
        fontsize=9,
        fontweight="bold",
    )
    plt.text(
        f_val + m_val / 2,
        i,
        f"{m_val:,}".replace(",", " "),
        va="center",
        ha="center",
        color="white",
        fontsize=9,
        fontweight="bold",
    )
    plt.text(
        total_val + max_val * 0.01,
        i,
        f"{total_val:,}".replace(",", " "),
        va="center",
        ha="left",
        color="black",
        fontsize=9.5,
        fontweight="bold",
    )

plt.xlim(0, max_val * 1.15)
plt.grid(axis="x", linestyle="--", alpha=0.5)
plt.legend(title="Стать", loc="lower right")

plt.title("Розподіл жінок та чоловіків за спеціальностями", fontsize=13, pad=15)
plt.xlabel("Кількість")
plt.ylabel("Спеціальність")
plt.tight_layout()
manager = plt.get_current_fig_manager()
manager.window.state("zoomed")
plt.savefig("images/gender_distribution2.png", dpi=300, bbox_inches="tight")
plt.show()


placed = df[df["Starting_Salary_USD"] > 0]
x = placed["Programming_Skill"]      
y = placed["Starting_Salary_USD"]  
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color="#C91289", alpha=0.4)  # alpha=0.4 делает точки полупрозрачными, чтобы видеть скопления
plt.xlabel("Навички програмування")
plt.ylabel("Зарплата")
plt.title("Связь между навичками програмування и зарплатой (1 точка = 1 студент)")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
manager = plt.get_current_fig_manager()
manager.window.state("zoomed")
plt.savefig("images/salary_scatter.png", dpi=300, bbox_inches="tight")
plt.show()


placed = df[df["Starting_Salary_USD"] > 0]
skills = sorted(placed["Programming_Skill"].unique())
salary_by_skill = [
    placed[placed["Programming_Skill"] == skill]["Starting_Salary_USD"]
    for skill in skills
]
plt.figure(figsize=(10, 6))
box = plt.boxplot(
    salary_by_skill,
    tick_labels=skills,
    patch_artist=True,  # Дозволяє зафарбувати «ящики»
    medianprops=dict(color="#E07A5F", linewidth=2.5),  # Яскрава лінія медіани
    boxprops=dict(facecolor="#3D405B", color="#47509E", alpha=0.8),
    whiskerprops=dict(color="#3D405B", linewidth=1.2),
    capprops=dict(color="#3D405B", linewidth=1.2),
    flierprops=dict(marker="o", markersize=3, alpha=0.3, markeredgecolor="#3D405B"),
)
for i, data in enumerate(salary_by_skill, start=1):
    med = data.median()
    plt.text(
        i,
        med + 1200,
        f"${med:,.0f}".replace(",", " "),
        ha="center",
        va="bottom",
        color="white",
        fontsize=8.5,
        fontweight="bold",
    )
plt.title("Розподіл та медіана стартової зарплати за рівнем навичок програмування", fontsize=12, pad=12)
plt.xlabel("Навички програмування (бали)")
plt.ylabel("Стартова зарплата (USD)")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
manager = plt.get_current_fig_manager()
manager.window.state("zoomed")
plt.savefig("images/salary_boxplot.png", dpi=300, bbox_inches="tight")
plt.show()