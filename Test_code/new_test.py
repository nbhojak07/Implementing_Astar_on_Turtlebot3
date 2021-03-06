# -*- coding: utf-8 -*-

import numpy as np
import math
import operator
#import obstacle_map
import cv2
# from google.colab.patches import cv2_imshow

visited = np.zeros((600, 400, 12))

def cart2img(adjust_coord):
    return [adjust_coord[0], 200 - adjust_coord[1]]


def find_line_slope_and_intercept(test_point_coord, line_point_1, line_point_2):
    slope = (line_point_2[1] - line_point_1[1]) / (line_point_2[0] - line_point_1[0])
    intercept = line_point_1[1] - (slope * line_point_1[0])
    # print(slope,intercept)
    return slope, intercept


# function returns false when the point is outside the circle
def circular_obstacle(clearance, radius_rigid_robot, test_point_coord):
    circle_center = (225, 150)
    test_point_coord_x = test_point_coord[0]
    test_point_coord_y = test_point_coord[1]
    augment_distance = radius_rigid_robot + clearance

    distance_from_center = ((test_point_coord_x - circle_center[0]) ** 2 + (
                test_point_coord_y - circle_center[1]) ** 2) ** 0.5

    if distance_from_center > (25 + augment_distance):
        return False
    else:
        return True


# function returns false when the point is outside the ellipse
def ellipsoid_obstacle(clearance, radius_rigid_robot, test_point_coord):
    ellipsoid_center = (150, 100)
    test_point_coord_x = test_point_coord[0]
    test_point_coord_y = test_point_coord[1]
    augment_distance = radius_rigid_robot + clearance
    semi_major_axis = 40
    semi_minor_axis = 20

    distance_from_center = ((test_point_coord_x - ellipsoid_center[0]) ** 2) / (
                (semi_major_axis + augment_distance) ** 2) + (test_point_coord_y - ellipsoid_center[1]) ** 2 / (
                                       (semi_minor_axis + augment_distance) ** 2)

    if distance_from_center > 1:
        return False
    else:
        return True


def rectangle_obstacle(clearance, radius_rigid_robot, test_point_coord):
    circle_center = (225, 150)
    augment_distance = radius_rigid_robot + clearance

    rectangle_point_1 = [100, 38.66025]
    rectangle_point_2 = [35.0481, 76.1603]
    rectangle_point_3 = [30.0481, 67.5]
    rectangle_point_4 = [95, 30]

    # We set the flags by testing for image point inside the rectangle
    # Because the sign for the half plane is unique for every line, we test it by using image point that is confirmed to be inside the rectangle
    edge1_m_c = find_line_slope_and_intercept(test_point_coord, rectangle_point_1, rectangle_point_2)
    line1 = test_point_coord[1] - (edge1_m_c[0] * test_point_coord[0]) - (
                edge1_m_c[1] + (augment_distance * 2 / (3 ** 0.5)))
    # print(line1)
    if line1 >= 0:
        flag1 = False
        # print("False")
    else:
        flag1 = True
        # print("True")

    edge2_m_c = find_line_slope_and_intercept(test_point_coord, rectangle_point_2, rectangle_point_3)
    line2 = test_point_coord[1] - (edge2_m_c[0] * test_point_coord[0]) - (edge2_m_c[1] + (augment_distance * 2))
    # print(line2)
    if line2 >= 0:
        flag2 = False
        # print("False")
    else:
        flag2 = True
        # print("True")

    edge3_m_c = find_line_slope_and_intercept(test_point_coord, rectangle_point_3, rectangle_point_4)
    line3 = test_point_coord[1] - (edge3_m_c[0] * test_point_coord[0]) - (
                edge3_m_c[1] - (augment_distance * 2 / (3 ** 0.5)))
    # print(line3)
    if line3 >= 0:
        flag3 = True
        # print("True")
    else:
        flag3 = False
        # print("False")

    edge4_m_c = find_line_slope_and_intercept(test_point_coord, rectangle_point_4, rectangle_point_1)
    line4 = test_point_coord[1] - (edge4_m_c[0] * test_point_coord[0]) - (edge4_m_c[1] - (augment_distance * 2))
    # print(line4)
    if line4 >= 0:
        flag4 = True
        # print("True")
    else:
        flag4 = False
        # print("False")

    if flag1 and flag2 and flag3 and flag4:
        return True
    else:
        return False


def rhombus_obstacle(clearance, radius_rigid_robot, test_point_coord):
    augment_distance = radius_rigid_robot + clearance

    rhombus_point_1 = [250, 25]
    rhombus_point_2 = [225, 40]
    rhombus_point_3 = [200, 25]
    rhombus_point_4 = [225, 10]

    # We set the flags by testing for image point inside the rectangle
    # Because the sign for the half plane is unique for every line, we test it by using image point that is confirmed to be inside the rectangle
    edge1_m_c = find_line_slope_and_intercept(test_point_coord, rhombus_point_1, rhombus_point_2)
    line1 = test_point_coord[1] - (edge1_m_c[0] * test_point_coord[0]) - (edge1_m_c[1] + (augment_distance / 0.8575))
    # print(line1)
    if line1 >= 0:
        flag1 = False
    else:
        flag1 = True

    edge2_m_c = find_line_slope_and_intercept(test_point_coord, rhombus_point_2, rhombus_point_3)
    line2 = test_point_coord[1] - (edge2_m_c[0] * test_point_coord[0]) - (edge2_m_c[1] + (augment_distance / 0.8575))
    # print(line2)
    if line2 >= 0:
        flag2 = False
    else:
        flag2 = True

    edge3_m_c = find_line_slope_and_intercept(test_point_coord, rhombus_point_3, rhombus_point_4)
    line3 = test_point_coord[1] - (edge3_m_c[0] * test_point_coord[0]) - (edge3_m_c[1] - (augment_distance / 0.8575))
    # print(line3)
    if line3 >= 0:
        flag3 = True
    else:
        flag3 = False

    edge4_m_c = find_line_slope_and_intercept(test_point_coord, rhombus_point_4, rhombus_point_1)
    line4 = test_point_coord[1] - (edge4_m_c[0] * test_point_coord[0]) - (edge4_m_c[1] - (augment_distance / 0.8575))
    # print(line4)
    if line4 >= 0:
        flag4 = True
    else:
        flag4 = False

    if flag1 and flag2 and flag3 and flag4:
        return True
    else:
        return False


def nonconvex_obstacle_right_half(clearance, radius_rigid_robot, test_point_coord):
    augment_distance = radius_rigid_robot + clearance

    nonconvex_point_1 = [100, 150]
    nonconvex_point_2 = [75, 185]
    nonconvex_point_3 = [60, 185]
    nonconvex_point_4 = [50, 150]
    nonconvex_point_5 = [75, 120]

    # We set the flags by testing for image point inside the rectangle
    # Because the sign for the half plane is unique for every line, we test it by using image point that is confirmed to be inside the nonconvex_obstacle
    edge1_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_1, nonconvex_point_2)
    line1 = test_point_coord[1] - (edge1_m_c[0] * test_point_coord[0]) - (edge1_m_c[1] + (augment_distance / 0.58124))
    # print(line1)
    if line1 >= 0:
        flag1 = False
        # print("False")
    else:
        flag1 = True
        # print("True")

    edge2_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_2, nonconvex_point_3)
    line2 = test_point_coord[1] - (edge2_m_c[0] * test_point_coord[0]) - (edge2_m_c[1] + (augment_distance / 1))
    # print(line2)
    if line2 >= 0:
        flag2 = False
        # print("False")
    else:
        flag2 = True
        # print("True")

    # edge 3 is not augmented with clearance+robot_radius since its inside the nonconvex polygon
    edge3_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_3, nonconvex_point_4)
    line3 = test_point_coord[1] - (edge3_m_c[0] * test_point_coord[0]) - (edge3_m_c[1] + (augment_distance / 0.27472))
    # print(line3)
    if line3 >= 0:
        flag3 = False
        # print("False")
    else:
        flag3 = True
        # print("True")

    edge4_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_4, nonconvex_point_5)
    line4 = test_point_coord[1] - (edge4_m_c[0] * test_point_coord[0]) - (edge4_m_c[1] - (augment_distance / 0.64018))
    # print(line4)
    if line4 >= 0:
        flag4 = True
        # print("True")
    else:
        flag4 = False
        # print("False")

    edge5_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_5, nonconvex_point_1)
    line5 = test_point_coord[1] - (edge5_m_c[0] * test_point_coord[0]) - (edge5_m_c[1] - (augment_distance / 0.640184))
    # print(line4)
    if line5 >= 0:
        flag5 = True
        # print("True")
    else:
        flag5 = False
        # print("False")

    if flag1 and flag2 and flag3 and flag4 and flag5:
        return True
    else:
        return False


def nonconvex_obstacle_left_half(clearance, radius_rigid_robot, test_point_coord):
    augment_distance = radius_rigid_robot + clearance

    nonconvex_point_1 = [50, 150]
    nonconvex_point_2 = [60, 185]
    nonconvex_point_3 = [25, 185]
    nonconvex_point_4 = [20, 120]

    # We set the flags by testing for image point inside the rectangle
    # Because the sign for the half plane is unique for every line, we test it by using image point that is confirmed to be inside the nonconvex_obstacle
    edge1_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_1, nonconvex_point_2)
    line1 = test_point_coord[1] - (edge1_m_c[0] * test_point_coord[0]) - (edge1_m_c[1] - (augment_distance / 0.27472))
    # print(line1)
    if line1 >= 0:
        flag1 = True
        # print("True")
    else:
        flag1 = False
        # print("False")

    edge2_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_2, nonconvex_point_3)
    line2 = test_point_coord[1] - (edge2_m_c[0] * test_point_coord[0]) - (edge2_m_c[1] + (augment_distance / 1))
    # print(line2)
    if line2 >= 0:
        flag2 = False
        # print("False")
    else:
        flag2 = True
        # print("True")

    # edge 3 is not augmented with clearance+robot_radius since its inside the nonconvex polygon
    edge3_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_3, nonconvex_point_4)
    line3 = test_point_coord[1] - (edge3_m_c[0] * test_point_coord[0]) - (edge3_m_c[1] + (augment_distance / 0.0767))
    # print(line3)
    if line3 >= 0:
        flag3 = False
        # print("False")
    else:
        flag3 = True
        # print("True")

    edge4_m_c = find_line_slope_and_intercept(test_point_coord, nonconvex_point_4, nonconvex_point_1)
    line4 = test_point_coord[1] - (edge4_m_c[0] * test_point_coord[0]) - (edge4_m_c[1] - (augment_distance / 0.7071))
    # print(line4)
    if line4 >= 0:
        flag4 = True
        # print("True")
    else:
        flag4 = False
        # print("False")

    if flag1 and flag2 and flag3 and flag4:
        return True
    else:
        return False


def boundary_obstacle(clearance, radius_rigid_robot, test_point_coord):
    augment_distance = radius_rigid_robot + clearance
    x = test_point_coord[0]
    y = test_point_coord[1]

    if 0 <= x < augment_distance:
        return True
    elif (299 - augment_distance) < x <= 299:
        return True
    elif 0 <= y < augment_distance:
        return True
    elif (199 - augment_distance) < y <= 199:
        return True
    else:
        return False

def test_point_obstacle_check(clearance, radius_rigid_robot, test_point_coord):
    test_point_coord = cart2img(test_point_coord)
    if circular_obstacle(clearance, radius_rigid_robot, test_point_coord):
        return True
    elif ellipsoid_obstacle(clearance, radius_rigid_robot, test_point_coord):
        return True
    elif rectangle_obstacle(clearance, radius_rigid_robot, test_point_coord):
        return True
    elif rhombus_obstacle(clearance, radius_rigid_robot, test_point_coord):
        return True
    elif nonconvex_obstacle_right_half(clearance, radius_rigid_robot, test_point_coord):
        return True
    elif nonconvex_obstacle_left_half(clearance, radius_rigid_robot, test_point_coord):
        return True
    elif boundary_obstacle(clearance, radius_rigid_robot, test_point_coord):
        return True
    else:
        return False

def check_inputs_wrt_obstacles(start_node_x, start_node_y, goal_node_x, goal_node_y):
    if test_point_obstacle_check(clearance, radius_rigid_robot, [start_node_x, start_node_y]):
        print("Start node is inside an obstacle. Enter some other coordinates. Restart program!")
        exit(0)

    if test_point_obstacle_check(clearance, radius_rigid_robot, [goal_node_x, goal_node_y]):
        print("Goal node is inside an obstacle. Enter some other coordinates. Restart program!")
        exit(0)

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


# def isValidNode(map_,x,y,rad):
#     rows,cols = map_.shape[:2]
#     if 0 <= x-rad and x+rad < rows and 0 <= y-rad and y+rad < cols:
#         if not detectCollision(map_, (x,y), rad):
#             return True
#         else :
#             return False
#     else:
#         return False


# def detectCollision(img, center,radius):
#     for i in range(2*radius+1):
#         for j in range(2*radius+1):
#             if i**2+j**2 <= radius**2:
#                 if not ((img[int(center[0])+i][int(center[1])+j]==(255,255,255)).all() and (img[int(center[0])+i][int(center[1])-j]==(255,255,255)).all()\
#                         and (img[int(center[0])-i][int(center[1])-j]==(255,255,255)).all() and (img[int(center[0])-i][int(center[1])+j]==(255,255,255)).all()):
#                     return True
#     return False


def heu(node1, node2):
  dist= math.sqrt( (node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)
  return dist


def move_along(node):
  cost = node[1]
  point = node[0]
  print("Point going inside move_along function", point)
  print("Cost going inside move_along function", cost)
  temp= [0,0,0]
  angle = math.radians((point[2]+ 0)%360)
  temp[0] = point[0] + step_size_robot* math.cos(angle)
  temp[1] = point[1] + step_size_robot* math.sin(angle)
  temp[2] = (point[2]+ 0)%360
  cost_g = cost + 1
  cost_h = heu(temp, goal)
  cost_est = cost_g + cost_h
  if test_point_obstacle_check(clearance,radius_rigid_robot, temp)==False:
     temp1= list(np.around([temp[0], temp[1]], decimals=1))
     temp[0]= temp1[0]
     temp[1]= temp1[1]
     return (temp, cost_est)
  else:
    return None

def move_UP1(node):
  cost = node[1]
  point = node[0]
  temp= [0,0,0]
  angle = math.radians((point[2]+ 30)%360)
  temp[0] = point[0] + step_size_robot* math.cos(angle)
  temp[1] = point[1] + step_size_robot* math.sin(angle)
  temp[2] = (point[2]+ 30)%360
  cost_g = cost + 1.3
  cost_h = heu(temp, goal)
  cost_est = cost_g + cost_h
  if test_point_obstacle_check(clearance,radius_rigid_robot, temp)==False:
     temp1= list(np.around([temp[0], temp[1]], decimals=1))
     temp[0]= temp1[0]
     temp[1]= temp1[1]
     return (temp, cost_est)
  else:
    return None
  
  
def move_UP2(node):
  cost= node[1]
  point = node[0]
  temp= [0,0,0]
  angle = math.radians((point[2]+ 60)%360)
  temp[0] = point[0] + step_size_robot* math.cos(angle)
  temp[1] = point[1] + step_size_robot* math.sin(angle)
  temp[2] = (point[2]+ 60)%360
  cost_g = cost + 1.5
  cost_h = heu(temp, goal)
  cost_est = cost_g + cost_h
  if test_point_obstacle_check(clearance,radius_rigid_robot, temp)==False:
     temp1= list(np.around([temp[0], temp[1]], decimals=1))
     temp[0]= temp1[0]
     temp[1]= temp1[1]
     return (temp, cost_est)
  else:
    return None


def move_DN1(node):
  cost = node[1]
  point = node[0]
  temp= [0,0,0]
  angle = math.radians((point[2]- 30)%360)
  temp[0] = point[0] + step_size_robot* math.cos(angle)
  temp[[  temp[1] = point[1] + step_size_robot* math.sin(angle)
1] ==== point[1] + step_size_robot* math.sin(angle)
  =temp[2] = (point[2]- 30)%360
  cost_g = cost + 1.3
  cost_h = heu(temp, goal)
  cost_est = cost_g + cost_h
  if test_point_obstacle_check(clearance,radius_rigid_robot, temp)==False:
     temp1= list(np.around([temp[0], temp[1]], decimals=1))
     temp[0]= temp1[0]
     temp[1]= temp1[1]
     return (temp, cost_est)
  else:
    return None

def move_DN2(node):
  cost = node[1]
  point = node[0]
  temp= [0,0,0]
  angle = math.radians((point[2]- 60)%360)
  temp[0] = point[0] + step_size_robot* math.cos(angle)
  temp[1] = point[1] + step_size_robot* math.sin(angle)
  temp[2] = (point[2]- 60)%360
  cost_g = cost + 1.5
  cost_h = heu(temp, goal)
  cost_est = cost_g + cost_h
  if test_point_obstacle_check(clearance,radius_rigid_robot, temp)==False:
     temp1= list(np.around([temp[0], temp[1]], decimals=1))
     temp[0]= temp1[0]
     temp[1]= temp1[1]
     return (temp, cost_est)
  else:
    return None
  


def generate_child(node):
  child= []
  child.append(node)
  parent= []
  i=0
  
  nd = move_along( child[i])
  if nd is not None:
    ndx = nd[0]
    if nd not in child:
      if visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)]==0:
        child.append(nd)
        visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] = 1



  nd = move_UP1(child[i])
  if nd is not None:
    ndx = nd[0]
    if nd not in child:
      if visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] == 0:
          child.append(nd)
          visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] = 1
        

  nd = move_UP2(child[i])
  if nd is not None:
    ndx = nd[0]
    if nd not in child:
      if visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] == 0:
          child.append(nd)
          visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] = 1
        

  nd = move_DN1(child[i])
  if nd is not None:
    ndx = nd[0]
    if nd not in child:
      if visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] == 0:
          child.append(nd)
          visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] = 1


  nd = move_DN2(child[i])
  if nd is not None:
    ndx = nd[0]
    if nd not in child:
      if visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] == 0:
          child.append(nd)
          visited[int(ndx[0] / 0.5)][int(ndx[1] / 0.5)][int(ndx[2] / 30)] = 1

  child.pop(0)
  #parent.append(child[i])
  return child

def explored_all(node, goal):
  explored_nodes=[]
  explored_nodes.append(node)
  parent = []
  parent_child = []

  while len(explored_nodes)>0:

    c1= explored_nodes[0]
    print("First element of explored node is:", c1)
    c2= generate_child(c1)
    #print(c2)
    explored_nodes.pop(0)
    print(explored_nodes)
    for item in c2:
      explored_nodes.append(item)
    explored_nodes.sort(key= operator.itemgetter(1))
    print(explored_nodes)
    target = check_goal(explored_nodes[0], goal)
    if target == True:
      print("goal found!")
      break;


        # all_nodes = [item, c1]
        # parent.append(all_nodes)
        # for v in explored_nodes:
        #     image[int(v[1]), int(v[0])] = (0, 0, 255)
        # #   # return image

  return explored_nodes


def check_goal(c1, goal):
  element = c1[0]
  print("Extracting the first element of tuple: ",element)
  if (((element[0]- goal[0])**2)+ ((element[1] - goal[1])**2)) <= (1.5)**2:
    return True
  else: 
    return False



print("Enter the start node co-ordinates")
start_node_x= int(input("x is: "))
start_node_y= int(input("y is: "))

print("Enter the goal node co-ordinates")
goal_node_x= int(input("x is: "))
goal_node_y= int(input("y is: "))

step_size_robot = int(input("Enter the step size of movement of the robot: "))
if (step_size_robot < 1 and step_size_robot > 10):
    print("Step_size_robot is out of range. Enter step_size_robot from [0,10]. Restart program!")
    exit(0)

print("Enter the initial angle for the robot:  ")
theta_i = int(input("theta_i is: "))

print("Enter the robot parameters:")
radius_rigid_robot = int(input("Enter the radius of the robot: "))
clearance = int(input("Enter the robot clearance: "))

image = plot_map(clearance, radius_rigid_robot)

if (start_node_x < 0 and start_node_x > 300) and (goal_node_x < 0 and goal_node_x > 300):
    print("X coordinate is out of range. Enter x from [0,300]. Restart program!")
    exit(0)

if (start_node_y < 0 and start_node_y > 200) and (goal_node_y < 0 and goal_node_y > 200):
    print("Y coordinate is out of range. Enter y from [0,200]. Restart program!")
    exit(0)

check_inputs_wrt_obstacles(start_node_x, start_node_y, goal_node_x, goal_node_y)

# start_node_y= 200-start_node_y
# goal_node_y= 200-goal_node_y

cost=0
start=([start_node_x, start_node_y, theta_i], cost)
goal= [goal_node_x, goal_node_y]


# c = generate_child(start)
# print(c)

explored_all(start, goal)


# parent_child, image1 = explored_all(start, goal)
# print(parent_child)