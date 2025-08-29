import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("src/qlearning_tuning_results.csv")

# Drop rows where 'best_fitness' is NaN
df_cleaned = df.dropna(subset=['best_fitness'])

# Find the row with the highest 'best_fitness'
if not df_cleaned.empty:
    best_row = df_cleaned.loc[df_cleaned['best_fitness'].idxmax()]
    print("Best row:")
    print(best_row)
else:
    print("No valid best fitness values found.")

print("Summary statistics:")
print(df.groupby(["alpha", "gamma", "epsilon_start", "epsilon_end"])["best_fitness"].agg(['mean', 'std', 'max', 'min']))

# # find best parameter combination
# best_row = df.loc[df['best_fitness'].idxmax()]
# print("\nBest parameter combination:")
# print(best_row)

# plot: best fitness by alpha/gamma
plt.figure(figsize=(10,6))
sns.boxplot(x="alpha", y="best_fitness", hue="gamma", data=df)
plt.title("Best Fitness by Alpha and Gamma")
plt.savefig("fitness_by_alpha_gamma.png")
plt.show()

# plot: best fitness by epsilon_start/epsilon_end
plt.figure(figsize=(10,6))
sns.boxplot(x="epsilon_start", y="best_fitness", hue="epsilon_end", data=df)
plt.title("Best Fitness by Epsilon Start/End")
plt.savefig("fitness_by_epsilon.png")
plt.show()

# optional: Heatmap of mean fitness for all parameter combos
pivot = df.pivot_table(index="alpha", columns="gamma", values="best_fitness", aggfunc="mean")
plt.figure(figsize=(8,6))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="viridis")
plt.title("Mean Best Fitness (alpha vs gamma)")