from motor.motor_asyncio import AsyncIOMotorClient
from isodate import parse_datetime, datetime_isoformat


class MongoDbApi:
    """Класс для работы с бд"""
    def __init__(
            self,
            url,
            db_name,
            collection_name,
    ):
        self._url = url
        self._client = AsyncIOMotorClient(self._url)
        self._db_name = db_name
        self._collection = collection_name

    def _get_collection(self):
        """Получение коллекции"""
        return self._client[self._db_name][self._collection]

    async def get_data_from_db(
            self,
            start_date: str,
            end_date: str,
            group_type: str,
    ):
        """Получение данных из бд"""
        collection = self._get_collection()
        data = {}
        match group_type:
            case 'month':
                stmt = {'$month': '$dt'}
            case 'day':
                stmt = {'$dayOfYear': '$dt'}
            case 'hour':
                stmt = {'$hour': '$dt'}
            case _:
                raise ValueError('invalid group type')

        pipeline = [
            {
                '$match': {
                    'dt': {
                        '$gte': parse_datetime(start_date),
                        '$lte': parse_datetime(end_date)
                    }
                }
            },
            {
                '$group': {
                    '_id': stmt,
                    'total': {'$sum': '$value'},
                    'date': {'$first': '$dt'}
                },
            },
            {
                '$sort': {'_id': 1},
            },
            {
                '$project': {
                    'total': 1,
                    'date': {
                        '$dateTrunc': {
                            'date': '$date', 'unit': group_type
                        }
                    },
                    '_id': 0,
                }
            }
        ]

        cursor = collection.aggregate(pipeline)

        async for item in cursor:
            data[datetime_isoformat(item['date'])] = item['total']
        return data
