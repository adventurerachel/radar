from radar.monitors.barclaycard import BarclaycardMonitor
from radar.state import load_state, save_state
from radar.diff import diff_dicts


def run_monitor(monitor):
    print(f"\nRunning {monitor.name}...")

    current = monitor.collect()
    previous = load_state(monitor.name)

    if not previous:
        print("First run — saving state.")
        save_state(monitor.name, current)
        return

    diff = diff_dicts(previous, current)

    if diff["added"] or diff["removed"] or diff["changed"]:
        print("Changes detected:\n")

        for k, v in diff["changed"].items():
            print(f"• {k}: {v['from']} → {v['to']}")

        for k, v in diff["added"].items():
            print(f"• added {k}: {v}")

        for k, v in diff["removed"].items():
            print(f"• removed {k}: {v}")

        save_state(monitor.name, current)

    else:
        print("No meaningful changes.")


if __name__ == "__main__":
    run_monitor(BarclaycardMonitor())