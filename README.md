````markdown
# 🚛 New Energy Logistics Scheduling Simulator

## 1. Overview

本项目实现一个**新能源物流调度仿真系统（Discrete Event Simulation）**，用于研究：

- 多车辆任务调度策略
- 路径规划与能耗约束
- 充电行为对系统效率的影响

系统支持策略对比、指标评估与扩展实验。

---

## 2. System Architecture

系统采用**模块化分层架构**：

```text
simulation-module   # 仿真核心（唯一调度入口）
│
├── strategy-module # 调度策略（可扩展）
├── map-module      # 地图与路径计算
└── model-module    # 数据模型（统一定义）
````

### Design Principles

* **单一职责（SRP）**：每个模块仅负责一类问题
* **接口隔离（API Contract）**：模块通过固定接口交互
* **可扩展性优先**：策略、地图、任务生成均可替换
* **仿真驱动（Simulation-driven）**：所有行为由 simulation 控制

---

## 3. Simulation Workflow

系统按离散时间推进：

```text
Task Generation
      ↓
Task Assignment (Strategy)
      ↓
Path Planning (Graph)
      ↓
Vehicle Movement
      ↓
Battery Consumption
      ↓
Charging Decision
      ↓
Task Completion
      ↓
Statistics Update
```

---

## 4. Module Specification

---

## 4.1 map-module

### Responsibility

* 构建道路网络（Graph）
* 提供最短路径与距离查询

### Data Structure

```python
graph: Dict[int, List[Tuple[int, float]]]
```

### API Contract

```python
def get_distance(graph, start: int, end: int) -> float:
    """Return shortest distance between two nodes."""
```

```python
def get_path(graph, start: int, end: int) -> List[int]:
    """Return shortest path as node sequence."""
```

### Implementation Notes

* 推荐算法：Dijkstra / A*
* 要求：无副作用（pure function）

---

## 4.2 model-module

### Responsibility

定义系统核心实体（**唯一数据源**）

### Entities

#### Vehicle

```python
class Vehicle:
    id: int
    position: int
    battery: float
    max_battery: float
    capacity: float
    status: str        # idle | busy | charging
    task: Optional["Task"]
    path: List[int]
```

#### Task

```python
class Task:
    id: int
    location: int
    weight: float
    release_time: int
    deadline: int
    completed: bool
    assigned: bool
```

#### Station

```python
class Station:
    id: int
    location: int
    queue: List[int]
```

---

## 4.3 strategy-module

### Responsibility

实现任务分配策略（核心可扩展点）

### API Contract (STRICT)

```python
def assign_tasks(
    vehicles: List[Vehicle],
    tasks: List[Task],
    graph
) -> List[Tuple[Vehicle, Task]]:
    """
    Return assignment pairs (vehicle, task)
    Must NOT mutate input objects directly.
    """
```

### Built-in Strategies

#### 1. Nearest Task First

* 基于最短距离
* Greedy

#### 2. Largest Task First

* 按 weight 排序
* 优先处理高价值任务

### Extension Guideline

新增策略需：

* 实现同名函数
* 不修改已有接口
* 可被 simulation 动态切换

---

## 4.4 simulation-module

### Responsibility

系统唯一调度入口，负责：

* 时间推进
* 状态更新
* 模块调用协调

---

### Core API

```python
def run_simulation(graph, vehicles, stations, T: int) -> Dict:
    """
    Run simulation for T time steps.

    Returns:
        stats: {
            total_tasks,
            completed_tasks,
            avg_completion_time,
            total_reward
        }
    """
```

---

### Execution Loop

```python
for time in range(T):

    tasks += generate_tasks(time)

    assignments = assign_tasks(vehicles, tasks, graph)

    update_vehicle_tasks(assignments)

    for vehicle in vehicles:
        move_vehicle(vehicle, graph)
        update_battery(vehicle)
        check_and_charge(vehicle, stations, graph)
        try_finish_task(vehicle, time)

    record_metrics()
```

---

### Suggested Internal APIs

```python
def generate_tasks(time) -> List[Task]
```

```python
def move_vehicle(vehicle, graph)
```

```python
def update_battery(vehicle)
```

```python
def check_and_charge(vehicle, stations, graph)
```

```python
def calculate_reward(task, finish_time) -> float
```

---

## 5. Vehicle State Machine

```text
        +--------+
        | idle   |
        +--------+
            |
            v
        +--------+
        | busy   |
        +--------+
            |
   battery low?
        /    \
      yes     no
      v        v
+-----------+  |
| charging  |<-+
+-----------+
```

---

## 6. Metrics Definition

| Metric              | Description |
| ------------------- | ----------- |
| total_tasks         | 生成任务总数      |
| completed_tasks     | 完成任务数       |
| avg_completion_time | 平均完成耗时      |
| total_reward        | 总收益         |

---

## 7. Global Constraints (MUST FOLLOW)

### 1. Node Representation

```text
All positions MUST use node_id
(x, y) is NOT allowed
```

---

### 2. Data Model Consistency

```text
All modules MUST import model-module
DO NOT redefine Vehicle / Task
```

---

### 3. Interface Consistency

```text
get_distance
get_path
assign_tasks
run_simulation
```

---

### 4. Control Ownership

```text
ONLY simulation-module can drive execution
```

---

## 8. Environment Setup

### 8.1 Python Version

```text
Python == 3.12.3
```

---

### 8.2 Create Virtual Environment

```bash
python3.12 -m venv .venv
```

激活环境：

```bash
# Linux / Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

---

### 8.3 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 8.4 Verify Environment

```bash
python --version
```

期望输出：

```text
Python 3.12.3
```

---

## 9. Project Structure

```text
project-root/
│
├── map-module/
├── model-module/
├── strategy-module/
├── simulation-module/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
```

---

## 10. How to Run

```bash
python main.py
```

或：

```python
stats = run_simulation(graph, vehicles, stations, T=1000)
print(stats)
```

---

## 11. Extensibility

可扩展方向：

* 新调度策略（RL / heuristic / auction）
* 多充电站策略
* 动态电价模型
* 不同地图结构（grid / real map）
* 多任务组合（pickup & delivery）

---

## 12. Project Goal

通过统一建模 + 策略对比，分析：

* 调度策略对效率的影响
* 电量约束下的系统行为
* 路径与调度的耦合关系

---

## 13. Summary

```text
This project models a logistics system using graph-based routing and strategy-driven scheduling, enabling simulation and evaluation of electric vehicle fleet operations.
```

```
```
