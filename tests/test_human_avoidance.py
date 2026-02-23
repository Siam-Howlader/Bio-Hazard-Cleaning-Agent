import random
from Environment import Environment
from Agent import Agent
from Action import Action
from Movement import Movement
from Random import Random


def test_human_avoidance_simulation_prints():
    runs = 100
    human_encounters = 0
    alternatives_used = 0
    objects_collected = 0

    for _ in range(runs):
        env = Environment(size=30)
        env.place_bio_hazards(200)
        env.place_humans(30)

        clean = env.get_clean_area_coordinates()
        if not clean:
            continue
        start = tuple(random.choice(clean))
        agent = Agent(start_position=start)

        action_module = Action()
        movement_validator = Movement(environment=env, agent=agent)
        random_movement = Random(agent=agent, action_module=action_module, movement_validator=movement_validator)

        steps = 0
        while agent.active and steps < 1000:
            moved = random_movement.perform_random_move()
            steps += 1
            if not moved:
                break

        human_encounters += getattr(agent, "human_encounters", 0)
        alternatives_used += getattr(agent, "alternative_paths_used", 0)
        objects_collected += getattr(agent, "waste_collected", 0)

    print("-- Number of human encountered:", human_encounters)
    print("-- Number of nearest path selected and avoided:", alternatives_used)
    print("-- Number of object collected:", objects_collected)
