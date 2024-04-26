import json
from json import JSONDecodeError

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from statistic.main import Statistic


router = Router()


def get_exception_message(query: list[dict]):
    f, s, t = query
    return f'Допустимо отправлять только следующие запросы: \n{json.dumps(f)}\n{json.dumps(s)}\n{json.dumps(t)}'


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    await message.answer(
        f'Hi [{username}](tg://user?id={str(user_id)})!', parse_mode='Markdown'
    )


@router.message()
async def get_result(message: Message):
    valid_query = [
        {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"},
        {"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", "group_type": "day"},
        {"dt_from": "2022-02-01T00:00:00", "dt_upto": "2022-02-02T00:00:00", "group_type": "hour"}
    ]
    try:
        data = json.loads(message.text)
        if data in valid_query:
            statistic = Statistic(
                start_date=data['dt_from'],
                end_date=data['dt_upto'],
                group_type=data['group_type'],
            )
            result = await statistic.get_statistic()
            await message.answer(json.dumps(result))
        else:
            await message.answer(get_exception_message(valid_query))

    except JSONDecodeError:
        await message.answer(
            f'Невалидный запрос. Пример запроса:\n{json.dumps(valid_query[0])}'
        )
