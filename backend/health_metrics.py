from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional

METRIC_RULES = {
    "收缩压": {"unit": "mmHg", "min": 50, "max": 260},
    "舒张压": {"unit": "mmHg", "min": 30, "max": 160},
    "血糖": {"unit": "mmol/L", "min": 1.0, "max": 40.0},
    "心率": {"unit": "bpm", "min": 20, "max": 250},
    "体重": {"unit": "kg", "min": 2.0, "max": 400.0},
}

@dataclass
class HealthMetric:
    metric_id: int
    member_id: int
    metric_type: str
    value: float
    unit: str
    measured_at: str
    abnormal: bool

class HealthMetricService:
    """Sprint 1：健康指标手工录入与基础异常标记。"""

    def __init__(self):
        self._metrics: Dict[int, HealthMetric] = {}
        self._next_id = 1

    def add_metric(
        self,
        member_id: int,
        metric_type: str,
        value: float,
        measured_at: Optional[str] = None,
    ) -> dict:
        if not isinstance(member_id, int) or member_id <= 0:
            raise ValueError("member_id 必须为正整数")
        if metric_type not in METRIC_RULES:
            raise ValueError("暂不支持该指标类型")

        rule = METRIC_RULES[metric_type]
        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("指标值必须为数字") from exc

        if not rule["min"] <= numeric_value <= rule["max"]:
            raise ValueError("指标值超出可接受录入范围")

        if measured_at:
            try:
                measured = datetime.fromisoformat(measured_at)
            except ValueError as exc:
                raise ValueError("measured_at 必须为 ISO 日期时间") from exc
        else:
            measured = datetime.now()

        abnormal = self._is_abnormal(metric_type, numeric_value)
        metric = HealthMetric(
            metric_id=self._next_id,
            member_id=member_id,
            metric_type=metric_type,
            value=numeric_value,
            unit=rule["unit"],
            measured_at=measured.isoformat(timespec="seconds"),
            abnormal=abnormal,
        )
        self._metrics[self._next_id] = metric
        self._next_id += 1
        return asdict(metric)

    def list_metrics(
        self,
        member_id: int,
        metric_type: Optional[str] = None,
    ) -> List[dict]:
        result = [
            m for m in self._metrics.values()
            if m.member_id == member_id
            and (metric_type is None or m.metric_type == metric_type)
        ]
        result.sort(key=lambda m: m.measured_at)
        return [asdict(m) for m in result]

    @staticmethod
    def _is_abnormal(metric_type: str, value: float) -> bool:
        # 仅用于课堂原型的基础提示阈值，不代表医学诊断标准。
        thresholds = {
            "收缩压": (90, 140),
            "舒张压": (60, 90),
            "血糖": (3.9, 7.8),
            "心率": (60, 100),
            "体重": (2.0, 400.0),
        }
        low, high = thresholds[metric_type]
        return value < low or value > high
