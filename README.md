# DataStructure-BD
华南理工大学大数据24数据结构大作业
很好，这一步就是**项目成败关键：统一接口规范** 👍
我帮你整理一份**可以直接放 README 的标准版（模块职责 + 数据结构 + 接口定义）**

👉 你可以原样发给组员使用

---

# 📦 项目模块划分与接口规范（README版）

---

# 🧠 一、整体说明

本项目实现一个**新能源物流调度仿真系统**，系统由四个模块组成：

```text
map-module        （地图与路径）
model-module      （数据结构定义）
strategy-module   （调度策略）
simulation-module （仿真系统）
```

系统运行流程：

```text
生成任务 → 调度策略分配 → 路径规划 → 车辆移动 → 电量判断 → 充电 → 完成任务 → 统计结果
```

---

# 🗺️ 二、map-module（地图模块）

## 📌 职责

* 构建道路图（Graph）
* 提供最短路径与距离计算

---

## 🧠 数据结构

```python
graph: Dict[node_id, List[(neighbor_id, distance)]]
```

---

## 🔌 对外接口（必须统一）

```python
def get_distance(graph, start, end) -> float:
    """
    输入：
        graph: 图结构
        start: 起点 node_id
        end: 终点 node_id
    输出：
        最短距离（float）
    """
```

---

```python
def get_path(graph, start, end) -> List[int]:
    """
    输入：
        graph: 图结构
        start: 起点 node_id
        end: 终点 node_id
    输出：
        路径（node_id 列表）
    """
```

---

# 🧱 三、model-module（建模模块）

## 📌 职责

* 定义系统中所有数据结构（Vehicle / Task / Station）

---

## 🧠 数据结构

### Vehicle

```python
class Vehicle:
    id: int
    position: int          # 当前节点
    battery: float         # 当前电量
    max_battery: float
    capacity: float        # 载重上限
    status: str            # idle / busy / charging
    task: Task | None
    path: List[int]
```

---

### Task

```python
class Task:
    id: int
    location: int          # node_id
    weight: float
    release_time: int
    deadline: int
    completed: bool
    assigned: bool
```

---

### Station

```python
class Station:
    id: int
    location: int
    queue: List[int]       # vehicle_id 队列
```

---

## 🔌 对外接口

👉 无函数接口（仅提供类定义）

---

# 🧠 四、strategy-module（调度模块）

## 📌 职责

* 决定“哪辆车执行哪个任务”
* 实现至少两种策略

---

## 🧠 数据结构

* vehicles: List[Vehicle]
* tasks: List[Task]

---

## 🔌 对外接口（必须统一🔥）

```python
def assign_tasks(vehicles, tasks, graph) -> List[tuple]:
    """
    输入：
        vehicles: 所有车辆列表
        tasks: 所有未完成任务
        graph: 地图

    输出：
        assignments: List[(vehicle, task)]

    说明：
        返回需要分配的 (车, 任务) 对
    """
```

---

## 📌 策略实现要求

至少实现：

```text
1. 最近任务优先
2. 最大任务优先
```

---

# ⚙️ 五、simulation-module（仿真模块）

## 📌 职责

* 控制系统运行（核心模块）
* 调用 map / strategy / model

---

## 🧠 数据结构

* vehicles: List[Vehicle]
* tasks: List[Task]
* stations: List[Station]
* graph

---

## 🔌 对外接口

```python
def run_simulation(graph, vehicles, stations, T: int):
    """
    输入：
        graph: 地图
        vehicles: 车辆列表
        stations: 充电站列表
        T: 仿真总时间

    输出：
        stats: Dict
    """
```

---

## 📌 内部流程（必须实现）

```text
for time in range(T):

    1. 生成新任务
    2. 调用 assign_tasks 分配任务
    3. 调用 get_path 获取路径
    4. 更新车辆位置（逐步移动）
    5. 更新电量
    6. 判断是否需要充电
    7. 处理充电逻辑
    8. 完成任务
    9. 记录数据
```

---

## 🔌 内部辅助接口（建议实现）

```python
def generate_tasks(time) -> List[Task]
```

---

```python
def move_vehicle(vehicle, graph)
```

---

```python
def check_and_charge(vehicle, stations, graph)
```

---

```python
def calculate_reward(task, finish_time) -> float
```

---

# 🔄 六、模块调用关系（统一规范）

```text
simulation-module（核心）
    ↓
    ├── strategy-module → assign_tasks()
    ├── map-module → get_distance() / get_path()
    └── model-module → 数据结构
```

---

# ⚠️ 七、强制统一规则（必须遵守）

---

## ❗ 1. 所有位置统一用 node_id

```text
禁止使用 (x, y)
必须使用 node_id
```

---

## ❗ 2. 所有模块使用同一数据结构

```text
必须 import model-module
禁止重复定义 Vehicle / Task
```

---

## ❗ 3. 接口函数名必须一致

```text
get_distance
get_path
assign_tasks
run_simulation
```

---

## ❗ 4. simulation 是唯一主控模块

```text
其他模块不能自己运行系统
```

---

# 🎯 八、最终目标

系统运行输出：

```text
总任务数
完成任务数
平均完成时间
总收益
```

并对比不同策略效果。

---

# 🧠 最后一行总结（README结尾建议写）

```text
本项目通过图结构建模道路网络，结合调度策略与仿真系统，实现新能源物流车队的动态调度与路径规划。
```

---

# 🚀 如果你下一步继续推进

我可以帮你：

👉 把这份 README 转成 **项目目录结构 + 代码模板（直接开写）**
👉 或帮你写一个 **最小可运行 demo（你们直接在上面扩展）**