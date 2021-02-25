import unittest
from copy import deepcopy
from itertools import cycle
from random import random
from typing import List, Dict, Tuple

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

road_destinations = {
    "rue-d-amsterdam": 1,
    "rue-d-athenes": 1,
    "rue-de-londres": 0,
    "rue-de-moscou": 3,
    "rue-de-rome": 2,

}


graph = {
    0: {
        "out": {'rue-d-amsterdam'},
        "in": {"rue-de-londres"},
        "schedule": [('rue-de-londres', 2)],
    },
    1: {
        "out": {"rue-de-moscou"},
        "in": {"rue-d-amsterdam", "rue-d-athenes"},
        "schedule": [('rue-d-athenes', 2), ('rue-d-amsterdam', 1)],

    },
    2: {
        "out": {"rue-de-londres", "rue-de-rome"},
        "in": {"rue-de-moscou"},
        "schedule": [('rue-de-moscou', 1)],
    },
    3: {
        "out": {"rue-d-athenes"},
        "in": {"rue-de-rome"},
        "schedule": []
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

Schedule = Dict[int, List[Tuple[str, int]]]

class Algorithm:
    """OOoooo"""

    CHILDREN = 5

    def __init__(self, data):
        self.init_graph(data)
        self.init_roads(data)

    def _init_roads(self, data):
        self.road_lengths = road_lengths
        self.roads_destinations = road_destinations

    def _init_graph(self, data):
        self.graph  = {
            0: {
                "out": {'rue-d-amsterdam'},
                "in": {"rue-de-londres"},
                "schedule": [],
            },
            1: {
                "out": {"rue-de-moscou"},
                "in": {"rue-d-amsterdam", "rue-d-athenes"},
                "schedule": [],

            },
            2: {
                "out": {"rue-de-londres", "rue-de-rome"},
                "in": {"rue-de-moscou"},
                "schedule": [],
            },
            3: {
                "out": {"rue-d-athenes"},
                "in": {"rue-de-rome"},
                "schedule": []
            }
        }

    @property
    def schedule(self) -> Schedule:
        # TODO: Optimise
        return {key: self.graph[key]['schedule'] for key in self.graph.keys()}

    def run(self) -> int:
        children_schedules = self.reproduce()
        scores = [
            score(self.paths, schedule, self.road_lengths, self.time, self.car_score)
            for schedule in children_schedules
        ]

    def reproduce(self) -> List[Schedule]:
        def update_randomly(keys, schedule) -> Schedule:
            class UpdateChoices:
                ADD_STREET = 0
                REMOVE_STREET = 1
                MODIFY_STREET = 2
            key_to_update = random.choice(keys)
            schedule = deepcopy(schedule)
            updates = [UpdateChoices.MODIFY_STREET]
            current_roads = [schedule_data[0] for schedule_data in schedule[key_to_update]]
            in_roads = self.graph[key_to_update]['in']
            if len(current_roads) < len(in_roads):
                updates.append(UpdateChoices.ADD_STREET)
            if len(current_roads) > 1:
                updates.append(UpdateChoices.REMOVE_STREET)


            schedule[key_to_update]
        schedule = self.schedule
        return list(schedule)


def schedule_to_green_lights(schedule: Schedule, time: int) -> List[List[str]]:
    green_lights = [[] for _ in range(time + 1)]
    for key in schedule.keys():
        time_left = 0
        green_street = None
        lights = cycle(schedule[key])
        for t in range(time + 1):
            if time_left == 0:
                green_street, green_time = next(lights)
                time_left += green_time - 1  # 1 second goes by already
            else:
                time_left -= 1
            green_lights[t].append(green_street)
    return green_lights


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

    def test_example_scoring(self):
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


class TestGreenLightGenerator(unittest.TestCase):

    def test_green_light_generation(self):

        max_time = 6

        schedule = {
            0: [('rue-de-londres', 2)],
            1: [('rue-d-athenes', 2), ('rue-d-amsterdam', 1)],
            2: [('rue-de-moscou', 1)]
        }

        expected_green_lights = [
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  0
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  1
            ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou'],  # t =  2
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  3
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  4
            ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou'],  # t =  5
            ['rue-de-londres', 'rue-d-athenes', 'rue-de-moscou'],  # t =  6
        ]

        self.assertEqual(expected_green_lights, schedule_to_green_lights(schedule, max_time))
