def handle_human_encounter(agent, env, movement_validator):
    
    agent.human_encounters += 1
    bio = env.get_bio_hazard_coordinates()
    if not bio:
        return False
    ar, ac = agent.get_current_position()
    nearest = min(bio, key=lambda b: abs(b[0] - ar) + abs(b[1] - ac))
    tr, tc = nearest
    sdr = (tr > ar) - (tr < ar)
    sdc = (tc > ac) - (tc < ac)
    cands = []
    if sdr:
        cands.append((ar + sdr, ac))
    if sdc:
        cands.append((ar, ac + sdc))
    if sdr and sdc:
        cands.append((ar + sdr, ac + sdc))
    for cand in cands:
        if movement_validator.is_move_valid(agent.get_current_position(), cand, getattr(agent, "visited_positions", set())):
            agent.update_position(cand)
            agent.alternative_paths_used += 1
            if env.is_bio_hazard(cand):
                env.clean_cell(cand)
                agent.collect_waste()
            return True
    return False
