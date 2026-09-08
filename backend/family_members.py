from dataclasses import dataclass, asdict
from datetime import date
from typing import Dict, List, Optional

ALLOWED_RELATIONS = {"本人", "父亲", "母亲", "配偶", "子女", "其他"}
ALLOWED_GENDERS = {"男", "女", "未知"}

@dataclass
class FamilyMember:
    member_id: int
    user_id: int
    name: str
    relation: str
    gender: str = "未知"
    birth_date: Optional[str] = None

class FamilyMemberService:
    """Sprint 1：家庭成员管理的最小可用业务服务。"""

    def __init__(self):
        self._members: Dict[int, FamilyMember] = {}
        self._next_id = 1

    def add_member(
        self,
        user_id: int,
        name: str,
        relation: str,
        gender: str = "未知",
        birth_date: Optional[str] = None,
    ) -> dict:
        self._validate(user_id, name, relation, gender, birth_date)

        # 同一主账号下，不允许出现“同姓名 + 同关系”的重复档案。
        duplicate = any(
            m.user_id == user_id
            and m.name.strip() == name.strip()
            and m.relation == relation
            for m in self._members.values()
        )
        if duplicate:
            raise ValueError("家庭成员档案重复")

        member = FamilyMember(
            member_id=self._next_id,
            user_id=user_id,
            name=name.strip(),
            relation=relation,
            gender=gender,
            birth_date=birth_date,
        )
        self._members[self._next_id] = member
        self._next_id += 1
        return asdict(member)

    def list_members(self, user_id: int) -> List[dict]:
        return [
            asdict(m)
            for m in self._members.values()
            if m.user_id == user_id
        ]

    def update_member(self, user_id: int, member_id: int, **changes) -> dict:
        member = self._members.get(member_id)
        if not member or member.user_id != user_id:
            raise KeyError("家庭成员不存在或无权访问")

        name = changes.get("name", member.name)
        relation = changes.get("relation", member.relation)
        gender = changes.get("gender", member.gender)
        birth_date = changes.get("birth_date", member.birth_date)
        self._validate(user_id, name, relation, gender, birth_date)

        member.name = name.strip()
        member.relation = relation
        member.gender = gender
        member.birth_date = birth_date
        return asdict(member)

    def remove_member(self, user_id: int, member_id: int) -> None:
        member = self._members.get(member_id)
        if not member or member.user_id != user_id:
            raise KeyError("家庭成员不存在或无权访问")
        del self._members[member_id]

    @staticmethod
    def _validate(
        user_id: int,
        name: str,
        relation: str,
        gender: str,
        birth_date: Optional[str],
    ) -> None:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id 必须为正整数")
        if not name or len(name.strip()) > 50:
            raise ValueError("成员姓名不能为空且长度不能超过50")
        if relation not in ALLOWED_RELATIONS:
            raise ValueError("非法关系类型")
        if gender not in ALLOWED_GENDERS:
            raise ValueError("非法性别值")
        if birth_date:
            try:
                parsed = date.fromisoformat(birth_date)
            except ValueError as exc:
                raise ValueError("birth_date 必须为 YYYY-MM-DD") from exc
            if parsed > date.today():
                raise ValueError("出生日期不能晚于今天")
