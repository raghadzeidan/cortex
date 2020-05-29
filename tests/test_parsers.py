import pytest
import json
from cortex.parsers import run_parser

MOCK = b'{"user": {"userId": "42", "username": "Dan Gittik", "birthday": "1970-01-09 04:22:26.400000", "gender": "m"}, "datetime": "2019-12-04 10:08:07.412000", "feelings": {"hunger": 0.001, "thirst": 0.003, "exhaustion": 0.002}, "color_image": {"width": 1920, "height": 1080, "data_path": "/home/user/Desktop/volume/color_images/bytes/42_1575446887412"}, "pose": {"translation": {"x": 0.15600797533988953, "y": 0.08133671432733536, "z": -0.49068963527679443}, "rotation": {"x": -0.2959017411322204, "y": -0.16749024140672616, "z": -0.04752900380336424, "w": 0.9392178514199446}}, "depth_image": {"width": 224, "height": 172, "data_path": "/home/user/Desktop/volume/depth_images/bytes/42_1575446887412.npy"}}'

POSE_EXPECTED = {"user": {"userId": "42", "username": "Dan Gittik", "birthday": "1970-01-09 04:22:26.400000", "gender": "m"}, "datetime": "2019-12-04 10:08:07.412000", "pose": {"translation": {"x": 0.15600797533988953, "y": 0.08133671432733536, "z": -0.49068963527679443}, "rotation": {"x": -0.2959017411322204, "y": -0.16749024140672616, "z": -0.04752900380336424, "w": 0.9392178514199446}}}
FEELINGS_EXPECTED = {"user": {"userId": "42", "username": "Dan Gittik", "birthday": "1970-01-09 04:22:26.400000", "gender": "m"}, "datetime": "2019-12-04 10:08:07.412000", "feelings": {"hunger": 0.001, "thirst": 0.003, "exhaustion": 0.002}}
def test_feelings():
	result = run_parser('feelings', MOCK)
	assert result == json.dumps(FEELINGS_EXPECTED)
	
def test_pose():
	result = run_parser('pose', MOCK)
	assert result == json.dumps(POSE_EXPECTED)
