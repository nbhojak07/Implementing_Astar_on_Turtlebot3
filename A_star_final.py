# ENPM 661 - Planning for Autonomous Robots
# Project 3 - Implementing A star search Algorithm for Rigid Robot
# Team - Nidhi Bhojak           , UID - 116787529
#        Kulbir Singh Ahluwalia , UID - 116836050

# import intersection_check as ic

from intersection_check import *
from obstacle_check import *
from matplotlib.patches import *
import numpy as np
import math
import matplotlib.pyplot as plt
import cv2
from time import process_time
import cv2

visited = np.zeros((600,400,12))


class GraphNode:
    def __init__(self, point):
        self.position = point
        self.cost = math.inf
        self.total_cost = 0
        self.parent = None
        self.angle = 0


def heu(node1, node2):
  dist= math.sqrt( (node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)
  return dist


def move_along(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot):
    angle = math.radians(test_point_angle + 0)
    new_point_x= test_point_coord[0] + step_size_robot*math.cos(angle)
    new_point_y= test_point_coord[1] + step_size_robot*math.sin(angle)
    new_point = [new_point_x, new_point_y, test_point_angle]
    action_cost = 1
    test_point_obstacle_check(clearance, radius_rigid_robot, test_point_coord, image)
    #intersection_check_of_vectors(clearance, radius_rigid_robot, test_point_coord, new_point)
    if (test_point_obstacle_check(clearance, radius_rigid_robot, new_point, image)) == False:
        return new_point, action_cost
    else:
        return None, None
    #return new_point, action_cost


def move_up1(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot):
    angle = math.radians(test_point_angle + 30)
    new_point_x= test_point_coord[0] + step_size_robot*math.cos(angle)
    new_point_y= test_point_coord[1] + step_size_robot*math.sin(angle)
    new_point = [new_point_x, new_point_y, test_point_angle + 30]

    # intersection_check_of_vectors(clearance, radius_rigid_robot, parent_coord, child_coord):
    # test_point_coord = parent_coord
    # new_point = child_coord

    action_cost = 1
    # intersection_check_of_vectors(clearance, radius_rigid_robot, test_point_coord, new_point)
    if (test_point_obstacle_check(clearance, radius_rigid_robot, new_point, image)) == False:
        return new_point, action_cost
    else:
        return None, None
    # return new_point, action_cost

def move_up2(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot):
    angle = math.radians(test_point_angle + 60)
    new_point_x= test_point_coord[0] + step_size_robot*math.cos(angle)
    new_point_y= test_point_coord[1] + step_size_robot*math.sin(angle)
    new_point = [new_point_x, new_point_y, test_point_angle + 60]
    action_cost = 1
    # intersection_check_of_vectors(clearance, radius_rigid_robot, test_point_coord, new_point)
    if (test_point_obstacle_check(clearance, radius_rigid_robot, new_point, image)) == False:
        return new_point, action_cost
    else:
        return None, None
    # return new_point, action_cost


def move_dn1(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot):
    angle = math.radians(test_point_angle - 30)
    new_point_x= test_point_coord[0] + step_size_robot*math.cos(angle)
    new_point_y= test_point_coord[1] + step_size_robot*math.sin(angle)
    new_point = [new_point_x, new_point_y, test_point_angle - 30]
    action_cost = 1
    # intersection_check_of_vectors(clearance, radius_rigid_robot, test_point_coord, new_point)
    if (test_point_obstacle_check(clearance, radius_rigid_robot, new_point, image)) == False:
        return new_point, action_cost
    else:
        return None, None
    # return new_point, action_cost


def move_dn2(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot):
    angle = math.radians(test_point_angle - 60)
    new_point_x= test_point_coord[0] + step_size_robot*math.cos(angle)
    new_point_y= test_point_coord[1] + step_size_robot*math.sin(angle)
    new_point = [new_point_x, new_point_y, test_point_angle - 60]
    action_cost = 1
    # intersection_check_of_vectors(clearance, radius_rigid_robot, test_point_coord, new_point)
    if (test_point_obstacle_check(clearance, radius_rigid_robot, new_point, image)) == False:
        return new_point, action_cost
    else:
        return None, None
    # return new_point, action_cost


def get_new_node(image, action, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot):
    action_map = {
        'S': move_along(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot),
        'UP1': move_up1(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot),
        'UP2': move_up2(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot),
        'DN1': move_dn1(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot),
        'DN2': move_dn2(image, clearance, radius_rigid_robot, test_point_coord, test_point_angle, step_size_robot),
       }
    return action_map[action]


def get_minimum_element(queue):
    min_index = 0
    for index in range(len(queue)):
        if queue[index].total_cost < queue[min_index].total_cost:
            min_index = index
    return queue.pop(min_index)

def round_off_till_threshold(number, threshold):
    number_double = round((number / threshold))
    return int(number_double*threshold)


def approximation(x, y, angle_theta):
    x = round_off_till_threshold(x, 0.5)
    y = round_off_till_threshold(y, 0.5)

    angle_theta = round_off_till_threshold(angle_theta, 30)
    return (x, y, int(angle_theta/30))


def check_goal(position, goal):
  if (((position[0]- goal[0])**2)+ ((position[1] - goal[1])**2)) <= (1.5)**2:
    return True
  else:
    return False


def reset_angle_in_range(angle):
      if angle >= 360:
          return angle % 360
      if angle < 0:
          return 360 + angle
      else:
          return angle



def find_path_astar(image, start_node_pos, goal_node_pos, clearance, radius_rigid_robot, step_size_robot, initial_angle):
    # class GraphNode:
    #     def __init__(self, point):            #initialise attributes position, cost and parent
    #         self.position = point
    #         self.cost = math.inf    #initialise initial cost as infinity for every node
    #         self.parent = None      #initialise initial parent as None for every node
    #         self.angle = 0          #initialise initial angle
    start_node = GraphNode(start_node_pos)
    start_node.cost = 0  # initialise cost of start node = 0
    start_node.angle = initial_angle #Set the angle of start node as given by user

    # visited = list()  # list of all visited nodes
    queue = [start_node]  # queue is a list that contains yet to be explored node "objects"
    # print(queue)

    actions = ["S", "UP1", "UP2", "DN1", "DN2"]  # define a list with all the possible actions
    visited_set = set()  # a set is used to remove the duplicate node values
    visited_list = []  # a list is used to visualize the order of nodes visited and to maintain order
    cost_updates_matrix = np.zeros((400, 600, 12), dtype=object)   #To keep track of duplicate nodes
    # print(cost_updates_matrix)

    cost_updates_matrix[:, :, :] = math.inf  # initialise cost update matrix with infinite costs for every node
    goal_reached = False  # set the goal_reached flag to zero initially
    parent_child_map = {}  # define a dictionary to store parent and child relations
    # key in a dict can't be a list, only immutable things can be used as keys, so use tuples as keys
    parent_child_map[tuple([start_node_pos[0], start_node_pos[1], initial_angle])] = None  # for start node, there is no parent
    # print(parent_child_map)

    start = process_time()  # start the time counter for calculating run time for the A* search algorithm
    last_node = None
    while len(queue) > 0:  # as long as there are nodes yet to be checked in the queue, while loop keeps running
        current_node = get_minimum_element(queue)  # choose the node object with minimum cost
        current_point = current_node.position  # store the position from the (minimum cost) current_node in "current_point"
        current_angle = current_node.angle
        # visited.append(str(current_point))  # convert the current_point to an immutable string and store it in the list "visited"

        if approximation(current_point[0], current_point[1], current_angle) not in visited_set:
            visited_list.append(current_node)
        visited_set.add(approximation(current_point[0], current_point[1], current_angle))  # you can only put immutable objects in a set, string is also immutable


        if check_goal(current_point, goal_node_pos):
            goal_reached = True
            print('Goal Reached')
            print("Cost = ", current_node.cost)
            last_node = current_node

            break

        # to generate, explore and append possible next positions, make a list of all the generated child nodes
        child_nodes = []
        # actions = ["S", "UP1", "UP2", "DN1", "DN2"] ,     action = iterable element
        for action in actions:
            # get_new_node is run for every action , U, D, L, R, UR, DR, UL, DL
            new_point, base_cost = get_new_node(image, action, clearance, radius_rigid_robot, current_point, current_angle, step_size_robot)
            print(new_point)
            if new_point is not None:  # present in the explorable area and not in obstacle
                print(len(new_point))
              #if new_point is not visited[int()][][]
                child_nodes.append((new_point, base_cost))  # append the new node in child nodes along with cost

        # print(child_nodes[0])        #first element of the list = ([x,y,theta],cost)
        # print(child_nodes[0][0])     #first element of first element of the list = [x,y,theta]
        # print(child_nodes[0][0][1])  #second element of first element of first element of the list = y

        for child in child_nodes:  # child = iterable element in child_nodes = of the format ([x,y],cost)
            child[0][2] = reset_angle_in_range(child[0][2])
            approx_x, approx_y, approx_theta = approximation(child[0][0], child[0][1], child[0][2])
            if approximation(child[0][0], child[0][1], child[0][2]) not in visited_set:
                child_position = child[0]  # child[0] = [x,y]
                child_position_x = child[0][0]  # child[0][0] = x
                child_position_y = child[0][1]  # child[0][1] = y
                print(approx_x, approx_y, approx_theta)
                prev_cost = cost_updates_matrix[approx_y, approx_x, approx_theta]  # row,column
                # prev_cost = cost_updates_matrix[y, x]  # row,column

                # add the cost of the child to the current node's cost to get new cost
                new_cost = child[1] + current_node.cost  # child[1] = cost
                total_cost = new_cost + heu(child[0], goal_node_pos)

                if total_cost < prev_cost:
                    print(approx_x, approx_y, approx_theta)
                    cost_updates_matrix[approx_y, approx_x, approx_theta] = new_cost
                    child_node = GraphNode(child[0])
                    child_node.cost = new_cost
                    child_node.parent = current_node
                    child_node.total_cost = total_cost
                    child_node.angle = child[0][2]
                    queue.append(child_node)  # child_node is yet to be explored
                    parent_child_map[tuple(child[0])] = tuple([current_point[0], current_point[1], current_angle])  # key, always immutable, here, tuple = tuple(child[0])
                    #   #value, can be anything = current_point

    end = process_time()
    print("Time to completion:", (end - start))

    if goal_reached:
        print('Reached')
        return visited_list, parent_child_map, last_node
    else:
        return None, None, None


def check_inputs_wrt_obstacles(start_node_x, start_node_y, goal_node_x, goal_node_y):
    if test_point_obstacle_check(clearance, radius_rigid_robot, [start_node_x, start_node_y], None):
        print("Start node is inside an obstacle. Enter some other coordinates. Restart program!")
        exit(0)

    if test_point_obstacle_check(clearance, radius_rigid_robot, [goal_node_x, goal_node_y], None):
        print("Goal node is inside an obstacle. Enter some other coordinates. Restart program!")
        exit(0)


radius_rigid_robot = int(input("Enter the radius of the rigid robot \n"))
clearance = int(input("Enter the desired clearance for the rigid robot\n"))
# Uncomment to choose different positions:-
start_node_x = int(input("Enter the starting x coordinate for the rigid robot\n"))
start_node_y = int(input("Enter the starting y coordinate for the rigid robot\n"))
initial_angle = int(input("Enter the initial angle of the robot in degree\n"))

step_size_robot = int(input("Enter the step size of movement of the robot: "))
if (step_size_robot < 1 and step_size_robot > 10):
    print("Step_size_robot is out of range. Enter step_size_robot from [0,10]. Restart program!")
    exit(0)


goal_node_x = int(input("Enter the goal x coordinate for the rigid robot\n"))
goal_node_y = int(input("Enter the goal y coordinate for the rigid robot\n"))

# # for testing
# start_node_x = 50
# start_node_y = 30
#
# goal_node_x = 150
# goal_node_y = 150
#
# step_size_robot = 1
# initial_angle = 60
#
# clearance = 1
# radius_rigid_robot = 1
augment_distance = radius_rigid_robot + clearance

if (start_node_x < 0 and start_node_x > 300) and (goal_node_x < 0 and goal_node_x > 300):
    print("X coordinate is out of range. Enter x from [0,300]. Restart program!")
    exit(0)

if (start_node_y < 0 and start_node_y > 200) and (goal_node_y < 0 and goal_node_y > 200):
    print("Y coordinate is out of range. Enter y from [0,200]. Restart program!")
    exit(0)

check_inputs_wrt_obstacles(start_node_x, start_node_y, goal_node_x, goal_node_y)


# print(test_point_obstacle_check(0,0,[230,40]))


def plot_map(clearance, radius_rigid_robot):
    image = np.ones((200, 300, 3), np.uint8) * 255

    # print("Circle: ", circular_obstacle(r, c, [225, 150]))

    for i in range(0, 300):
        for j in range(0, 200):
            # print("For Loop")
            idx = cart2img([i, j])
            # print("Circle: ", circular_obstacle(r, c, [225, 150]))
            if circular_obstacle(radius_rigid_robot, clearance, [idx[0], idx[1]]) == True:
                # print("Circle: ",i,j)
                image[j, i] = (0, 0, 0)

            if ellipsoid_obstacle(radius_rigid_robot, clearance, [idx[0], idx[1]]) == True:
                # print("Circle: ",i,j)
                image[j, i] = (0, 0, 0)

            if rhombus_obstacle(radius_rigid_robot, clearance, [idx[0], idx[1]]) == True:
                # print("Circle: ",i,j)
                image[j, i] = (0, 0, 0)

            if rectangle_obstacle(radius_rigid_robot, clearance, [idx[0], idx[1]]) == True:
                # print("Circle: ",i,j)
                image[j, i] = (0, 0, 0)

            if nonconvex_obstacle_right_half(radius_rigid_robot, clearance, [idx[0], idx[1]]) == True:
                # print("Circle: ",i,j)
                image[j, i] = (0, 0, 0)

            if nonconvex_obstacle_left_half(radius_rigid_robot, clearance, [idx[0], idx[1]]) == True:
                # print("Circle: ", i, j)
                image[j, i] = (0, 0, 0)

            if boundary_obstacle(radius_rigid_robot, clearance, [idx[0], idx[1]]) == True:
                # print("Circle: ", i, j)
                image[j, i] = (0, 0, 0)
            # image[np.where(image==255)]=True
            # image[np.where(image==0)]=False
    return image



def cv2_imshow(resized_new):
    pass


def main():
    image = plot_map(clearance, radius_rigid_robot)

    adjusted_coord_start_node = ([start_node_x, start_node_y])
    adjusted_coord_goal_node = ([goal_node_x, goal_node_y])

    image[adjusted_coord_start_node[1], adjusted_coord_start_node[0]] = (0, 255, 10)
    image[adjusted_coord_goal_node[1], adjusted_coord_goal_node[0]] = (10, 0, 255)

    start_node_position = [start_node_x, start_node_y]
    goal_node_position = [goal_node_x, goal_node_y]

    #find_path_astar(image, start_node_pos, goal_node_pos, clearance, radius_rigid_robot):

    visited_list, parent_child_map, last_node = find_path_astar(image, start_node_position, goal_node_position, clearance,
                                                        radius_rigid_robot, step_size_robot, initial_angle)





    # plot the path:
    fig, ax = plt.subplots()
    plt.grid()
    #
    ax.set_aspect('equal')

    circle = plt.Circle((225,150), radius=25+augment_distance)
    ax.add_patch(circle)

    points = [[225, 40+(augment_distance/0.8575)], [250+(augment_distance/0.5145), 25], [225, 10-(augment_distance/0.8575)], [200-(augment_distance/0.5145), 25]]
    polygon = plt.Polygon(points)
    ax.add_patch(polygon)

    rectangle_points = rectangle_points_find(clearance, radius_rigid_robot, None, None)
    #print([rectangle_points[0][x],rectangle_points[0][y]])

    points = [[rectangle_points[0][x],rectangle_points[0][y]], [rectangle_points[1][x],rectangle_points[1][y]], [rectangle_points[2][x],rectangle_points[2][y]],
              [rectangle_points[3][x], rectangle_points[3][y]]]
    polygon = plt.Polygon(points)
    ax.add_patch(polygon)




    polygon_points = polygon_right_points(clearance, radius_rigid_robot, None, None)
    # print([rectangle_points[0][x],rectangle_points[0][y]])

    points = [[polygon_points[0][x], polygon_points[0][y]], [polygon_points[1][x], polygon_points[1][y]],
              [polygon_points[2][x], polygon_points[2][y]],
              [polygon_points[3][x], polygon_points[3][y]],
              [polygon_points[4][x], polygon_points[4][y]]]
    polygon = plt.Polygon(points)
    ax.add_patch(polygon)

    polygon_points_left = polygon_left_points(clearance, radius_rigid_robot, None, None)
    # print([rectangle_points[0][x],rectangle_points[0][y]])

    points = [[polygon_points_left[0][x], polygon_points_left[0][y]], [polygon_points_left[1][x], polygon_points_left[1][y]],
              [polygon_points_left[2][x], polygon_points_left[2][y]],
              [polygon_points_left[3][x], polygon_points_left[3][y]]]
    polygon = plt.Polygon(points)
    ax.add_patch(polygon)

    ellipse = Ellipse(xy=(150, 100), width=80+(2*augment_distance), height=40+(2*augment_distance))
    ax.add_patch(ellipse)

    #add the left boundary
    points = [[0,0], [0,200],
              [augment_distance,200], [augment_distance,0]]
    polygon = plt.Polygon(points)
    ax.add_patch(polygon)

    # add the top boundary
    points = [[300, 200], [0, 200],[0, 200-augment_distance],
              [300 , 200- augment_distance]]
    polygon = plt.Polygon(points)
    ax.add_patch(polygon)

    # add the lower boundary
    points = [[300, 0], [0, 0], [0, augment_distance-1],
              [300, augment_distance-1]]
    polygon = plt.Polygon(points)
    ax.add_patch(polygon)

    # add the right boundary
    points = [[300, 200], [300, 0], [300 - augment_distance, 0],
              [300-augment_distance, 200]]
    polygon = plt.Polygon(points)
    ax.add_patch(polygon)







    plt.xlim(0, 300)
    plt.ylim(0, 200)

    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'XVID'), 1, (565, 379))

    if visited_list is not None:

        for ind, v in enumerate(visited_list):
            print(ind)
            child_pos = v.position
            if v.parent is not None:
                parent_pos = v.parent.position
                ax.quiver(parent_pos[0], parent_pos[1], child_pos[0]-parent_pos[0], child_pos[1]-parent_pos[1], units='xy', scale=1)
                if ind%3000==0:

                    plt_name = './plots/plot' + str(ind) + '.png'
                    plt.savefig(plt_name, bbox_inches='tight')
                    plot_img = cv2.imread(plt_name)
                    #print('frame', plot_img.shape)
                    out.write(plot_img)

            #image[v[1], v[0]] = (255, 255, 0)
            #resized_new = cv2.resize(image, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
            #cv2_imshow(resized_new)
            #if cv2.waitKey(1) == 27:
            #    break



        trace_path = []

        child_pos = last_node.position
        child_pos_tuple = (child_pos[0], child_pos[1], last_node.angle)
        parent = parent_child_map[child_pos_tuple]
        while parent is not None:
            ax.quiver(parent[0], parent[1], child_pos_tuple[0] - parent[0], child_pos_tuple[1] - parent[1], units='xy', scale=1, color='g')

            #trace_path.append(parent)
            child_pos_tuple = parent
            parent = parent_child_map[parent]

        plt_name = './plots/plot.png'
        plt.savefig(plt_name, bbox_inches='tight')
        plot_img = cv2.imread(plt_name)
        out.write(plot_img)
        out.release()


        fig.show()
        # fig.draw()
        plt.show()
    else:
        print('Cannot find goal.')

    '''
    trace_path.reverse()
    for point in trace_path:
        image[point[1], point[0]] = (200, 0, 200)
        resized_new = cv2.resize(image, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)

    cv2_imshow(resized_new)

    print("Press any key to Quit")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    plt.imshow(image)
    # print(image)
    plt.show()
    '''


if __name__ == "__main__":
    main()


