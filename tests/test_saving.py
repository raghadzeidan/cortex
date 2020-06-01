import pytest
from cortex.common import DatabaseDriver, MongoDriver
import json
import pathlib
from pymongo import MongoClient

MOCK_ID = "mockID"
mock = {'_id': MOCK_ID, 'user': {'userId': MOCK_ID, 'username': 'Dan Gittik', 'birthday': '1970-01-09 04:22:26.400000', 'gender': 'm'}, 'datetime': '2019-12-04 10:08:07.339000', 'snapshotId': f'{MOCK_ID}_2019-12-04 10:08:07.339000', 'feelings': {'happiness':0.5,'exhaustion':0.4, 'thirst':0.3,'hunger':0.2}}


def test_save(mongodb, monkeypatch):
   
    def mockinit(self, host,port):
        self.db = mongodb['cortex-db']
        self.users = self.db.users
    monkeypatch.setattr(MongoDriver, '__init__', mockinit)    
    saver = DatabaseDriver('mongodb://localhost:27017')
    saver.save('feelings', json.dumps(mock))
    snapshot = saver.db_driver.users.find_one({'_id': MOCK_ID})
    print(snapshot)
    assert snapshot is not None
    assert snapshot['snapshots'] is not None
    assert snapshot['snapshots'][0]['feelings'] is not None
    assert snapshot['snapshots'][0]['feelings']['happiness'] == 0.5
    assert snapshot['snapshots'][0]['feelings']['thirst'] == 0.3


def test_saver_error():
    with pytest.raises(Exception):
        saver = Saver('bad://localhost:27017')
