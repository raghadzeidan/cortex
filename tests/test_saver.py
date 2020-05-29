import pytest
import pymongo
from cortex.saver import DatabaseDriver

PORT=27017
HOST="127.0.0.1"
MOCK_ID = "mockID"
mock = {'_id': MOCK_ID, #mockID
		'user_info': {'userId': MOCK_ID, 'username': 'Dan Gittik', 'birthday': '1970-01-09 04:22:26.400000', 'gender': 'm'},
		'snapshots': [
		{'datetime': '2019-12-04 10:08:07.339000',
		 'snapshotId': f'{MOCK_ID}_2019-12-04 10:08:07.339000',
		  'pose': {'translation': {'x': 0.4873843491077423, 'y': 0.007090016733855009, 'z': -1.1306129693984985}, 'rotation': {'x': -0.10888676356214629, 'y': -0.26755994585035286, 'z': -0.021271118915446748, 'w': 0.9571326384559261}},
		   'feelings': {},
		    'depth_image': '/home/user/Desktop/volume/depth_images/images/42_2019-12-04 10:08:07.339000.png',
		     'color_image': '/home/user/Desktop/volume/color_images/images/42_2019-12-04 10:08:07.339000.png'}]}

EXPECTED_USER_INFO = {'userId': MOCK_ID, 'username': 'Dan Gittik', 'birthday': '1970-01-09 04:22:26.400000', 'gender': 'm'}
EXPECTED_SNAPSHOTS_LIST = [{'datetime': '2019-12-04 10:08:07.339000', 'snapshotId': 'mockID_2019-12-04 10:08:07.339000', 'pose': {'translation': {'x': 0.4873843491077423, 'y': 0.007090016733855009, 'z': -1.1306129693984985}, 'rotation': {'x': -0.10888676356214629, 'y': -0.26755994585035286, 'z': -0.021271118915446748, 'w': 0.9571326384559261}}, 'feelings': {}, 'depth_image': '/home/user/Desktop/volume/depth_images/images/42_2019-12-04 10:08:07.339000.png', 'color_image': '/home/user/Desktop/volume/color_images/images/42_2019-12-04 10:08:07.339000.png'}]
EXPECTED_SNAPSHOTS_FEELINGS_POSE = [{'pose': {'translation': {'x': 0.4873843491077423, 'y': 0.007090016733855009, 'z': -1.1306129693984985}, 'rotation': {'x': -0.10888676356214629, 'y': -0.26755994585035286, 'z': -0.021271118915446748, 'w': 0.9571326384559261}}, 'feelings': {}}]
EXPECTED_SNAPSHOTS_COLOR_POSE = [{'pose': {'translation': {'x': 0.4873843491077423, 'y': 0.007090016733855009, 'z': -1.1306129693984985}, 'rotation': {'x': -0.10888676356214629, 'y': -0.26755994585035286, 'z': -0.021271118915446748, 'w': 0.9571326384559261}}, 'color_image': '/home/user/Desktop/volume/color_images/images/42_2019-12-04 10:08:07.339000.png'}]
SNAPSHOT_MOCK_ID = f'{MOCK_ID}_2019-12-04 10:08:07.339000'

EXPECTED_SNAPSHOT_RESULTS = {'datetime': '2019-12-04 10:08:07.339000', 'snapshotId': 'mockID_2019-12-04 10:08:07.339000', 'results': ['pose', 'depth_image', 'color_image']}
@pytest.fixture
def mongo_driver():
	driver = DatabaseDriver(f"mongodb://{HOST}:{PORT}")
	driver.debug_save(mock)
	try:
		yield driver
	finally:
		#don't want to garbage our db
		driver.debug_delete_id(MOCK_ID)
	
def test_saver_user_info(mongo_driver):
	result = mongo_driver.load_user_info(MOCK_ID)
	assert result==EXPECTED_USER_INFO
	#collection = db.test_coll
	#test_coll.insert({'foo': 'bar'})
	#assert test_coll.find_one()['foo'] == 'bar'
	
def test_saver_users(mongo_driver):
	users = mongo_driver.load_users()
	ids = [user['userId'] for user in users]
	assert (MOCK_ID in ids)
	
@pytest.mark.parametrize("f,p,c,d,expected",[(0,0,0,0,EXPECTED_SNAPSHOTS_LIST),(1,1,0,0,EXPECTED_SNAPSHOTS_FEELINGS_POSE), (0,1,1,0,EXPECTED_SNAPSHOTS_COLOR_POSE)])
def test_load_user_snapshots_list(mongo_driver,f,p,c,d,expected):
	result = mongo_driver.load_user_snapshots_list(MOCK_ID, feelings=f, pose=p, color_image=c, depth_image=d)
	assert result == expected
	
def test_snapshot(mongo_driver):
	result = mongo_driver.load_user_snapshot_results(MOCK_ID, SNAPSHOT_MOCK_ID)
	print('z',result,'z')
	assert result== EXPECTED_SNAPSHOT_RESULTS
