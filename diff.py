def diff_dicts(old: dict, new: dict) -> dict:
    """
    Returns a structured diff between two dictionaries.
    """

    changes = {
        "added": {},
        "removed": {},
        "changed": {},
        "unchanged": {},
    }

    old_keys = set(old.keys())
    new_keys = set(new.keys())

    for k in old_keys - new_keys:
        changes["removed"][k] = old[k]

    for k in new_keys - old_keys:
        changes["added"][k] = new[k]

    for k in old_keys & new_keys:
        if old[k] != new[k]:
            changes["changed"][k] = {
                "from": old[k],
                "to": new[k],
            }
        else:
            changes["unchanged"][k] = old[k]

    return changes