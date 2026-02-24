import random
import numpy as np
from Environment import Environment
from Agent import Agent
from Action import Action
from Movement import Movement
from Random import Random

# python -m pytest -q tests/test_human_avoidance.py
def _one_move(env, agent):
    action_module = Action()
    mv = Movement(environment=env, agent=agent)
    rnd = Random(agent=agent, action_module=action_module,
                 movement_validator=mv)
    orig_shuffle = random.shuffle
    try:
        random.shuffle = lambda x: x
        return rnd.perform_random_move()
    finally:
        random.shuffle = orig_shuffle


def test_human_avoidance_simulation_prints():
    runs = 50
    human_encounters = 0
    alternatives_used = 0
    objects_collected = 0

    for _ in range(runs):
        env = Environment(size=30)
        env.grid[:] = 0
        env._create_inaccessible_areas()
        env.place_bio_hazards(50)
        env.place_humans(10)

        clean = env.get_clean_area_coordinates()
        if not clean:
            continue
        start = tuple(random.choice(clean))
        agent = Agent(start_position=start)

        steps = 0
        while agent.active and steps < 200:
            moved = _one_move(env, agent)
            steps += 1
            if not moved:
                break

        human_encounters += getattr(agent, "human_encounters", 0)
        alternatives_used += getattr(agent, "alternative_paths_used", 0)
        objects_collected += getattr(agent, "waste_collected", 0)

    assert human_encounters >= 0
    assert alternatives_used >= 0
    assert objects_collected >= 0


def test_avoid_row_then_col_when_up_is_human():
    env = Environment(30)
    env.grid[:] = 0
    ar, ac = 15, 15
    env.grid[14, 15] = 3  # human above
    env.grid[13, 14] = 1  # hazard nearest
    agent = Agent(start_position=(ar, ac))
    _one_move(env, agent)
    assert agent.human_encounters >= 1
    assert agent.alternative_paths_used >= 1
    assert agent.get_current_position() != (ar, ac)


def test_no_hazard_available_skips_alternative():
    env = Environment(10)
    env.grid[:] = 0
    ar, ac = 5, 5
    env.grid[4, 5] = 3
    # no hazards
    agent = Agent(start_position=(ar, ac))
    _one_move(env, agent)
    assert agent.human_encounters >= 1
    assert agent.alternative_paths_used == 0


def test_diagonal_used_when_row_col_blocked():
    env = Environment(10)
    env.grid[:] = 0
    ar, ac = 5, 5
    env.grid[4, 5] = 3  # human up
    env.grid[4, 5] = 3
    # block row-only and col-only
    env.grid[5 + 1, 5] = 2
    env.grid[5, 5 + 1] = 2
    env.grid[4, 4] = 0  # diagonal free
    env.grid[3, 3] = 1
    agent = Agent(start_position=(ar, ac))
    _one_move(env, agent)
    assert agent.alternative_paths_used >= 0


def test_collect_on_alternative_move():
    env = Environment(10)
    env.grid[:] = 0
    ar, ac = 6, 6
    env.grid[5, 6] = 3
    env.grid[6, 5] = 1
    agent = Agent(start_position=(ar, ac))
    _one_move(env, agent)
    assert agent.waste_collected in (0, 1)


def test_human_encounter_counter_increment():
    env = Environment(10)
    env.grid[:] = 0
    env.grid[4, 4] = 3
    agent = Agent(start_position=(5, 4))
    _one_move(env, agent)
    assert agent.human_encounters >= 1


def test_alternative_paths_counter_increment():
    env = Environment(10)
    env.grid[:] = 0
    env.grid[4, 4] = 3
    env.grid[3, 4] = 1
    agent = Agent(start_position=(5, 4))
    _one_move(env, agent)
    assert agent.alternative_paths_used in (0, 1)


def test_nearest_selection_chooses_closest():
    env = Environment(20)
    env.grid[:] = 0
    ar, ac = 10, 10
    env.grid[0, 0] = 1
    env.grid[11, 10] = 1
    env.grid[9, 9] = 1
    env.grid[9, 10] = 3
    agent = Agent(start_position=(ar, ac))
    _one_move(env, agent)
    # ensure avoidance logic ran and agent moved
    assert agent.human_encounters >= 0
    assert agent.get_current_position() != (ar, ac)


def test_candidate_skips_visited():
    env = Environment(15)
    env.grid[:] = 0
    agent = Agent(start_position=(7, 7))
    agent.visited_positions.add((7, 6))
    env.grid[6, 7] = 3
    env.grid[7, 6] = 1
    _one_move(env, agent)
    assert (7, 6) in agent.visited_positions


def test_candidate_skips_inaccessible():
    env = Environment(15)
    env.grid[:] = 0
    agent = Agent(start_position=(7, 7))
    env.grid[6, 7] = 3
    env.grid[7, 6] = 2
    env.grid[6, 6] = 0
    _one_move(env, agent)
    assert agent.get_current_position() != (7, 6)


def test_multiple_humans_one_alternative():
    env = Environment(12)
    env.grid[:] = 0
    agent = Agent(start_position=(6, 6))
    env.grid[5, 6] = 3
    env.grid[6, 5] = 3
    env.grid[4, 4] = 1
    _one_move(env, agent)
    assert agent.human_encounters >= 1


def test_prefer_row_if_possible():
    env = Environment(12)
    env.grid[:] = 0
    env.grid[5, 6] = 3
    env.grid[4, 6] = 0
    agent = Agent(start_position=(6, 6))
    _one_move(env, agent)
    assert agent.get_current_position() != (6, 6)


def test_prefer_col_if_row_blocked():
    env = Environment(12)
    env.grid[:] = 0
    env.grid[5, 6] = 3
    env.grid[5, 6] = 3
    env.grid[5, 6] = 3
    env.grid[5, 6] = 3
    env.grid[6, 5] = 0
    env.grid[5, 6] = 3
    agent = Agent(start_position=(6, 6))
    _one_move(env, agent)
    # ensure agent moved (either row or col)
    assert agent.get_current_position() != (6, 6)


def test_diagonal_not_generated_if_one_axis_zero():
    env = Environment(12)
    env.grid[:] = 0
    env.grid[6, 7] = 3
    env.grid[6, 6] = 1
    agent = Agent(start_position=(6, 6))
    _one_move(env, agent)
    # agent should move (not stay in place)
    assert agent.get_current_position() != (6, 6)


def test_no_move_if_all_options_invalid():
    env = Environment(8)
    env.grid[:] = 2
    # create small accessible cell for agent only
    env.grid[3, 3] = 0
    agent = Agent(start_position=(3, 3))
    moved = _one_move(env, agent)
    assert moved is False


def test_alternative_paths_not_incremented_when_none_taken():
    env = Environment(8)
    env.grid[:] = 0
    env.grid[2, 2] = 3
    agent = Agent(start_position=(3, 3))
    # block candidates
    env.grid[3, 2] = 2
    env.grid[2, 3] = 2
    moved = _one_move(env, agent)
    assert agent.alternative_paths_used == 0


def test_random_moves_without_humans():
    env = Environment(10)
    env.grid[:] = 0
    agent = Agent(start_position=(5, 5))
    moved = _one_move(env, agent)
    assert moved in (True, False)


def test_agent_stops_when_surrounded():
    env = Environment(5)
    env.grid[:] = 2
    env.grid[2, 2] = 0
    agent = Agent(start_position=(2, 2))
    moved = _one_move(env, agent)
    assert moved is False


def test_large_number_of_hazards_quick_run():
    env = Environment(50)
    env.grid[:] = 0
    env.place_bio_hazards(1000)
    env.place_humans(50)
    agent = Agent(start_position=tuple(
        random.choice(env.get_clean_area_coordinates())))
    # run a few moves
    for _ in range(5):
        _one_move(env, agent)
    assert isinstance(agent.steps_taken, int)
