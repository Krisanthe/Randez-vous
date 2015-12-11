from controller import *
from controller import Robot
import math
import time


class MyRobot (Robot):
  def run(self):
    rotatingLeft = False
    rotatingRight = False
    speed = 14
    LaserSensor = ['ds_left_front','ds_right_front','ds_back','ds_leftfront','ds_rightfront','ds_left_rear','ds_right_rear']
    Motors = ['wheel1','wheel2','wheel3','wheel4']
    LightSens = ['light sensor front','light sensor right','light sensor left','light sensor back']
    lights = []
    sensor = []
    wheels = []
    before_k = 0;
    before_l = 0;
    k=20
    l=1
    TIME_STEP = 16
    KONIEC = 0
    cnt = 0
    
    nieodwiedzone = 0
    dozwolone = 1
    odwiedzone = 100
    przeszkoda = 30
    array = [] 
    for i in range(20):
      array.append([])
      for j in range(20):
        array[i].append(0)
    
    wagi = []
    for i in range(20):
      wagi.append([])
      for j in range(20):
            wagi[i].append(0)
          
    for i in range(7):
      sensor.append(self.getDistanceSensor(LaserSensor[i]))
      sensor[i].enable(TIME_STEP)
    for i in range(4):
      lights.append(self.getLightSensor(LightSens[i]))
      lights[i].enable(TIME_STEP)
    for i in range(4):
      wheels.append(self.getMotor(Motors[i]))
      wheels[i].setPosition(float('inf'))
    
    compas = self.getCompass('compass')
    compas.enable(TIME_STEP)
    
    gps = self.getGPS('gps')
    gps.enable(TIME_STEP)
    
    def get_bearing_in_degrees():
      temp = compas.getValues()
      rad = math.atan2(temp[0],temp[2])
      bearing = (rad - 1.5708) / math.pi * 180
      if (bearing < 0):
        bearing += 360
      return bearing
      
    def get_new_orientation(angle, turn_side):
      if angle > 175 and angle < 185:
        if turn_side == 'left':
          return 90
        else:
          return 270
      elif angle > 355 or angle < 5:
        if turn_side == 'left':
          return 270
        else:
          return 90
      elif angle > 265 and angle < 275:
        if turn_side == 'left':
          return 180
        else:
          return 0
      elif angle > 85 and angle < 95:
        if turn_side == 'left':
          return 0
        else:
          return 180
      else:
        return 0
      
    def showArray():
      for i in range(20):
        for j in range(20):
          print array[i][j],
        print ''
      print ''
      
    def clearArray():
      for i in range(20):
        for j in range(20):
          array[i][j] = 0
      
    def getPercent():
      cnt = 0
      for i in range(20):
        for j in range(20):
          if array[i][j] != 0:
            cnt += 1
      return 100*cnt/400.0

    def showWeights():
      for i in range(20):
        for j in range(20):
          print wagi[i][j],
        print ''
      print ''
   
    def calcWeights():
      for i in range(20):
        for j in range(20):
          wagi[i][j] = array[i][j]
          if i <= 18:
            wagi[i][j] += array[i+1][j]
          if i >= 1:
            wagi[i][j] += array[i-1][j]
          if j >= 1:
            wagi[i][j] += array[i][j-1]
          if j <= 18:
            wagi[i][j] += array[i][j+1]
          
          
    def wierszFront(wiersz, kat):
      if kat > 265 and kat < 275:
        return int(wiersz-1)
      elif kat > 85 and kat < 95:
        return int(wiersz+1)
      else:
        return wiersz
          
    def kolumnaFront(kolumna, kat):
      if kat > 175 and kat < 185:
        return int(kolumna-1)
      elif kat > 355 or kat < 5:
        return int(kolumna+1)
      else:
        return kolumna

    def wierszLeft(wiersz, kat):
      if kat > 175 and kat < 185:
        return int(wiersz+1)
      elif kat > 355 or kat < 5:
        return int(wiersz-1)
      else:
        return wiersz
               
    def kolumnaLeft(kolumna, kat):
      if kat > 265 and kat < 275:
        return int(kolumna-1)
      elif kat > 85 and kat < 95:
        return int(kolumna+1)
      else:
        return kolumna
        
    def wierszRight(wiersz, kat):
      if kat > 175 and kat < 185:
        return int(wiersz-1)
      elif kat > 355 or kat < 5:
        return int(wiersz+1)
      else:
        return wiersz
               
    def kolumnaRight(kolumna, kat):
      if kat > 265 and kat < 275:
        return int(kolumna+1)
      elif kat > 85 and kat < 95:
        return int(kolumna-1)
      else:
        return kolumna
      
    #KONIEC = 1
    while (self.step(TIME_STEP) != -1):
      ##Zatrzymywanie sie co 600 cykli na 600 cykli##
      cnt+=1
      if cnt >= 600:
        for i in range(4):
              wheels[i].setVelocity(0)
        if cnt == 900:
          cnt = 0
      ##Zatrzymywanie sie co 600 cykli na 600 cykli##
      else:  
    
      # Pobieranie danych z czujnikow

        dis_front_left = sensor[0].getValue()
        dis_front_right = sensor[1].getValue()
        dis_back = sensor[2].getValue()
        dis_left_front = sensor[3].getValue()
        dis_right_front = sensor[4].getValue()
        dis_left_rear = sensor[5].getValue()
        dis_right_rear = sensor[6].getValue()
        
        light_front = lights[0].getValue()
        light_right = lights[1].getValue()
        light_left = lights[2].getValue()
        light_back = lights[3].getValue()
        
        angle = get_bearing_in_degrees()
        coords = gps.getValues() #pobranie wspolrzednych z GPS
        x = round(coords[0],5)
        z = round(coords[2],5)
        k = 19-int(round(4.25*x+9.5)) #wyznaczenie indeksow tablicy
        l = int(round(4.25*z+9.5))
        array[k][l] = odwiedzone;
        percent = getPercent()
        print 'Procent B:', percent
        if percent >= 90:
          print 'osiagnieto 90 procent, eksploracja od poczatku'
          clearArray()
          
        if light_front == 1000 or light_right == 1000 or light_left == 1000 or light_back == 1000: 
          print 'wykrylem',light_front,light_right,light_left
          for i in range(4):
              wheels[i].setVelocity(0)
          KONIEC = 1

            
        
        
   
  
        #relizacja skrecania o 90 st
        if rotatingLeft:
          wheels[0].setVelocity(-0.5)
          wheels[2].setVelocity(-0.5)
          wheels[1].setVelocity(0.5)
          wheels[3].setVelocity(0.5)
          if math.fabs( nowa_orientacja - get_bearing_in_degrees()) < 0.5:
            rotatingLeft = False
            if KONIEC == 1:
              for i in range(4):
                wheels[i].setVelocity(0)
              print 'koniec'
              TIME_STEP = -1
        elif rotatingRight:
          wheels[0].setVelocity(0.5)
          wheels[2].setVelocity(0.5)
          wheels[1].setVelocity(-0.5)
          wheels[3].setVelocity(-0.5)
          if math.fabs( nowa_orientacja - get_bearing_in_degrees()) < 0.5:
            rotatingRight = False
            if KONIEC == 1:
              for i in range(4):
                wheels[i].setVelocity(0)
              print 'koniec'
              TIME_STEP = -1
        else:
          if True: #wypelnianie tablicy rastrowej opisujacej mape
            if (dis_front_left < 2600 or dis_front_right < 2600):
              if wierszFront(k,angle) >= 0 and wierszFront(k,angle) <= 19 and kolumnaFront(l,angle) >= 0 and kolumnaFront(l,angle) <= 19:# and array[wierszFront(k,angle)][kolumnaFront(l,angle)] == 0:
                array[wierszFront(k,angle)][kolumnaFront(l,angle)]  = przeszkoda
            else:
              if wierszFront(k,angle) >= 0 and wierszFront(k,angle) <= 19 and kolumnaFront(l,angle) >= 0 and kolumnaFront(l,angle) <= 19 and array[wierszFront(k,angle)][kolumnaFront(l,angle)] == 0:
                array[wierszFront(k,angle)][kolumnaFront(l,angle)] = dozwolone
            
            if (dis_right_front > 2600 and dis_right_rear > 2600):
              if wierszRight(k,angle) >= 0 and wierszRight(k,angle) <= 19 and kolumnaRight(l,angle) >= 0 and kolumnaRight(l,angle) <= 19 and array[wierszRight(k,angle)][kolumnaRight(l,angle)] == 0:
                array[wierszRight(k,angle)][kolumnaRight(l,angle)]  = dozwolone
            else:
               if wierszRight(k,angle) >= 0 and wierszRight(k,angle) <= 19 and kolumnaRight(l,angle) >= 0 and kolumnaRight(l,angle) <= 19:# and array[wierszRight(k,angle)][kolumnaRight(l,angle)] == 0:
                 array[wierszRight(k,angle)][kolumnaRight(l,angle)] = przeszkoda
                
            if (dis_left_front > 2600 and dis_left_rear > 2600):
              if wierszLeft(k,angle) >= 0 and wierszLeft(k,angle) <= 19  and kolumnaLeft(l,angle) >= 0 and kolumnaLeft(l,angle) <= 19 and array[wierszLeft(k,angle)][kolumnaLeft(l,angle)] == 0:
                array[wierszLeft(k,angle)][kolumnaLeft(l,angle)]  = dozwolone
            else:
                if wierszLeft(k,angle) >= 0 and wierszLeft(k,angle) <= 19 and kolumnaLeft(l,angle) >= 0 and kolumnaLeft(l,angle) <= 19:# and array[wierszLeft(k,angle)][kolumnaLeft(l,angle)] == 0:
                  array[wierszLeft(k,angle)][kolumnaLeft(l,angle)] = przeszkoda    
             
            if False:
              pass
            else:
              calcWeights()
              if wierszFront(k,angle) >= 0 and wierszFront(k,angle) <= 19 and kolumnaFront(l,angle) <= 19 and kolumnaFront(l,angle) >= 0:
                if (dis_front_left > 2600 and dis_front_right > 2600):
                  wagafront = wagi[wierszFront(k,angle)][kolumnaFront(l,angle)]
                else:
                  wagafront = 800;
              else:
                wagafront = 800;
              if wierszRight(k,angle) >= 0 and wierszRight(k,angle) <= 19 and kolumnaRight(l,angle) <= 19 and kolumnaRight(l,angle) >= 0:
                if (dis_right_front > 2600 and dis_right_rear > 2600):
                  wagaright = wagi[wierszRight(k,angle)][kolumnaRight(l,angle)]
                else:
                  wagaright = 800;              
              else:
                wagaright = 800;
              if wierszLeft(k,angle) >= 0 and wierszLeft(k,angle) <= 19 and kolumnaLeft(l,angle) <= 19 and kolumnaLeft(l,angle) >= 0:
                if (dis_left_front > 2600 and dis_left_rear > 2600):
                   wagaleft = wagi[wierszLeft(k,angle)][kolumnaLeft(l,angle)]
                else:
                  wagaleft = 800;             
              else:
                wagaleft = 800;
             
              #print 'WagaFront:',wagafront
              #print 'WagaLeft:',wagaleft
              #print 'WagaRight:',wagaright
              
              if wagafront <= wagaright and wagafront <= wagaleft and wagafront < 800:
                pass
              elif wagaright <= wagaleft:#wagaleft <= wagaright:
                nowa_orientacja = get_new_orientation(get_bearing_in_degrees(), 'right')
                rotatingRight = True
              else: #wagaright <= wagaleft:              
                nowa_orientacja = get_new_orientation(get_bearing_in_degrees(), 'left')
                rotatingLeft = True
  
            
                  
            for i in range(4):
              wheels[i].setVelocity(speed)
            
          if KONIEC == 1:
            for i in range(4):
              wheels[i].setVelocity(0)
            print 'koniec'
            TIME_STEP = -1
        
    # Enter here exit cleanup code

robot = MyRobot()
robot.run()