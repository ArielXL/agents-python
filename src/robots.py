from elements import *

class Robot(Element):

    def __init__(self, pos, environment):
        Element.__init__(self, pos, environment)
        self.child = False
        self.playpen = None

    def bfs(self):
        d = {(i, j): None for i in range(self.environment.height) for j in range(self.environment.width)}
        pi = {(i, j): None for i in range(self.environment.height) for j in range(self.environment.width)}
        d[self.pos] = 0
        q = [self.pos]
        while q:
            u = q.pop(0)

            for direction in range(0, 4):
                if direction == N:
                    v = (u[0] - 1, u[1])
                elif direction == E:
                    v = (u[0], u[1] + 1)
                elif direction == S:
                    v = (u[0] + 1, u[1])
                elif direction == W:
                    v = (u[0], u[1] - 1)

                if self.environment.is_in(v) and d[v] is None and type(self.environment[v]) is not Obstacle:
                    element = self.environment[v]
                    d[v] = d[u] + 1
                    pi[v] = u
                    non_empty_playpen = type(element) is Playpen and element.child
                    on_child_no_pass = self.environment.robot.child and type(element) is Child
                    if not (on_child_no_pass or non_empty_playpen):
                        q.append(v)
                        
        return d,pi

    def get_path(self, pi, v):
        path = []
        while pi[v]:
            path.insert(0, v)
            v = pi[v]
        return path
            
    def find_near_element(self, d, elements):
        min = self.environment.height * self.environment.width
        element = None
        for e in elements:
            if d[e] and d[e] < min:
                min = d[e]
                element = e
        return element

    def find_far_element(self, d, elements):
        max = 0
        element = None
        for e in elements:
            if d[e] and d[e] > max:
                max = d[e]
                element = e
        return element

    def move(self):
        pass

    def blocked(self):
        directions = [0, 1, 2, 3]
        random.shuffle(directions)
        for direction in directions:
            next = self.find_next_step(direction)
            if self.environment.is_in(next) and self.environment[next] is not Obstacle and not (self.environment[next] is Playpen and self.environment[next].child):
                self.pos = next
                print('Robot Position', next)
                break

class ChildsFirstRobot(Robot):
   
    def move(self):
        d, pi = self.bfs()
        dirty_percent = self.environment.get_dirty_percent()
        if dirty_percent > 50:
            print('High Dirtiness Level')
            if self.child:
                if not self.environment[self.pos]:
                    self.child = False
                    self.environment[self.pos] = Child(self.pos, self.environment)
                    print('Robot droped child', self.pos)
                else:
                    if self.playpen and d[self.playpen]:
                        path = self.get_path(pi, self.playpen)
                        next = path[1] if len(path) > 1 else path[0] 
                        self.pos = next
                        print('Robot Position', next)
                        if next == self.playpen:
                            self.child = False
                            self.environment[next].child = True
                            print('Robot placed child in Playpen', next)
                            self.playpen = None
                    else:
                        self.playpen = None
                        playpens = self.environment.get_playpen()
                        empty_playpens = [ p for p in playpens if not self.environment[p].child]
                        far_playpen = self.find_far_element(d, empty_playpens)
                        if far_playpen:
                            self.playpen = far_playpen
                            path = self.get_path(pi, far_playpen)
                            next = path[1] if len(path) > 1 else path[0] 
                            self.pos = next
                            print('Robot Position', next)
                            if next == far_playpen:
                                self.child = False
                                self.environment[next].child = True
                                print('Robot placed child in Playpen', next)
                        else:
                            print('Robot BLOCKED')
                            self.blocked()
            else:
                dirties = self.environment.get_dirty_spaces()
                near_dirty = self.find_near_element(d, dirties)
                if near_dirty:
                    path = self.get_path(pi, near_dirty)
                    next = path[0]
                    self.pos = next
                    print('Robot Position', next)
                else:
                    print('Robot BLOCKED')
                    self.blocked()

        else:
            if self.child:
                if self.playpen and d[self.playpen]:
                        path = self.get_path(pi, self.playpen)
                        next = path[1] if len(path) > 1 else path[0] 
                        self.pos = next
                        print('Robot Position', next)
                        if next == self.playpen:
                            self.child = False
                            self.environment[next].child = True
                            print('Robot placed child in Playpen', next)
                            self.playpen = None
                else:
                    self.playpen = None
                    playpens = self.environment.get_playpen()
                    empty_playpens = [ p for p in playpens if not self.environment[p].child]
                    far_playpen = self.find_far_element(d, empty_playpens)
                    if far_playpen:
                        self.playpen = far_playpen
                        path = self.get_path(pi, far_playpen)
                        next = path[1] if len(path) > 1 else path[0] 
                        self.pos = next
                        print('Robot Position', next)
                        if next == far_playpen:
                            self.child = False
                            self.environment[next].child = True
                            print('Robot placed child in Playpen', next)
                    else:
                        print('Robot BLOCKED')
                        self.blocked()
            else:
                childs = self.environment.get_childs()
                if childs:
                    near_child = self.find_near_element(d, childs)
                    if near_child:
                        path = self.get_path(pi, near_child)
                        next = path[0]
                        self.pos = next
                        print('Robot Position', next)
                        if next == near_child:
                            self.child = True
                            self.environment[next] = None
                            print('Robot pick up child', next)
                    else:
                        print('Robot BLOCKED')
                        self.blocked()                        
                elif type(self.environment[self.pos]) is Dirty:
                    self.environment[self.pos] = None
                    print('Robot cleaned Dirty', self.pos)
                else:
                    dirties = self.environment.get_dirty_spaces()
                    near_dirty = self.find_near_element(d, dirties)
                    if near_dirty:
                        path = self.get_path(pi, near_dirty)
                        next = path[0]
                        self.pos = next
                        print('Robot Position', next)
                    else:
                        print('Robot BLOCKED')
                        self.blocked()                        

class NearFirstRobot(Robot):

    def move(self):
        d, pi = self.bfs()
        if self.child:
            if self.playpen and d[self.playpen]:
                    path = self.get_path(pi, self.playpen)
                    next = path[1] if len(path) > 1 else path[0] 
                    self.pos = next
                    print('Robot Position', next)
                    if next == self.playpen:
                        self.child = False
                        self.environment[next].child = True
                        print('Robot placed child in Playpen', next)
                        self.playpen = None
            else:
                self.playpen = None         
                playpens = self.environment.get_playpen()
                empty_playpens = [ p for p in playpens if not self.environment[p].child]
                far_playpen = self.find_far_element(d, empty_playpens)
                if far_playpen:
                    self.playpen = far_playpen
                    path = self.get_path(pi, far_playpen)
                    next = path[1] if len(path) > 1 else path[0] 
                    self.pos = next
                    if next == far_playpen:
                        self.child = False
                        self.environment[next].child = True
                else:
                    print('Robot BLOCKED')
                    self.blocked() 
        elif type(self.environment[self.pos]) is Dirty:
            self.environment[self.pos] = None
            print('Robot cleaned Dirty', self.pos)
        else:
            elements = self.environment.get_dirty_spaces() + self.environment.get_childs()
            near_element = self.find_near_element(d, elements)
            if near_element:
                path = self.get_path(pi, near_element)
                next = path[0]
                self.pos = next
                if type(self.environment[next]) is Child:
                    self.child = True
                    self.environment[next] = None
                    print('Robot pick up child', next)
            else:
                print('Robot BLOCKED')
                self.blocked()           
