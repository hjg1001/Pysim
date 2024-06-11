import numpy as np
# THIS CODE WAS FOUND ONLINE ON A PUBLIC REPO AND NOT WRITTEN BY MYSELF
def generate_noise(shape, res, tileable=(False, False)):
    def interpolant(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def fn(x):
        return int((x + 1) * 122)

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]] \
               .transpose(1, 2, 0) % 1
    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    if tileable[0]:
        gradients[-1, :] = gradients[0, :]
    if tileable[1]:
        gradients[:, -1] = gradients[:, 0]
    gradients = gradients.repeat(d[0], 0).repeat(d[1], 1)
    g00 = gradients[:-d[0], :-d[1]]
    g10 = gradients[d[0]:, :-d[1]]
    g01 = gradients[:-d[0], d[1]:]
    g11 = gradients[d[0]:, d[1]:]
    # Ramps
    n00 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1])) * g00, 2)
    n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
    # Interpolation
    t = interpolant(grid)
    n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
    n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
    arr = np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)
    return [[fn(j) for j in i] for i in arr]




#GPT4写的
def is_within_bounds(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def bfs(start, end, grid):
    from collections import deque
    
    if grid[end[0]][end[1]].passability is None:
        return None
    
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if is_within_bounds(neighbor[0], neighbor[1], grid) and neighbor not in visited:
                if grid[neighbor[0]][neighbor[1]].passability is not None:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current
    
    return None

def dfs(start, end, grid):
    if grid[end[0]][end[1]].passability is None:
        return None
    
    stack = [start]
    visited = set()
    parent = {start: None}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while stack:
        current = stack.pop()
        
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        if current not in visited:
            visited.add(current)
            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if is_within_bounds(neighbor[0], neighbor[1], grid) and neighbor not in visited:
                    if grid[neighbor[0]][neighbor[1]].Pass is not None:
                        stack.append(neighbor)
                        parent[neighbor] = current
    
    return None
class CustomSVC:
    def __init__(self, C=1):
        self.C = C
        self.X_train = []
        self.y_train = []

    def fit(self, X, y, partial_train=False):
        if not partial_train:
            self.X_train = X
            self.y_train = y
        else:
            for new_sample, new_label in zip(X, y):
                replaced = False
                for i, existing_sample in enumerate(self.X_train):
                    if existing_sample == new_sample:
                        self.y_train[i] = new_label
                        replaced = True
                        break
                if not replaced:
                    self.X_train.append(new_sample)
                    self.y_train.append(new_label)

    def predict(self, X):
        y_pred = []
        for sample in X:
            dist = [np.linalg.norm(np.array(sample) - np.array(x)) for x in self.X_train]
            closest_index = np.argmin(dist)
            y_pred.append(self.y_train[closest_index])
        return y_pred