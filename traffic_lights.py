from copy import deepcopy

car_score = 1000
time = 6

car_paths = [
    ['rue-de-londres', 'rue-d-amsterdam' 'rue-de-moscou rue-de-rome'],
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
    0: [('rue-d-londres', 2)],
    1: [('rue-d-athenes', 2), ('rue-d-amsterdam', 1)],
    2: [('rue-de-moscou', 1)]
}

green_light_schedule = [
    ['rue-d-londres', 'rue-d-athenes', 'rue-de-moscou'], # t =  0
    ['rue-d-londres', 'rue-d-athenes', 'rue-de-moscou'], # t =  1
    ['rue-d-londres', 'rue-d-amsterdam', 'rue-de-moscou'], # t =  2
    ['rue-d-londres', 'rue-d-athenes', 'rue-de-moscou'], # t =  3
    ['rue-d-londres', 'rue-d-athenes', 'rue-de-moscou'], # t =  4
    ['rue-d-londres', 'rue-d-amsterdam', 'rue-de-moscou'], # t =  5
]

def score(graph, paths, schedule) -> int:
    car_stuck_time = [0] * len(car_paths)
    car_paths_copy = deepcopy(car_paths)
    for t in range(time):
        for car_id, car_path in enumerate(car_paths_copy):
            if car_stuck_time[car_id] == 0: # TODO: Add queueing check
                if car_paths[0] in green_light_schedule[i]:
                    car_stuck_time[car_id] +=



