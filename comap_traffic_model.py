from random import *
 
def ini_Traf(numberOfCars, spacing, initialposition, initialnumber): #Initial Traffic for a lane
    IC_list = []
    for car in xrange(numberOfCars):
        carName = "Car"+str(initialnumber+car+1)
        maxSpeed = 65 + randint(0,15)
        position = initialposition + car*spacing
        currentSpeed = randint(85*maxSpeed/100,95*maxSpeed/100)
        moreSpaces = currentSpeed
        IC_list.append([carName,maxSpeed,position,currentSpeed,moreSpaces,False])
    return IC_list #[carName,maxSpeed,position,currentSpeed, moreSpaces, currentcar]
 
def printk(TrafficInfo,parameter): #prints traffic info readably
    for lane in TrafficInfo:
        currentlane = []
        for car in lane:
            currentlane.append([car[0],car[parameter]])
        print
        print currentlane
 
def printk2(TrafficInfo,parameter,parameter2): #prints traffic info readably
    for lane in TrafficInfo:
        currentlane = []
        for car in lane:
            currentlane.append([car[0],car[parameter],car[parameter2]])
#        print
        print currentlane
 
def i_trafficList(number_of_lanes, number_of_cars, spacing): #initial traffic list (time = 0)
    IC_list = []
    for lane in xrange(number_of_lanes):
        IC_list.append(ini_Traf(number_of_cars, spacing, 2*(lane+1 % 2),number_of_cars*lane))
    return IC_list
 
def STL(laneList): #Sorts Traffic List
    return sorted(laneList,key=lambda cI:float(cI[2]))
 
def find_true_car_lane(lane):
    for car in xrange(len(lane)):
        if lane[car][5]:
            return car
             
def car_is_in_this_lane(lane):
    for car in xrange(len(lane)):
        if lane[car][5]:
            return True
    return False
 
def find_true_car(TrafficList):
    for lane in xrange(len(TrafficList)):
        if car_is_in_this_lane(TrafficList[lane]):
            location = TrafficList[lane][find_true_car_lane(TrafficList[lane])][2]
            position = find_true_car_lane(TrafficList[lane])
            return [lane, location, position]
    return "car is not in any lanes"
 
def next_car(traffic_list): #finds the next car in each lane, based on true car
    ftc = find_true_car(traffic_list)
    true_car_location = ftc[1]
    true_car_maxSpeed = traffic_list[ftc[0]][ftc[2]][1]
    next_car_list = []
    for lane in traffic_list:
        try:
            farthest_car = lane[-1][2] #location of farthest car in lane
            if true_car_location >= farthest_car:
                next_car_list.append(true_car_location+true_car_maxSpeed+1)
            else:
                for car in lane:
                    if car[2] > true_car_location:
                        next_car_list.append(car[2])
                        break
        except:
            next_car_list.append(true_car_location+true_car_maxSpeed+1)
    return next_car_list
def there_is_a_car_in_this_position(lane,location):
    for car in lane:
        if car[2] == location:
            return True
    return False
def allowed_switch_up(traffic_list):
    ftc = find_true_car(traffic_list)
    permitted_lanes = []
    for lane in xrange(ftc[0]+1,len(traffic_list)):
        if not there_is_a_car_in_this_position(traffic_list[lane],ftc[1]):
            permitted_lanes.append(lane)
        else:
            return permitted_lanes
    return permitted_lanes
     
def allowed_switch_down(traffic_list):
    ftc = find_true_car(traffic_list)
    permitted_lanes = []
    for lane in range(ftc[0])[::-1]:
        if not there_is_a_car_in_this_position(traffic_list[lane],ftc[1]):
            permitted_lanes.append(lane)
        else:
            return permitted_lanes
    return permitted_lanes
     
def allowed_switch(traffic_list):
    ftc = find_true_car(traffic_list)
    legal_lanes = [ftc[0]]
    for lane in allowed_switch_up(traffic_list):
        legal_lanes.append(lane)
    for lane in allowed_switch_down(traffic_list):
        legal_lanes.append(lane)
    return sorted(legal_lanes)
 
def every_car(traffic_list): #returns names of cars sorted by position
    car_list = []
    name_list = []
    for lane in traffic_list:
        for car in lane:
            car_list.append(car)
    for car in STL(car_list)[::-1]:
        name_list.append(car[0])
    return name_list
 
def mark_car_name_true(traffic_list,car_name):
    for lane in traffic_list:
        for car in lane:
            if car[0] == car_name:
                car[5] = True
                return traffic_list
def mark_car_name_false(traffic_list,car_name):
    for lane in traffic_list:
        for car in lane:
            if car[0] == car_name:
                car[5] = False
                return traffic_list
def pick_lane(traffic_list):
    ftc = find_true_car(traffic_list)
    next_car_list = []
    true_car_location = ftc[1]
    true_car_currentSpeed = traffic_list[ftc[0]][ftc[2]][3]
    legal_lanes = allowed_switch(traffic_list)
    for lane in legal_lanes:
        ncv = next_car(traffic_list)[lane] #next car value, by lane
        next_car_list.append(ncv)
        if ncv > true_car_location + true_car_currentSpeed:
            return lane
    for lane in legal_lanes:
        ncv = next_car(traffic_list)[lane]
        if ncv == max(next_car_list):
            return lane
             
def switch_to_lane(traffic_list):
    ftc = find_true_car(traffic_list)
    currentLane = ftc[0]
    carIndex = ftc[2]
    newLane = pick_lane(traffic_list)
    traffic_list[newLane].append(traffic_list[currentLane][carIndex])
    traffic_list[currentLane].pop(carIndex)
    traffic_list[newLane] = STL(traffic_list[newLane])
    return traffic_list
     
def move_car_forward(traffic_list):
    ftc = find_true_car(traffic_list)
    true_car_location = ftc[1]
    true_car_currentSpeed = traffic_list[ftc[0]][ftc[2]][3]
    currentLane = ftc[0]
    carIndex = ftc[2]
    if true_car_location + true_car_currentSpeed < next_car(traffic_list)[ftc[0]]:
        traffic_list[ftc[0]][ftc[2]][2] += traffic_list[ftc[0]][ftc[2]][3]
    else:
        distance_between_cars = next_car(traffic_list)[ftc[0]]-ftc[1]
        traffic_list[ftc[0]][ftc[2]][2] += (distance_between_cars - 1)
    return traffic_list

def change_speed0(traffic_list):
    ftc = find_true_car(traffic_list)
    currentSpeed = traffic_list[ftc[0]][ftc[2]][3]
    if currentSpeed < 4:
        acceleration = choice([0,0,1,1,2])
    elif currentSpeed > 5:
        acceleration = choice([0,0,-1,-1,-2])
    else:
        acceleration = choice([-1,0,0,1])
    maxSpeed = traffic_list[ftc[0]][ftc[2]][1]
    if currentSpeed + acceleration <= maxSpeed and currentSpeed + acceleration >= 0:
        traffic_list[ftc[0]][ftc[2]][3] += acceleration
    return traffic_list

def change_speed(traffic_list):
    ftc = find_true_car(traffic_list)
    currentSpeed = traffic_list[ftc[0]][ftc[2]][3]
    max_speed = traffic_list[ftc[0]][ftc[2]][1]
    there_is_a_car_in_front = False
    try:
        if traffic_list[ftc[0]][ftc[2]+1][2]-traffic_list[ftc[0]][ftc[2]][2] == 1:
            there_is_a_car_in_front = True
    except:
        there_is_a_car_in_front = False
    if currentSpeed < (0.8*max_speed):
        if not there_is_a_car_in_front:
            acceleration = choice([0,2,5,10])
        else:
            acceleration = choice([0,0,-1])
    elif currentSpeed > (0.9*max_speed):
        if there_is_a_car_in_front:
            acceleration = choice([0,0,-2,-5,-10])
        else:
            acceleration = choice([2,0,-2,-5,-10])
    else:
        if there_is_a_car_in_front:
            acceleration = choice([-5,-3,0,0])
        else:
            acceleration = choice([-2,0,0,2])
    maxSpeed = traffic_list[ftc[0]][ftc[2]][1]
    if currentSpeed + acceleration <= maxSpeed and currentSpeed + acceleration >= 0:
        traffic_list[ftc[0]][ftc[2]][3] += acceleration
    return traffic_list
 
def switch_to_rightmost_lane(traffic_list):
    ftc = find_true_car(traffic_list)
    currentLane = ftc[0]
    carIndex = ftc[2]
    newLane = smallest_lane = allowed_switch(itl)[0]
    traffic_list[newLane].append(traffic_list[currentLane][carIndex])
    traffic_list[currentLane].pop(carIndex)
    traffic_list[newLane] = STL(traffic_list[newLane])
    return traffic_list
 
def true_and_move(traffic_list):
    for car_name in every_car(traffic_list):
        mark_car_name_true(traffic_list,car_name)
        switch_to_lane(traffic_list)
        move_car_forward(traffic_list)
        switch_to_rightmost_lane(traffic_list)
        change_speed(traffic_list)
        mark_car_name_false(traffic_list,car_name)
 
def ECP(traffic_list): #returns names of cars sorted by position
    #Every Car's Position
    pos_list = []
    for lane in traffic_list:
        for car in lane:
            pos_list.append(car[2])
    return list(set(pos_list))
 
def ECP2(lane): #returns names of cars sorted by position
    pos_list = []
    for car in lane:
        pos_list.append(car[2])
    return pos_list
 
def removespaces(somestring): #removes leading spaces
    counter = 0
    for index in range(len(somestring)):
        if somestring[index] == " ":
            counter += 1
        else:
            return somestring[counter:]
    return ""
 
def cropstring(string,length): #crops string to some length
    if len(string)>length:
        return string[:length]
    else:
        return string
 
def ex_and_oh(lane): #represents a lane as exes and ohs, starting from the first car
    pos_list = ECP2(lane)
    maximum = pos_list[-1]
    empty_list = [" "] * maximum
    for position in pos_list:
        empty_list[position-1] = "X"
    return ''.join(cropstring(removespaces(empty_list),2**10))
 
def ex_and_oh2(traffic_list):
    list_of_pos_list = []
    for lane in traffic_list:
        list_of_pos_list.append(ex_and_oh(lane))
    return list_of_pos_list

def ex_and_oh3(pos_list): #represents a lane as exes and ohs, starting from the first car
    maximum = sorted(pos_list)[-1]
    empty_list = [" "] * maximum
    for position in pos_list:
        try:
            empty_list[position-1] = "X"
        except:
            print len(empty_list)
            print ECP(itl)
    return ''.join(cropstring(removespaces(empty_list),2**10))
 
#find_true_car(TrafficList) --> [lane, location, position]
 
#[carName,maxSpeed,position,currentSpeed, moreSpaces, currentcar]
 
def location_sum(traffic_list):
    loc_sum = 0
    for car_name in every_car(traffic_list):
        mark_car_name_true(traffic_list,car_name)
        loc_sum += find_true_car(traffic_list)[1]
        mark_car_name_false(traffic_list,car_name)
    return loc_sum      
 
def run_simulation(traffic_list, steps):
    print ex_and_oh3(ECP(itl))
    for x in range(steps):
        true_and_move(itl)
        print ex_and_oh3(ECP(itl))

itl = i_trafficList(3, 40, 5)
#print "-->", 
run_simulation(itl,200)
#printk(itl,2)
