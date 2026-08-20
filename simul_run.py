import libsumo
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt

SUMO_BINARY = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo"
SUMOCFG_DIR = "current.sumocfg"
ROUTE_DIR_ORI = "assets/network.rou.xml"
ROUTE_DIR_NEW = "assets/network-new.rou.xml"
TREE = et.parse(ROUTE_DIR_ORI)
ROOT = TREE.getroot()
SUMO_CMD = [
    SUMO_BINARY,
    "-c",
    SUMOCFG_DIR,
    "-r",
    ROUTE_DIR_NEW,
    "--no-warnings",
]


def simulation() -> list[int]:
    res = []
    route_val = [int(flow.get("number")) for flow in ROOT.findall("flow")]  # type: ignore

    for rate in range(80, 160, 10):
        for i, flow in enumerate(ROOT.findall("flow")):
            flow.set("number", str(route_val[i] * rate // 100))
        TREE.write(ROUTE_DIR_NEW)

        print(f"{rate}% 시뮬레이션 시작")

        libsumo.start(SUMO_CMD)
        time = 0
        while libsumo.simulation.getMinExpectedNumber() > 0:  # type: ignore
            libsumo.simulationStep()
            time += 1
        libsumo.close()
        res.append(time)

    return res


result = simulation()
plt.scatter(range(80, 160, 10), result)
plt.show()
