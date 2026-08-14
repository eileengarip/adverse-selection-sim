import random
import matplotlib.pyplot as plt
import statistics
import math

random.seed(0)

RUNS = 300          # repetitions per data point
STEPS = 10000       # steps per run

# p_informed is the probability our trader is informed
def run(spread, p_informed=0.2, sigma=0.1, n=STEPS, k=None, skew=0.0):
    V = 100.0
    cash = 0.0
    inventory = 0
    trades = 0
    inventory_path = []

    for step in range(n):
        M = V
        V += random.gauss(0, sigma)

        # skew shifts both quotes against the current position (skew=0.0 -> unchanged)
        M_adjusted = M - skew * inventory

        # our bid and ask are quoted a step behind
        bid = M_adjusted - spread / 2
        ask = M_adjusted + spread / 2

        if random.random() < p_informed:
            if V > ask:
                cash += ask
                inventory -= 1
                trades += 1
            elif V < bid:
                cash -= bid
                inventory += 1
                trades += 1
        else:
            if k is None or random.random() < math.exp(-spread / k):
                coin_flip = random.choice(['trader_buys', 'trader_sells'])
                if coin_flip == 'trader_buys':
                    cash += ask
                    inventory -= 1
                    trades += 1
                else:
                    cash -= bid
                    inventory += 1
                    trades += 1

        inventory_path.append(inventory)

    return cash + inventory * V, trades, inventory_path


# ---- Table 1: adverse selection ----
print("p_informed, mean P&L, standard error")
for p in [0.0, 0.2, 0.4, 0.6, 0.8]:
    results = [run(0.10, p_informed=p)[0] for _ in range(RUNS)]
    mean = sum(results) / len(results)
    se = statistics.stdev(results) / (len(results) ** 0.5)
    print(f"{p:.1f}, {mean:8.1f}, {se:5.1f}")


# ---- Figure 1-2: spread curve and spread comparison ----
spreads = [i * 0.05 for i in range(21)]
pnls_broken = []
pnls_fixed = []

for spread in spreads:
    results = [run(spread)[0] for _ in range(RUNS)]
    pnls_broken.append(sum(results) / len(results))

for spread in spreads:
    results = [run(spread, k=0.5)[0] for _ in range(RUNS)]
    pnls_fixed.append(sum(results) / len(results))

plt.figure(figsize=(7, 5))
plt.plot(spreads, pnls_broken, marker='o')
plt.axhline(0, color='grey', linewidth=0.8)
plt.xlabel('spread')
plt.ylabel(f'mean P&L ({STEPS:,} steps)')
plt.savefig('spread_curve.png', dpi=110, bbox_inches='tight')
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(spreads, pnls_broken, marker='o', label='price-insensitive noise traders')
plt.plot(spreads, pnls_fixed, marker='s', label='with arrival decay (k = 0.5)')
plt.axhline(0, color='grey', linewidth=0.8)
plt.xlabel('spread')
plt.ylabel(f'mean P&L ({STEPS:,} steps)')
plt.legend()
plt.savefig('spread_comparison.png', dpi=110, bbox_inches='tight')
plt.close()


# ---- Figure 3: inventory paths, with and without skewing ----
_, _, path_unskewed = run(0.5, k=0.5, skew=0.0)
_, _, path_skewed   = run(0.5, k=0.5, skew=0.01)

plt.figure(figsize=(8, 4.5))
plt.plot(path_unskewed, label='no skew', linewidth=0.9)
plt.plot(path_skewed, label='skew = 0.01', linewidth=0.9)
plt.axhline(0, color='grey', linewidth=0.8)
plt.xlabel('step')
plt.ylabel('inventory')
plt.legend()
plt.savefig('inventory_comparison.png', dpi=110, bbox_inches='tight')
plt.close()


# ---- Table 2 and Figure 4: skew sweep and risk-return frontier ----
skews = [0, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.05, 0.1]
means = []
sds = []

print("skew, mean P&L, std dev, standard error")
for skew in skews:
    results = [run(0.5, k=0.5, skew=skew)[0] for _ in range(RUNS)]
    mean = sum(results) / len(results)
    sd = statistics.stdev(results)
    means.append(mean)
    sds.append(sd)
    print(f"{skew:.4f}, {mean:7.1f}, {sd:7.1f}, {sd / (RUNS ** 0.5):5.1f}")

plt.figure(figsize=(7, 5))
plt.plot(sds, means, marker='o', color='tab:purple')
for s, m, d in zip(skews, means, sds):
    plt.annotate(f'{s}', (d, m), textcoords='offset points', xytext=(6, 5), fontsize=8)
plt.xlabel('standard deviation of P&L (risk)')
plt.ylabel('mean P&L (return)')
plt.savefig('skew_frontier.png', dpi=110, bbox_inches='tight')
plt.close()