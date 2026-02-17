from Environment import Environment
from Agent import Agent
from Action import Action
from Movement import Movement
from Random import Random
import random

env = Environment(size=100)
env.place_bio_hazards(1000)

print("Initial Bio-Hazard Cells:", env.count_bio_hazards())
print("Initial Clean Cells:", env.count_clean_areas())
print("Initial Inaccessible Cells:", env.count_inaccessible_areas())

clean_cells = env.get_clean_area_coordinates()
start_position = tuple(random.choice(clean_cells))
agent = Agent(start_position=start_position)

print(f"Agent starting at: {start_position}")

collected_coordinates = []

action_module = Action()
movement_validator = Movement(environment=env, agent=agent)
random_movement = Random(agent=agent,
                         action_module=action_module,
                         movement_validator=movement_validator)

while agent.active:
    actions = action_module.get_all_actions()
    random.shuffle(actions)
    moved = False

    for action_name in actions:
        dr, dc = action_module.get_action_delta(action_name)
        new_r = agent.get_current_position()[0] + dr
        new_c = agent.get_current_position()[1] + dc
        new_pos = (new_r, new_c)

        if not env.is_accessible(new_pos):
            agent.stop("Next move inaccessible")
            moved = False
            break

        if movement_validator.is_move_valid(new_pos):
            agent.update_position(new_pos)
            moved = True

            if env.is_bio_hazard(new_pos):
                env.clean_cell(new_pos)
                agent.collect_waste()
                collected_coordinates.append(new_pos)

            break

    if not moved and agent.active:
        agent.stop("No valid moves left")

stats = agent.get_statistics()
total_steps = stats["steps_taken"]
total_waste = stats["waste_collected"]
initial_bio_hazard = 1000
percentage_cleaned = (total_waste / initial_bio_hazard) * 100
avg_steps_per_waste = total_steps / total_waste if total_waste > 0 else 0
stop_reason = stats["stop_reason"]

print("\n===== Simulation Finished =====")
print("Stop reason:", stop_reason)
print("Total steps taken:", total_steps)
print("Total waste collected:", total_waste)
print(f"Percentage of bio-hazard cleaned: {percentage_cleaned:.2f}%")
print(f"Average steps per waste collected: {avg_steps_per_waste:.2f}")
print("Total path length:", len(agent.get_path()))

print("\nAgent Path from First to Last:")
for step, pos in enumerate(agent.get_path(), 1):
    print(f"Step {step}: {pos}")

print("\nCollected Bio-Hazard Coordinates:")
for idx, coord in enumerate(collected_coordinates, 1):
    print(f"{idx}: {coord}")

report_file = "simulation_report.txt"

with open(report_file, "w") as f:
    f.write("===== BIO-HAZARD CLEANING AGENT SIMULATION REPORT =====\n\n")

    f.write("1. Data Structures Used:\n")
    f.write("- 2D numpy arrays for environment grid\n")
    f.write("- Lists for storing clean, inaccessible, and bio-hazard coordinates\n")
    f.write("- List for storing agent path\n")
    f.write("- List for storing collected bio-hazard coordinates\n\n")

    f.write("2. Algorithm Description:\n")
    f.write("- Initialize environment (100x100 grid) with inaccessible areas and random bio-hazards\n")
    f.write("- Initialize agent at a random clean cell\n")
    f.write("- While agent is active:\n")
    f.write("    - Randomly select movement direction\n")
    f.write("    - Check if next cell is accessible and not visited\n")
    f.write("    - Move agent to new cell\n")
    f.write("    - If the cell has bio-hazard, collect and mark as cleaned\n")
    f.write("    - Stop if no valid moves or next cell is inaccessible\n\n")

    f.write("3. Test Data:\n")
    f.write(f"- Environment size: 100x100\n")
    f.write(f"- Bio-hazard cells placed: {initial_bio_hazard}\n")
    f.write(f"- Random starting position of agent: {start_position}\n\n")

    f.write("4. Console Output:\n")
    f.write(f"Stop reason: {stop_reason}\n")
    f.write(f"Total steps taken: {total_steps}\n")
    f.write(f"Total waste collected: {total_waste}\n")
    f.write(f"Percentage of bio-hazard cleaned: {percentage_cleaned:.2f}%\n")
    f.write(f"Average steps per waste collected: {avg_steps_per_waste:.2f}\n")
    f.write(f"Total path length: {len(agent.get_path())}\n\n")

    f.write("Agent Path (first to last):\n")
    for step, pos in enumerate(agent.get_path(), 1):
        f.write(f"{step}: {pos}\n")

    f.write("\nCollected Bio-Hazard Coordinates:\n")
    for idx, coord in enumerate(collected_coordinates, 1):
        f.write(f"{idx}: {coord}\n")

    f.write("\n===== END OF REPORT =====\n")

print(f"\nSimulation report saved to {report_file}")
