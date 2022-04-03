from robots import *
from simulation import Simulation

def childs_first_robot(enviroments, output_fd):

    output_fd.write(f'------------------------------------------------------------------------\n')
    output_fd.write(f'Robot: ChildsFirstRobot\n')
    output_fd.write(f'------------------------------------------------------------------------\n')

    for enviroment in enviroments:
        enviroment.describe()
        for i in range(30):
            enviroment.run(ChildsFirstRobot)
        enviroment.report_results()
        enviroment.restart()

def near_first_robot(enviroments, output_fd):

    output_fd.write(f'------------------------------------------------------------------------\n')
    output_fd.write(f'Robot: NearFirstRobot\n')
    output_fd.write(f'------------------------------------------------------------------------\n')

    for enviroment in enviroments:
        enviroment.describe()
        for i in range(30):
            enviroment.run(NearFirstRobot)
        enviroment.report_results()
        enviroment.restart()

def main():

    output_fd = open('output.txt', 'w')

    enviroments = [
        Simulation(width=10, height=10, dirtiness=25, obstacles=15, children=5, interval=10, id=1, output_fd=output_fd),
        Simulation(width=7, height=8, dirtiness=15, obstacles=10, children=3, interval=5, id=2, output_fd=output_fd),
        Simulation(width=7, height=8, dirtiness=15, obstacles=10, children=3, interval=20, id=3, output_fd=output_fd),
        Simulation(width=15, height=15, dirtiness=15, obstacles=15, children=10, interval=50, id=4, output_fd=output_fd),
        Simulation(width=5, height=5, dirtiness=10, obstacles=5, children=2, interval=5, id=5, output_fd=output_fd),
        Simulation(width=10, height=5, dirtiness=20, obstacles=20, children=3, interval=10, id=6, output_fd=output_fd),
        Simulation(width=10, height=10, dirtiness=30, obstacles=10, children=5, interval=20, id=7, output_fd=output_fd),
        Simulation(width=10, height=10, dirtiness=10, obstacles=30, children=5, interval=30, id=8, output_fd=output_fd),
        Simulation(width=9, height=9, dirtiness=15, obstacles=20, children=3, interval=20, id=9, output_fd=output_fd),
        Simulation(width=10, height=10, dirtiness=20, obstacles=20, children=4, interval=20, id=10, output_fd=output_fd)
    ]

    childs_first_robot(enviroments, output_fd)

    near_first_robot(enviroments, output_fd)

if __name__ == '__main__':
    main()
