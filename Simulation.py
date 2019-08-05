from random import randint
from enum import Enum
from typing import Callable
from tqdm import tqdm
import matplotlib.pyplot as plt

from typing import List, Dict

plt.style.use('fivethirtyeight')


def two_ways_approach(train: List[bool]) -> int:
    """
    Find the number of cars in a circular train only by turning train car lights on or off.
    
    Strategy: Walk through the train around the train, every time you find a light that matches the starting light,
    change it and return to start while keeping track of the number of cars you went through to get there.
        - If the starting car's light has changed when you get back then you know you were just in the starting car and
          can return the number of cars in the train.
        - If the starting car's light is unchanged then repeat this process going in the
          opposite direction that you just came from. This is more efficient than backtracking to the direction you already
          had gone since you are always swapping the light closest to the start rather than potentially backtracking across
          almost the entire train multiple times.
       
    Time Complexity:
        Worst Case: All of the lights on the train are the same. For each new car you see you have to
                    backtrack all the way to the start and begin going in the opposite direction.

        Average Case: We already know lights which are different than the start can't be the start and so there is no
                      reason to backtrack in this case. On average 1/2 of the new lights seen will require backtracking
                      and the other half will not.

        Best Case: First light different than every other light. In this case you can make one complete loop.
    """
    starting_car_state: int = train[0]
    num_cars: int = 0  # Accumulate number of cars in the train

    # Initialize at 1 since we're not counting the first move between the starting car and the second

    num_moves: int = 1
    num_cars_from_start: int = 1

    # at the start move forwards

    moving_forwards = True
    while True:
        actual_position_in_train: int = num_cars_from_start % len(train)

        if num_cars_from_start == 0:
            # Once we get back to start start going in the other direction.
            moving_forwards = not moving_forwards

        if num_cars_from_start == 0 and train[actual_position_in_train] != starting_car_state:

            # If we've backtracked to the starting car and the light has changed then
            # the last light we changed must have been the starting car. We now know
            # how many cars there are!

            assert num_cars == len(train)  # Assert that we were correct

            return num_moves

        # If we run into a car with the same light as the starting car
        elif num_cars_from_start != 0 and train[actual_position_in_train] == starting_car_state:
            # Change the light to the reverse of what it was
            # - i%len(train) so that we don't get index out of bounds
            train[num_cars_from_start % len(train)] = not train[actual_position_in_train]

            # Backtrack to the starting car
            num_moves += abs(num_cars_from_start)
            num_cars = abs(num_cars_from_start)
            num_cars_from_start = 0

        else:
            # If on the way around we encounter a car with a different light than the
            # starting car we know it isn't the starting car and can keep moving.
            if moving_forwards:
                num_cars_from_start += 1
            else:
                num_cars_from_start -= 1

            num_moves += 1


def one_way_approach(train: List[bool]) -> int:
    """
    Find the number of cars in a circular train only by turning train car lights on or off.

    Strategy: Walk through the train around the train, every time you find a light that matches the starting light,
    change it and return to start while keeping track of the number of cars you went through to get there.
        - If the starting car's light has changed when you get back then you know you were just in the starting car and
          can return the number of cars in the train.
        - If the starting car's light is unchanged then repeat the process.

    Time Complexity:
        Worst Case: All of the lights on the train are the same. For each new car you see you have to
                    backtrack all the way to the start.

        Average Case: We already know lights which are different than the start can't be the start and so there is no
                      reason to backtrack in this case. On average 1/2 of the new lights seen will require backtracking
                      and the other half will not.

        Best Case: First light different than every other light. In this case you can make one complete loop. Find the
                   first light and immediately backtrack for a total of 2n moves
    """
    starting_car_state: int = train[0]
    num_cars: int = 0  # Accumulate number of cars in the train

    # Initialize at 1 since we're not counting the first move between the starting car and the second
    num_moves: int = 1
    num_cars_from_start: int = 1

    while True:
        actual_position_in_train = num_cars_from_start % len(train)

        if num_cars_from_start == 0 and train[actual_position_in_train] != starting_car_state:
            # If we've backtracked to the starting car and the light has changed then
            # the last light we changed must have been the starting car. We now know
            # how many cars there are!

            assert num_cars == len(train)  # Assert that we were correct

            return num_moves

        # If we run into a car with the same light as the starting car
        elif num_cars_from_start != 0 and train[actual_position_in_train] == starting_car_state:
            # Change the light to the reverse of what it was
            # - i%len(train) so that we don't get index out of bounds
            train[num_cars_from_start % len(train)] = not train[actual_position_in_train]

            # Backtrack to the starting car
            num_moves += num_cars_from_start
            num_cars = num_cars_from_start
            num_cars_from_start = 0

        else:

            # If on the way around we encounter a car with a different light than the
            # starting car we know it isn't the starting car and can keep moving.
            num_cars_from_start += 1
            num_moves += 1


class Case(Enum):
    Random = 0
    AllOn = 1
    AllOffButStart = 2


def generate_train(n: int, case: Case) -> List[bool]:
    """
    Create a train represented by a list of bool values based on a train case
        - True -> Light on, False -> Light off
    """
    if case is Case.Random:
        return [bool(randint(0, 1)) for _ in range(n)]
    elif case is Case.AllOn:
        return [True for _ in range(n)]
    elif case is Case.AllOffButStart:
        return [True] + [False for _ in range(n - 1)]


def simulate(n: int, iterations: int, strategy: Callable[[List[bool]], int], case: Case) -> float:
    """
    Run multiple iterations to get an average (for random) num of steps to solve an n sized train.
    """

    if case is Case.random:
        steps = []
        for _ in range(iterations):
            train = generate_train(n, case)
            steps.append(strategy(train))

        return sum(steps) / iterations
    else: # No need to run iterations for identical trains
        train = generate_train(n, case)
        return strategy(train)


def generate_stats(case: Case, min_train_len=1, max_train_len=10, iterations=1_000):
    """
    Generate statistics for trains over a range of sizes.
    """
    one_way_stats: Dict[int, float] = {}
    two_way_stats: Dict[int, float] = {}

    for i in tqdm(range(min_train_len, max_train_len + 1)):
        one_way_stats[i] = simulate(i, iterations, one_way_approach, case)
        two_way_stats[i] = simulate(i, iterations, two_ways_approach, case)

    return one_way_stats, two_way_stats


def plot(one_way_stats: Dict[int, float], two_way_stats: Dict[int, float], case: str, ax):
    """
    Plot a simulation of both strategies on a type of train.
    """
    one_way_x, one_way_y = list(one_way_stats.keys()), list(one_way_stats.values())
    ax.plot(one_way_x, one_way_y, label=f'One Way', color='red',  alpha=.5)

    two_way_x, two_way_y = list(two_way_stats.keys()), list(two_way_stats.values())
    ax.plot(two_way_x, two_way_y, label=f'Two Way', color='blue', alpha=.5)

    ax.set_title(case)



# Generate Stats
all_on_one_way_stats, all_on_two_way_stats = generate_stats(Case.AllOn)
random_one_way_stats, random_two_way_stats = generate_stats(Case.Random)
all_off_but_start_one_way_stats, all_off_but_start_two_way_stats = generate_stats(Case.AllOffButStart)

# Plot Stats
fig, axs, = plt.subplots(1, 3, sharey='row')

plot(random_one_way_stats, random_two_way_stats, 'Lights on at random', axs[0])
plot(all_on_one_way_stats, all_on_two_way_stats, 'All lights are on', axs[1])
plot(all_off_but_start_one_way_stats, all_off_but_start_two_way_stats, 'All lights off (except start)', axs[2])

axs[1].set_xlabel('Number of cars in the train')
axs[0].set_ylabel(f'Avg Moves')
plt.savefig('simulation_outcomes.png')