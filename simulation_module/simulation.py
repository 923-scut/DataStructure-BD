# simulation_module/simulation.py

import random
from typing import List, Dict


class Simulation:
    """
    仿真系统核心控制器
    你这个模块的唯一职责：
    👉 控制时间流动 + 调度 + 状态更新
    """

    def __init__(self, graph, vehicles, stations):
        self.graph = graph
        self.vehicles = vehicles
        self.stations = stations

        self.tasks = []          # 动态任务池
        self.time = 0

        # ===== 统计指标 =====
        self.total_reward = 0
        self.completed_tasks = 0

    # =========================
    # 🚀 主入口（必须实现）
    # =========================
    def run_simulation(self, T: int):
        """
        T: 仿真时间长度
        """

        for t in range(T):
            self.time = t

            # 1. 生成任务
            self._generate_tasks()

            # 2. 调度（未来 strategy module 会接入）
            assignments = self._assign_tasks_placeholder()

            # 3. 执行车辆移动
            self._move_vehicles()

            # 4. 检查任务完成
            self._check_tasks()

            # 5. 电量与充电（先预留）
            self._handle_energy()

        return self._get_stats()

    # =========================
    # 📦 任务生成（随机模拟）
    # =========================
    def _generate_tasks(self):
        """
        模拟任务随机出现
        """
        if random.random() < 0.4:   # 40%概率
            task = {
                "id": random.randint(1000, 9999),
                "location": random.randint(0, 20),
                "weight": random.uniform(1, 10),
                "release_time": self.time,
                "deadline": self.time + random.randint(5, 20),
                "completed": False
            }
            self.tasks.append(task)

    # =========================
    # 🧠 调度接口（预留给 strategy module）
    # =========================
    def _assign_tasks_placeholder(self):
        """
        ⚠️ 这里以后会接 strategy module
        现在只返回空
        """
        return []

    # =========================
    # 🚗 车辆移动逻辑（核心框架）
    # =========================
    def _move_vehicles(self):
        for v in self.vehicles:

            # 如果有路径就移动一步
            if hasattr(v, "path") and v.path:
                v.position = v.path.pop(0)

    # =========================
    # 📦 检查任务是否完成
    # =========================
    def _check_tasks(self):
        for task in self.tasks:

            if task["completed"]:
                continue

            for v in self.vehicles:
                if v.position == task["location"]:
                    task["completed"] = True
                    self.completed_tasks += 1

                    # 简单收益模型（后面可以升级）
                    reward = task["weight"] * 10
                    self.total_reward += reward

    # =========================
    # ⚡ 电量系统（先占位）
    # =========================
    def _handle_energy(self):
        """
        后面要扩展：
        - 电量不足 → 去充电站
        - 排队逻辑
        """
        pass

    # =========================
    # 📊 输出结果
    # =========================
    def _get_stats(self):
        return {
            "completed_tasks": self.completed_tasks,
            "total_reward": self.total_reward,
            "remaining_tasks": len(self.tasks) - self.completed_tasks
        }