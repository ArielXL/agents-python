from tools import Constants
from enviroment import Environment

class Simulation:

    def __init__(self, width, height, dirtiness, obstacles, children, interval, id, output_fd):
        self.interval = interval
        self.width = width
        self.height = height
        self.dirtiness = dirtiness
        self.obstacles = obstacles
        self.children = children
        self.id = id
        self.output_fd = output_fd
        self.fired = 0
        self.clean = 0
        self.time_out = 0
        self.dirty_mean = []

    def describe(self):
        self.output_fd.write(f'Environment {self.id}\n width:{self.width} --- height:{self.height} --- dirtiness:{self.dirtiness} --- obstacles:{self.obstacles} --- children:{self.children} --- interval:{self.interval}\n')
        
    def restart(self):
        self.fired = 0
        self.clean = 0
        self.time_out = 0
        self.dirty_mean = []        

    def run(self, robot_init):
        self.environment = Environment(self.width, self.height, self.dirtiness, self.obstacles, self.children)
        self.environment.initialize_robot(robot_init)
        times = 1
        while True:
            print('Turno', times)
            print(self.environment)
            is_final_state, state = self.environment.is_final_state()
            if is_final_state:
                self.terminate(state)
                break
            elif times == 100 * self.interval:
                self.terminate(2)
                break
            else:
                self.environment.robot.move()
                self.environment.natural_change()
                if not times % self.interval:
                    print('RANDOM CHANGE')
                    self.environment.random_change()
            times += 1

    def terminate(self, state):
        print('State', state)
        if state == Constants.DIRTINESS_UP_60_PERCENT:
            self.fired += 1
        elif state == Constants.CHILDREN_UNDER_CONTROL_CLEAN_HOUSE:
            self.clean += 1
        elif state == Constants.TIME_OVER:
            self.time_out += 1
        self.dirty_mean.append(sum(self.environment.dirty_count)/len(self.environment.dirty_count))

    def report_results(self):
        self.output_fd.write(f'Success: {self.clean}\n')
        self.output_fd.write(f'Fired: {self.fired}\n')
        self.output_fd.write(f'Timeout: {self.time_out}\n')
        self.output_fd.write(f'Dirty Mean: {sum(self.dirty_mean)/len(self.dirty_mean)}\n')
        self.output_fd.write('\n')
