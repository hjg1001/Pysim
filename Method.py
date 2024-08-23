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
    
    if not grid[end[0]][end[1]].Pass:
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
                if grid[neighbor[0]][neighbor[1]].Pass:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current
    return None

def dfs(start, end, grid):
    if grid[end[0]][end[1]].Pass is None:
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
from collections import deque

def search_tile(map, search_type,type2,search_value,radius, start_x, start_y):
    rows = len(map)
    cols = len(map[0]) if rows > 0 else 0

    # 定义 BFS 搜索的四个方向（上下左右）
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 辅助函数：检查坐标是否在地图范围内
    def is_within_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols

    # BFS 队列，存储当前点及其距离
    queue = deque([(start_x, start_y, 0)])
    visited = set()
    visited.add((start_x, start_y))

    while queue:
        x, y, dist = queue.popleft()

        # 检查当前地块是否符合目标属性
        if type2:
        	if getattr(map[x][y],search_type) and getattr(getattr(map[x][y],search_type),type2) == search_value:
          	  return (x, y)
        else:
      	  if getattr(map[x][y],search_type) == search_value:
          	  return (x, y)

        # 如果超出半径范围，跳过该点
        if dist >= radius:
            continue

        # 遍历四个方向，添加到队列中
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_within_bounds(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))

    # 如果未找到符合条件的地块，返回 None
    return None