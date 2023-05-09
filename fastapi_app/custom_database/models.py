from typing import Optional

from pydantic import BaseModel

from fastapi_app.custom_database.utils import get_custom_db_worker, CustomDBWorker, get_connection


class CustomBaseModel(BaseModel):
    priority: int = 0
    string_repr: str = ''
    table_name: str = 'Base'

    @staticmethod
    def get_all_subclasses(cls):
        all_subclasses = []
        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(subclass.get_all_subclasses(subclass))
        return all_subclasses

    @staticmethod
    async def create_all():
        worker = get_custom_db_worker(CustomDBWorker)(next(get_connection()))
        all_subclasses = CustomBaseModel.__subclasses__()
        all_subclasses.sort(key=lambda x: x().priority)
        for subclass in all_subclasses:
            await worker.create_table(subclass)

    def get_string_repr(self):
        return self.string_repr


class TimerCustom(CustomBaseModel):
    priority: int = 1
    string_repr: str = 'name: string, start_time: string, duration_seconds: int, time_left: int, active: bool'
    table_name: str = 'Timer'

    name: Optional[str]
    start_time: Optional[str]
    duration_seconds: Optional[int]
    time_left: Optional[int]
    active: Optional[bool]


class UserCustom(CustomBaseModel):
    priority: int = 2
    string_repr: str = 'id: int(unique), timers: [%26Timer]'
    table_name: str = 'User'

    id: Optional[int]
    timers: Optional[TimerCustom]
