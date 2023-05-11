import json
import math
import urllib
from datetime import datetime
from http.client import HTTPConnection
from typing import Type, Callable

from fastapi import HTTPException, Depends
from starlette import status

from fastapi_app.api.settings import custom_db_settings


class CustomDBWorker:
    def __init__(self, conn: HTTPConnection) -> None:
        self.conn = conn

    async def send_with_query(self, method: str = 'GET', url: str = '/Query', query_params: dict = None) -> dict:
        if query_params is None:
            self.conn.request(method, url)
        else:
            params = [f'{key}={urllib.parse.quote(value)}' for key, value in query_params.items()]
            query_params = '&'.join(params)
            self.conn.request(method, f'{url}?{query_params}')
        response = self.conn.getresponse()
        data = response.read().decode("utf-8")
        return json.loads(data)

    async def send_only_query(self, query: str):
        return await self.send_with_query(query_params={'query': query})

    @staticmethod
    def get_data_from_response(func):
        async def wrap(*args, **kwargs):
            result = (await func(*args, **kwargs))
            response = result.get("Ok")
            if response is not None or kwargs.get('safe'):
                return response
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"Error": result.get("Error")}
            )

        return wrap

    @get_data_from_response
    async def get_users_by_id(self, user_ids: list[int], safe: bool = False):
        user_ids_string = " or ".join([f'id = {user_id}' for user_id in user_ids])
        return await self.send_only_query(f'get [User] where {user_ids_string}')

    @get_data_from_response
    async def get_timers(self, timer_pointers: list[str]):
        timer_pointers_string = f"[{','.join(timer_pointers)}]"
        return await self.send_only_query(f'retrieve {timer_pointers_string}')

    async def get_timers_from_user(self, user):
        timers = user.get("timers")
        if timers is not None:
            return await self.get_timers(timers)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    async def get_timers_for_user(self, user_id: int):
        users = await self.get_users_by_id([user_id])
        if len(users) == 0:
            # The user is not registered in Custom-DB (they didn't create any timers yet)
            return []
        return await self.get_timers_from_user(users[0])

    async def get_timers_for_users(self, user_ids: list[int]):
        users = await self.get_users_by_id(user_ids)
        result = {}
        for user in users:
            result[user["id"]] = await self.get_timers_from_user(user)
        return result

    @get_data_from_response
    async def add_timer(self, timer: dict):
        query = f"add [Timer] [{json.dumps(timer)}]"
        return await self.send_only_query(query)

    async def remove_timer(self, pointer: str):
        query = f"remove [{pointer}]"
        return await self.send_only_query(query)

    @get_data_from_response
    async def update_user(self, user, timers: list[str]):
        new_dict_value = json.dumps({"id": int(user["id"]), "timers": timers})
        query = f'replace [{user["pointer"]}] [{new_dict_value}]'
        return await self.send_only_query(query)

    @get_data_from_response
    async def create_user(self, user_id, timers=list[str]):
        query = f'add [User] [{json.dumps({"id": user_id, "timers": timers})}]'
        return await self.send_only_query(query)

    async def add_timer_for_user(self,
                                 user_id: int,
                                 name: str,
                                 start_time: datetime,
                                 duration_seconds: int,
                                 active: bool = False
                                 ):
        timer = {
            "name": name,
            "start_time": str(start_time),
            "duration_seconds": duration_seconds,
            "time_left": duration_seconds,
            "active": active
        }
        user = (await self.get_users_by_id([user_id], safe=True))
        if not user:
            await self.create_user(user_id, [])
            user = (await self.get_users_by_id([user_id], safe=True))
        user = user[0]
        timers = await self.get_timers_from_user(user)
        timer_names = [timer["name"] for timer in timers]
        if timer["name"] in timer_names:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Timer already exists")
        timer_name = (await self.add_timer(timer))[0]
        timer_names = [timer["pointer"] for timer in timers] + [timer_name]
        update_user = await self.update_user(user, timer_names)
        if update_user != "Successful!":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    async def remove_timer_for_user(self, user_id: int, timer_name: str):
        user = (await self.get_users_by_id([user_id]))[0]
        timers = await self.get_timers_for_user(user_id)
        for timer in timers:
            if timer["name"] == timer_name:
                timer_to_delete = timer["pointer"]
                timer_names = [cur_timer["pointer"] for cur_timer
                               in timers if cur_timer["name"] != timer_name]
                await self.update_user(user, timer_names)
                await self.remove_timer(timer_to_delete)
                return {"detail": "Ok"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such timer in database")

    async def rename_timer_for_user(self, user_id: int, old_timer_name: str, new_timer_name: str):
        user = (await self.get_users_by_id([user_id]))[0]
        timers = await self.get_timers_for_user(user_id)
        for timer in timers:
            if timer["name"] == old_timer_name:
                timers = await self.get_timers_from_user(user)
                timer_names = [timer["name"] for timer in timers]
                if new_timer_name in timer_names:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Timer already exists")
                timer["name"] = new_timer_name
                timer_to_delete = timer["pointer"]
                timer.pop("pointer")
                new_timer = (await self.add_timer(timer))[0]
                timer_names = [cur_timer["pointer"] for cur_timer
                               in timers if cur_timer["name"] != old_timer_name] + [new_timer]
                await self.update_user(user, timer_names)
                await self.remove_timer(timer_to_delete)
                return new_timer
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such timer in database")

    @staticmethod
    def get_time_left(start_time: str, duration_seconds: int, time_left: int) -> int:
        start_time: datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        res = math.floor(min(duration_seconds, time_left) - (datetime.utcnow() - start_time).total_seconds())
        return res

    @staticmethod
    def get_time_now() -> str:
        return str(datetime.utcnow())

    async def stop_timer(self, user_id: int, timer_name: str):
        timers = await self.get_timers_for_user(user_id)
        for timer in timers:
            if timer["name"] == timer_name:
                time_left = self.get_time_left(timer["start_time"],
                                               timer["duration_seconds"],
                                               timer["time_left"])
                if not timer["active"] or time_left < 0:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Timer already stopped")
                timer["active"] = False
                timer_to_delete = timer["pointer"]
                timer["time_left"] = time_left
                timer.pop("pointer")
                new_timer = (await self.add_timer(timer))[0]
                timer_names = [cur_timer["pointer"] for cur_timer
                               in timers if cur_timer["name"] != timer_name] + [new_timer]
                user = (await self.get_users_by_id([user_id]))[0]
                await self.update_user(user, timer_names)
                await self.remove_timer(timer_to_delete)
                return new_timer
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such timer in database")

    async def resume_timer(self, user_id: int, timer_name: str):
        timers = await self.get_timers_for_user(user_id)
        for timer in timers:
            if timer["name"] == timer_name:
                if timer["active"]:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Timer is active")
                timer["start_time"] = self.get_time_now()
                timer["active"] = True
                timer_to_delete = timer["pointer"]
                timer.pop("pointer")
                new_timer = (await self.add_timer(timer))[0]
                timer_names = [cur_timer["pointer"] for cur_timer
                               in timers if cur_timer["name"] != timer_name] + [new_timer]
                user = (await self.get_users_by_id([user_id]))[0]
                await self.update_user(user, timer_names)
                await self.remove_timer(timer_to_delete)
                return new_timer
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such timer in database")

    async def reset_timer(self, user_id: int, timer_name: str):
        timers = await self.get_timers_for_user(user_id)
        for timer in timers:
            if timer["name"] == timer_name:
                timer_to_delete = timer["pointer"]
                timer["time_left"] = timer["duration_seconds"]
                timer["start_time"] = self.get_time_now()
                timer.pop("pointer")
                new_timer = (await self.add_timer(timer))[0]
                timer_names = [cur_timer["pointer"] for cur_timer
                               in timers if cur_timer["name"] != timer_name] + [new_timer]
                user = (await self.get_users_by_id([user_id]))[0]
                await self.update_user(user, timer_names)
                await self.remove_timer(timer_to_delete)
                return new_timer
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such timer in database")

    async def change_timer_duration(self, user_id: int, timer_name: str, new_duration: int):
        timers = await self.get_timers_for_user(user_id)
        for timer in timers:
            if timer["name"] == timer_name:
                timer_to_delete = timer["pointer"]
                timer["duration_seconds"] = new_duration
                timer["time_left"] = new_duration
                timer.pop("pointer")
                new_timer = (await self.add_timer(timer))[0]
                timer_names = [cur_timer["pointer"] for cur_timer
                               in timers if cur_timer["name"] != timer_name] + [new_timer]
                user = (await self.get_users_by_id([user_id]))[0]
                await self.update_user(user, timer_names)
                await self.remove_timer(timer_to_delete)
                return new_timer
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such timer in database")

    async def get_all_timers_for_user_pure(self, user_id):
        timers = await self.get_timers_for_user(user_id)
        pure_timers = []
        for timer in timers:
            timer.pop('pointer')
            pure_timers.append(timer)
        return timers

    async def create_table(self, model):
        model = model()
        fields = model.get_string_repr()
        query = f'create entity {model.table_name} {{{fields}}}'
        return await self.send_only_query(query)


def get_custom_db_worker(
        worker: Type[CustomDBWorker]
) -> Callable[[HTTPConnection], CustomDBWorker]:
    def _get_worker(
            conn: HTTPConnection = Depends(get_connection)
    ):
        return worker(conn)

    return _get_worker


def get_connection():
    yield HTTPConnection(custom_db_settings.custom_db_ip, int(custom_db_settings.custom_db_port))
