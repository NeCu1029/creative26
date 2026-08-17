import traci
import matplotlib.pyplot as plt


def simulation() -> tuple[dict[str, int], dict[str, int], int]:
    sumo_binary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo"
    sumocfg_dir = "current.sumocfg"
    route_dir = "assets/network.rou.xml"

    sumo_cmd = [
        sumo_binary,
        "-c",
        sumocfg_dir,
        "-r",
        route_dir,
        "--no-warnings",
    ]
    traci.start(sumo_cmd)

    start = dict()
    end = dict()
    time = 0

    while traci.simulation.getMinExpectedNumber() > 0:  # type: ignore
        traci.simulationStep()
        time += 1

        departed = traci.simulation.getDepartedIDList()
        arrived = traci.simulation.getArrivedIDList()

        for veh_id in departed:
            start[veh_id] = time
        for veh_id in arrived:
            end[veh_id] = time

    traci.close()

    return start, end, time


def get_result(veh_start: dict[str, int], veh_end: dict[str, int], time: int) -> None:
    dur = {veh_id: veh_end[veh_id] - veh_start[veh_id] for veh_id in veh_start}
    dur_vals = tuple(dur.values())
    print(f"정체 지수: {sum(dur_vals) / len(dur_vals)} (s)")

    elapse = [[[0] * (time + 1) for _ in range(3)] for _ in range(5)]
    elapse[0][0][0] = 1578
    elapse[1][0][0] = 1168
    elapse[2][0][0] = 1028
    elapse[3][0][0] = 30
    elapse[4][0][0] = 1414

    for veh_id in dur:
        i = int(veh_id.split(".")[0][-1])
        elapse[i][0][veh_start[veh_id]] -= 1
        elapse[i][1][veh_start[veh_id]] += 1
        elapse[i][1][veh_end[veh_id]] -= 1
        elapse[i][2][veh_end[veh_id]] += 1

    for i in range(5):
        for j in range(3):
            for k in range(time):
                elapse[i][j][k + 1] += elapse[i][j][k]

    fig, axes = plt.subplots(3, 2, figsize=(8, 12))
    for i, ax in enumerate(axes.flat):
        if i >= 5:
            break
        ax.stackplot(range(time + 1), elapse[i][0], elapse[i][1], elapse[i][2])
        ax.set_title(f"F{i}")  # error
    fig.tight_layout()
    fig.savefig("images/graph.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    start, end, time = simulation()
    get_result(start, end, time)
