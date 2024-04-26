import asyncio

from isodate import parse_datetime, datetime_isoformat
from dateutil.relativedelta import relativedelta

from statistic.mongoAPI import MongoDbApi
from variables import MONGO_URL


class Statistic:
    """Класс для получения данных после обработки"""
    def __init__(
            self,
            start_date,
            end_date,
            group_type
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.group_type = group_type
        self.client = MongoDbApi(
            url=MONGO_URL,
            db_name='sampleDB',
            collection_name='sample_collection'
        )

    def _get_range_of_date(self):
        """Генератор возвращающий дату для проверки ее наличия в данных из базы"""
        start = parse_datetime(self.start_date)
        end = parse_datetime(self.end_date)

        match self.group_type:
            case 'month':
                diff = relativedelta(months=1)
            case 'day':
                diff = relativedelta(days=1)
            case 'hour':
                diff = relativedelta(hours=1)
            case _:
                raise ValueError('invalid step')

        while start <= end:
            yield datetime_isoformat(start)
            start += diff

    async def get_statistic(self):
        """Получение подготовленных данных"""
        data = await self.client.get_data_from_db(
            start_date=self.start_date,
            end_date=self.end_date,
            group_type=self.group_type
        )
        result = {
            'dataset': [],
            'labels': []
        }

        for date in self._get_range_of_date():
            if date in data:
                result['dataset'].append(data[date])
                result['labels'].append(date)
            else:
                result['dataset'].append(0)
                result['labels'].append(date)

        return result


if __name__ == '__main__':
    test_queries = [
        {
            "dt_from": "2022-09-01T00:00:00",
            "dt_upto": "2022-12-31T23:59:00",
            "group_type": "month"
        },
        {
            "dt_from": "2022-10-01T00:00:00",
            "dt_upto": "2022-11-30T23:59:00",
            "group_type": "day"
        },
        {
            "dt_from": "2022-02-01T00:00:00",
            "dt_upto": "2022-02-02T00:00:00",
            "group_type": "hour"
        }
    ]
    statistic = Statistic(
        start_date=test_queries[2]['dt_from'],
        end_date=test_queries[2]['dt_upto'],
        group_type=test_queries[2]['group_type']
    )
    loop = asyncio.new_event_loop()
    print(loop.run_until_complete(statistic.get_statistic()))
