from Environment import Environment
from Agent import Agent
from Action import Action
from Movement import Movement
from Random import Random
import random


def run():
    env = Environment(100)
    env.place_bio_hazards(1000)
    clean_cells = env.get_clean_area_coordinates()
    start = tuple(random.choice(clean_cells))
    agent = Agent(start)
    action = Action()
    mv = Movement(env, agent)
    rnd = Random(agent, action, mv)
    while agent.active:
        if not rnd.perform_random_move():
            break
    stats = agent.get_statistics()
    print("Stop reason:", stats["stop_reason"])
    print("Total steps taken:", stats["steps_taken"])
    print("Total waste collected:", stats["waste_collected"])


if __name__ == "__main__":
    run()
