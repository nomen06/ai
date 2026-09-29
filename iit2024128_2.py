import math
import random

cities = {
    1: (60, 200), 2: (23, 45), 3: (15, 150), 4: (85, 90), 5: (71, 123),
    6: (98, 45), 7: (50, 220), 8: (20, 30), 9: (40, 180), 10: (75, 155),
    11: (82, 60), 12: (91, 120), 13: (12, 210), 14: (37, 100), 15: (28, 77),
    16: (66, 89), 17: (55, 130), 18: (73, 140), 19: (88, 33), 20: (42, 170),
}

HUB = 1
MUT_RATE = 0.3
RUNS = 10


def dist(a, b):
    return math.hypot(cities[a][0] - cities[b][0], cities[a][1] - cities[b][1])


def total_distance(route):
    d = sum(dist(route[i], route[i + 1]) for i in range(len(route) - 1))
    return d + dist(route[-1], route[0])


def fitness(route):
    return 1 / total_distance(route)


def create_population(size):
    others = [c for c in cities if c != HUB]
    pop = []
    for _ in range(size):
        random.shuffle(others)
        pop.append([HUB] + others[:])
    return pop


def roulette(pop):
    fits = [fitness(r) for r in pop]
    r = random.uniform(0, sum(fits))
    cum = 0
    for route, f in zip(pop, fits):
        cum += f
        if r <= cum:
            return route
    return pop[-1]


def order_crossover(p1, p2):
    n = len(p1)
    s, e = sorted(random.sample(range(1, n), 2))
    child = [None] * n
    child[0] = HUB
    child[s:e + 1] = p1[s:e + 1]
    rest = iter([c for c in p2 if c not in child])
    for i in range(1, n):
        if child[i] is None:
            child[i] = next(rest)
    return child


def mutate(route):
    if random.random() < MUT_RATE:
        i, j = random.sample(range(1, len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route


def genetic_algorithm(pop_size, generations):
    pop = create_population(pop_size)
    for _ in range(generations):
        new_pop = [min(pop, key=total_distance)[:]]
        while len(new_pop) < pop_size:
            child = order_crossover(roulette(pop), roulette(pop))
            new_pop.append(mutate(child))
        pop = new_pop
    best = min(pop, key=total_distance)
    return best, total_distance(best)


def show(route):
    return " -> ".join(map(str, route + [HUB]))


configs = [("A", 10, 100), ("B", 20, 100), ("C", 30, 100),
           ("D", 10, 200), ("E", 20, 200), ("F", 30, 200)]

summary = []
for name, pop_size, gens in configs:
    results = []
    for run in range(RUNS):
        random.seed(42 + run)
        results.append(genetic_algorithm(pop_size, gens))
    first = results[0]
    best = min(results, key=lambda x: x[1])
    avg = sum(c for _, c in results) / RUNS

    print(f"\nConfig {name}: Population = {pop_size}, Generations = {gens}")
    print("Seed-42 run:")
    print("  Tour    :", show(first[0]))
    print(f"  Distance: {first[1]:.2f}")
    print(f"Best of {RUNS} runs:")
    print("  Tour    :", show(best[0]))
    print(f"  Distance: {best[1]:.2f}")
    print(f"Average of {RUNS} runs: {avg:.2f}")
    summary.append((name, pop_size, gens, first[1], best[1], avg))

print("\nCfg  Pop  Gens  Seed-42   Best      Average")
for name, p, g, f, b, a in summary:
    print(f"{name:<5}{p:<5}{g:<6}{f:<10.2f}{b:<10.2f}{a:.2f}")
