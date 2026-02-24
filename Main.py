from Environment import Environment
from Agent import Agent
from Action import Action
from Movement import Movement
from Random import Random
import random


def run(runs=100):
    total_human = 0
    total_alts = 0
    total_objects = 0
    for _ in range(runs):
        env = Environment(100)
        env.place_bio_hazards(1000)
        env.place_humans(30)
        clean_cells = env.get_clean_area_coordinates()
        if not clean_cells:
            continue
        start = tuple(random.choice(clean_cells))
        agent = Agent(start)
        action = Action()
        mv = Movement(env, agent)
        rnd = Random(agent, action, mv)
        steps = 0
        while agent.active and steps < 1000:
            moved = rnd.perform_random_move()
            steps += 1
            if not moved:
                break
        total_human += getattr(agent, "human_encounters", 0)
        total_alts += getattr(agent, "alternative_paths_used", 0)
        total_objects += getattr(agent, "waste_collected", 0)

    print("-- Number of human encountered:", total_human)
    print("-- Number of nearest path selected and avoided:", total_alts)
    print("-- Number of object collected:", total_objects)


if __name__ == "__main__":
    run()
