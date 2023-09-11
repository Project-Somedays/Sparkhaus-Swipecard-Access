from dataclasses import dataclass
from datetime import datetime
import json
from enum import Enum


class InductionAttendanceFieldNames(Enum):
    RECORD_ID = "Record ID"
    INDUCTION_ID = "Induction ID"
    MEMBER = "Member"
    EQUIPMENT = "Inducted to Use"
    DATE_ATTENDED = "Date Attended"
    PRESENTER = "Inducted By"


class InductionSessionFieldNames(Enum):
    ID = "ID"
    START = "Start"
    END = "End"
    EQUIPMENT = "Equipment"
    PRESENTER = "Presenter"


@dataclass
class InductionSession:
    id: str
    start: datetime
    end: datetime
    equipment: str
    presenter: str

    def __repr__(self) -> str:
        return (
            f"{self.equipment} induction run by {self.presenter} on {self.start.date()}"
        )


@dataclass
class InductionAttendance:
    id: str
    induction_session_id: str
    induction_date: datetime
    presenter: str
    equipment: str
    member_id: str

    def __repr__(self) -> str:
        return f"{self.member_id} inducted to use {self.equipment} by {self.presenter} on {self.induction_date}"

    @property
    def is_in_date(self) -> bool:
        return datetime.today() - self.induction_date <= 365


def construct_induction_session(record: dict[str, str]) -> InductionSession:
    return InductionSession(
        id=record[InductionSessionFieldNames.ID.value],
        start=datetime.strptime(
            record[InductionSessionFieldNames.START.value], "%d/%m/%Y %H:%M:%S"
        ),
        end=datetime.strptime(
            record[InductionSessionFieldNames.END.value], "%d/%m/%Y %H:%M:%S"
        ),
        equipment=record[InductionSessionFieldNames.EQUIPMENT.value],
        presenter=record[InductionSessionFieldNames.PRESENTER.value],
    )


def construct_induction_attendance(record: dict[str, str]) -> InductionAttendance:
    return InductionAttendance(
        id=record[InductionAttendanceFieldNames.RECORD_ID.value],
        induction_session_id=record[InductionAttendanceFieldNames.INDUCTION_ID.value],
        induction_date=record[InductionAttendanceFieldNames.DATE_ATTENDED.value],
        equipment=record[InductionAttendanceFieldNames.EQUIPMENT.value],
        member_id=record[InductionAttendanceFieldNames.MEMBER.value],
        presenter=record[InductionAttendanceFieldNames.PRESENTER.value],
    )


def construct_list_from_column(
    records: list[dict[str, str]], column_name: str
) -> list[str]:
    return [record[column_name] for record in records]


def convert_records_to_induction_sessions(
    records: list[dict[str]],
) -> list[InductionSession]:
    return [construct_induction_session(record) for record in records]


def convert_records_to_induction_attendances(
    records: list[dict[str]],
) -> list[InductionAttendance]:
    return [construct_induction_attendance(record) for record in records]


def construct_induction_register_by_equipment(
    equipment_list: list[str], attendance_records: list[InductionAttendance]
) -> dict[str, list[dict[str, str | datetime]]]:
    equipment_register = {}
    for equipment in equipment_list:
        equipment_register[equipment] = [
            {record.member_id: record.induction_date}
            for record in attendance_records
            if record.equipment == equipment
        ]
    return equipment_register


def save_to_json(data_dict: dict, fn: str) -> None:
    with open(file=fn, mode="w", encoding="utf-8") as fh:
        json.dump(data_dict, fh, indent=2)


def save_all_to_json(to_save: dict[str, dict]) -> None:
    for fn, data in to_save.items():
        save_to_json(data_dict=data, fn=fn)
