import numpy as np
from pathlib import Path


SEED = 42
rng = np.random.default_rng(SEED)

P = 0.3
INSTANCES_PER_SIZE = 10

SIZES = {
    "small": [10, 15, 20],
    "medium": [25, 30, 40, 50],
    "large": [75, 100, 150],
}


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def generate_graph(n, p):
    graph = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                graph[i][j] = 1
                graph[j][i] = 1

    return graph


for category, sizes in SIZES.items():

    category_dir = DATA_DIR / category
    category_dir.mkdir(parents=True, exist_ok=True)

    for n in sizes:

        for instance_id in range(1, INSTANCES_PER_SIZE + 1):

            graph = generate_graph(n, P)

            filename = (
                f"{category}_n{n}_{instance_id:02d}.npy"
            )

            path = category_dir / filename

            np.save(path, graph)

            print(f"Generated: {path}")