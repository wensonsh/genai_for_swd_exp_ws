import json
import random
from pathlib import Path

GROUP_DATA_FILE = 'data/groups.json'
TASK_DATA_FILE = 'data/tasks.json'

# initialize group data if it doesn't exist
def initialize_group_data():
    if not Path(GROUP_DATA_FILE).exists():
        with open(GROUP_DATA_FILE, 'w') as f:
            json.dump([], f)

# load group data
def load_group_data():
    with open(GROUP_DATA_FILE, 'r') as f:
        return json.load(f)

# save group data
def save_group_data(data):
    with open(GROUP_DATA_FILE, 'w') as f:
        json.dump(data, f)

# group assignment
def assign_to_group(participant_id):
    """
    Assign a participant to a group and task ensuring balance within each group.

    :param participant_id: str - identifier of an individual participant
    """
    initialize_group_data()
    group_data = load_group_data()

    # check if participant is already assigned
    for participant in group_data:
        if participant['id'] == participant_id:
            return participant['group']

    # count participants per group
    count_default = sum(1 for p in group_data if p['group'] == 'group_default')
    count_tailored = sum(1 for p in group_data if p['group'] == 'group_tailored')

    # determine the group with fewer participants
    if count_default < count_tailored:
        assigned_group = 'group_default'
    elif count_tailored < count_default:
        assigned_group = 'group_tailored'
    else:
        assigned_group = random.choice(['group_default', 'group_tailored'])

    # count tasks within the assigned group
    group_tasks = [p['task'] for p in group_data if p['group'] == assigned_group]
    task_counts = {
        "easy": group_tasks.count("easy"),
        "medium": group_tasks.count("medium"),
        "hard": group_tasks.count("hard")
    }
    assigned_task = min(task_counts, key=task_counts.get)

    # assign the participant to the group and task
    group_data.append({'id': participant_id, 'group': assigned_group, 'task': assigned_task})
    save_group_data(group_data)

    # update participant's JSON file with group and task
    participant_file = f'data/participants/participant_{participant_id}.json'
    with open(participant_file, 'r') as f:
        participant_data = json.load(f)
    participant_data['assigned_group'] = assigned_group
    participant_data['assigned_task'] = assigned_task
    with open(participant_file, 'w') as f:
        json.dump(participant_data, f)

    return assigned_group