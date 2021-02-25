import unittest
from copy import deepcopy
from typing import List, Dict

car_score = 1000
max_time = 6

car_paths = [
    ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou', 'rue-de-rome'],
    ['rue-d-athenes', 'rue-de-moscou', 'rue-de-londres'],
]

road_lengths = {
    'rue-d-amsterdam': 1,
    "rue-de-londres": 1,
    "rue-de-moscou": 3,
    "rue-d-athenes": 1,
    "rue-de-rome": 2
}

graph = {
    0: {
        "out": {'rue-d-amsterdam'},
        "in": {"rue-de-londres"}
    },
    1: {
        "out": {"rue-de-moscou"},
        "in": {"rue-d-amsterdam", "rue-d-athenes"}
    },
    2: {
        "out": {"rue-de-londres", "rue-de-rome"},
        "in": {"rue-de-moscou", "rue-de-rome"}
    },
    3: {
        "out": {"rue-d-athenes"},
        "in": {"rue-de-rome"}
    }
}

schedule = {
    0: [('rue-de-londres', 2)],
    1: [('rue-d-athenes', 2), ('rue-d-amsterdam', 1)],
    2: [('rue-de-moscou', 1)]
}

green_light_schedule = [
    ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  0
    ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  1
    ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou'],  # t =  2
    ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  3
    ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  4
    ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou'],  # t =  5
    ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  6
]


def score(paths: List[List[str]], schedule: List[List[str]], roads: Dict[str, int], max_time: int, car_score: int) -> int:
    score = 0
    car_stuck_time = [0] * len(paths)
    car_paths_copy = deepcopy([path[1:] for path in paths])
    for t in range(max_time):
        for car_id, car_path in enumerate(car_paths_copy):
            if car_stuck_time[car_id] == 0:  # TODO: Add queueing check
                if not car_path:
                    score += (max_time - t) + car_score
                    del car_paths_copy[car_id]
                elif car_path[0] in schedule[t]:  # TODO add queuing check
                    car_stuck_time[car_id] += (roads[car_path[0]] - 1)  # car travels for 1 sec
                    road_now_entered = car_paths_copy[car_id].pop(0)
                    print(road_now_entered)
            else:
                car_stuck_time[car_id] -= 1
    return score


class TestScoring(unittest.TestCase):

    def test_exmaple_scoring(self):
        score_per_car = 1000
        max_time = 6
        schedule = [
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  0
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  1
            ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou'],  # t =  2
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  3
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  4
            ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou'],  # t =  5
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  6
        ]
        car_paths = [
            ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou', 'rue-de-rome'],
            ['rue-d-athenes', 'rue-de-moscou', 'rue-de-londres'],
        ]
        road_lengths = {
            'rue-d-amsterdam': 1,
            "rue-de-londres": 1,
            "rue-de-moscou": 3,
            "rue-d-athenes": 1,
            "rue-de-rome": 2
        }
        expected_score = 1002
        self.assertEqual(expected_score, score(car_paths, schedule, road_lengths, max_time, car_score))
