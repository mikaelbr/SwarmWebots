
from controller import *   # controller comes with Webots
import time                # A Python primitive module
import math                #   "            "
import Image               # An extra Python module (that you'll have to download)
import imagepro            # A module provided by Keith Downing for this assignment

# This is the basic class for controlling an epuck robot in the Webots simulator.  In theory, the
# same code can also run a physical epuck robot with just the "flip of a switch" - although there are small
# differences.  

# The class hierarchy is Robot => DifferentialWheels => epuck_basic, where the superclass, Robot, and
# DifferentialWheels are written by the Webots people, while we defined epuck_basic.  By inheriting
# from epuck_basic, you're controller should have access to basic robot functionality such as:
# a) reading distance sensors, b) viewing camera images from the robot's "eye", c) setting wheel speeds of
# the robot
# Here is the main class of your controller.
# This class defines how to initialize and run your controller.
# Note that this class derives Robot and so inherits all its functions

# When using this code with a neural-network-based controller, you may only need to call
# a small set of the routines defined below, such as:
# run_timestep, set_wheel_speeds, get_proximities, and snapshot


class EpuckBasic (DifferentialWheels):

  max_wheel_speed = 1000
  num_dist_sensors = 8
  encoder_resolution = 159.23 # for wheel encoders
  tempo = 0.5  # Upper velocity bound = Fraction of the robot's maximum velocity = 1000 = 1 wheel revolution/sec  
  wheel_diameter = 4.1 # centimeters
  axle_length = 5.3 # centimeters

# Final 4 slots not used in Webots but included for use with physical epucks that are not driven by Webots.
  max_spin_rate = tempo * (wheel_diameter / axle_length) 
  robot_camera_xres = 40 # Need to save X and Y resolution for the epuck camera
  robot_camera_yres = 40
  timestep_duration = 1 # Real-time seconds per timestep

# Initialization needs to setup the camera and the distance sensors.  The timestep is
# found in the Webots WORLD file associated with an epuck controller.  BE SURE TO CALL THIS or
# something similar in order to get access to camera and sensor data, along with the timestep.

  def basic_setup(self, tempo = 1.0):
      self.timestep = int(self.getBasicTimeStep()) # Fetched from WorldInfo.basicTimeStep (in the Webots world)
      self.tempo = tempo
      self.enableEncoders(self.timestep)
      self.camera = self.getCamera('camera')
      self.camera.enable(4*self.timestep)
      print "Camera width: " , self.camera.getWidth()
      self.dist_sensor_values = [0 for i in range(self.num_dist_sensors)]
      self.dist_sensors = [self.getDistanceSensor('ps'+str(x)) for x in range(self.num_dist_sensors)]  # distance sensors
      map((lambda s: s.enable(self.timestep)), self.dist_sensors) # Enable all distance sensors

 
# **** TIMED ACTION ***

# The routines do_timed_action and run_timestep are explicit commands to the robot to actually DO
# something (i.e. move its wheels) for a given amount of time.  The actual setting of the wheel speeds
# is done via independent calls to routines such as "move" (below).

#  This is a CRITICAL method for "Robot" objects to insure synching of actuators and sensors.
# The parameter in the call to "step" is duration in milliseconds, and it needs to be a multiple of the timestep parameter, hence
# the division by timestep, rounding, and then multiplication by timestep.  The "duration" argument to
# do_timed_action is in SECONDS (hence the multiplication by 1000 prior to rounding in computing ms_second).

  def do_timed_action(self, duration = False):
      if duration:
        ms_duration = int(round(duration*1000/self.timestep)*self.timestep)
      else: ms_duration = self.timestep

      if self.getMode() == 0: # Running the simulator
        self.step(ms_duration)
      else: # Running a real robot
          print "Doing timed robot action"
          self.step(ms_duration)
          self.stop_moving() # I seem to need this to halt the previous action
          self.step(self.timestep)
     # self.stop_moving()
    #  self.wait(duration)
    #  self.stop_moving()

# This gets called by ANNs when they want their associated agent to do it's timestep of activity.  The setting of
# motor values and the reading of sensors are done by other ANN code such that run_timestep just needs to
# activate the bot for a brief period (with the current motor settings in effect).

  def run_timestep(self, cycles = 1):
      for i in range(cycles):
        self.do_timed_action()

  def wait(self, seconds = 1.0):
      print "waiting"
      time.sleep(seconds)
   

# *****  Basic Movement Routines ****

# All movement in an epuck boils down to setting the speeds of the two wheels, nothing more.
# These speeds range from -1000 (one BACKWARD wheel revolution per second) to +1000 (one FORWARD)
# wheel revolution per second.  EpuckBasic includes a "tempo" parameter which denotes the
# fraction of this maximum speed that is permitted.  So when tempo = 0.5, the wheel speeds are
# restricted to the range [-500, 500].  Except for the lowest-level routine, set_wheel_speeds, the
# movement routines simply deal with speeds in the range [-1, 1], which are then scaled to
# actual wheel speeds by set_wheel_speeds prior to it's call to the Webots primitive "setSpeed".


  def forward(self,speed=1.0,duration = 1.0):
      self.move(speed = speed, duration = duration, dir = 'forward')

  def backward(self,speed=1.0,duration = 1.0):
      self.move(speed = speed, duration = duration, dir = 'backward')

# This could have been named "translate", as it causes the robot to
# move forward or backward along a line, but not to turn.
# In the methods MOVE and MOVE_WHEELS, note that the call to set_wheel_speeds does NOT
# cause the robot to move.  It only loads in the wheel-speed values so that they are
# relevant the NEXT TIME the epuck is asked to run a timestep.  We force that
# running via the call to do_timed_action.

  def move(self,speed=1.0,duration =1.0, dir = 'forward'):
      print "Moving"
      s = min(1.0, abs(speed))
      if dir == 'forward':
        self.set_wheel_speeds(left=s,right=s)
      elif dir == 'backward':
          self.set_wheel_speeds(left = -s, right = -s)
          self.do_timed_action(duration)

# A version of move that takes the two wheel speeds (between -1 and 1) as basis.  This
# version permits turning, since both wheel speeds can be specified independently.

  def move_wheels(self, left = 0.0, right = 0.0, duration = 1.0):
      ls = max(-1.0, min(1.0, left)) 
      rs = max(-1.0, min(1.0, right)) 
      self.set_wheel_speeds(left = ls, right = rs)
      self.do_timed_action(duration)

# When running real robots, we occasionally need to explicitly tell the
# robot to stop.

  def stop_moving(self): self.set_wheel_speeds(0,0)

# This is the lowest-level movement method, which calls the Webot's method "setSpeed" with two
# integer values in the range [-1000, 1000] or tighter if "tempo" is smaller than 1.
# The arguments "left" and "right" are in the range [-1,1].

  def set_wheel_speeds(self,left = 0.0, right = 0.0):
      #print "Setting wheel speeds: ", "Left =", left ,"  Right = ", right
      ms = self.tempo*self.max_wheel_speed
      self.setSpeed(int(left*ms),int(right*ms))



# ***** TURNING *********

# Turning involves setting the wheel speeds at different values.  To "turn on a dime" (i.e. turn in place) in, say, the
# clockwise direction, you set the left wheel to a positive value, V, and then the right wheel to the corresponding
# negative value, -V.  The robot will then turn without translating (i.e. without moving forward or
# backward).  To combine forward or backward motion with a turn, set one wheel to spin faster than
# the other, but both can spin in the same direction.

  def turn_left(self): self.spin_angle(90)
  def turn_right(self): self.spin_angle(-90)

# Spin clockwise and counter-clockwise for a specified number of seconds (duration).

  def spin_cw(self,speed=1.0,duration = 1): self.spin(speed=speed, dir = 'cw',duration = duration)
  def spin_ccw(self,speed=1.0,duration = 1): self.spin(speed=speed, dir = 'ccw',duration = duration)

# This causes a spinning motion in either the clockwise or counter-clockwise direction
# for a given length of time.  In earlier versions of this code, we implemented spin_angle (below)
# via calls to this timed-spin method, but now we use the wheel encoders.  So this
# method is now just used as support for the spin_cw and spin_ccw methods
 
  def spin(self, speed = 1.0, dir = 'cw', duration = 1):
      s = int(min(1.0,abs(speed))*self.tempo*self.max_wheel_speed)
      if dir == 'ccw':
        self.set_wheel_speeds(left = -s, right = s)
      elif dir == 'cw':
        self.set_wheel_speeds(left = s, right = -s)
      self.do_timed_action(duration)

# This causes the robot to spin a particular angle, given in degrees with counter-clockwise rotations being
# positive, and clockwise being negative.
# The angle must be converted to "encoder units" of the wheels, of which there are
# RES per radians of wheel rotation, where RES is found in the "encoderResolution" slot of a differentialWheels object,
# from which basic_epuck inherits.  A typical value for RES is around 150. 

  def spin_angle(self, angle):
      a = abs(angle)*math.pi/180.0
      if angle > 0:
        self.set_wheel_speeds(-1.0,1.0)
      else: self.set_wheel_speeds(1.0,-1.0)

      self.setEncoders(0.0,0.0)
      total_units = a * self.encoder_resolution * self.axle_length / self.wheel_diameter
      current = abs(self.getLeftEncoder())
      goal_units = current + total_units

      while current < goal_units:
          self.step(self.timestep)
          current = abs(self.getLeftEncoder())


#  **** SENSORS and CAMERA ****

# This fetches the values of the proximity sensors and returns them in a list.  The sensors need to
# be initialized/fetched before this routine can be run.  This is done in the "Initialize" method near the
# top of the class definitions.

  def get_proximities(self):
      for i in range(self.num_dist_sensors):
          self.dist_sensor_values[i] = self.dist_sensors[i].getValue()
      return self.dist_sensor_values



# This is the high-level routine for getting camera images; just call it directly from your code and
# then prepare to deal with the "Image" object that it returns.  This is where you'll need Python's Image module.
#  The "show" option enables you to have the camera image drawn to a small window on the screen.  This is
# mainly used during debugging.  Webots ALSO presents a camera picture, so you normally don't need snapshot to
# draw the same picture.  But the rendering done by Webots and that done by the image module's SHOW method
# can be a little different, and since snapshot returns the image module's version of the picture, you may want/need
# to look at it.

  def snapshot(self, show = False):
      im = self.get_image()
      if show: im.show()
      return im

# This is the lower-level method that calls Webots code to fetch the camera image (in the form of a big string)
# and then converts the string to an Image object.  

  def get_image(self):
      strImage=self.camera.getImage()
      im = Image.fromstring('RGB',(self.camera.getWidth(), self.camera.getHeight()), strImage)
      return im

# ****** RUN LOOP **********

# You do NOT need to use this particular name (continuous_run), but you'll want to have some sort of
# loop that reads sensors, the camera, etc. and then performs some action.

  def continuous_run(self):
    
    # Main loop
      while True:
        self.turn_left()
        self.get_proximities()
        # self.braitenburg_avoidance()
      
      
        # This runs a simulation step of duration 64 milliseconds (simulation time, not real time).
        # The STEP method returns a -1 when the simulation is over. 
        if self.step(64) == -1: break
    
    # Enter here exit cleanup code

# ****** Accessories ******

# This is just some useful and/or fun stuff
  def testrun(self):
      self.run_toy()
      self.stop_moving()
      

  def braitenburg_avoidance(self):
      sv = self.dist_sensor_values
      sum1 = sv[0] + sv[1] + sv[2] + sv[3]
      sum2 = sv[4] + sv[5] + sv[6] + sv[7]
      tot = sum1 + sum2
      self.set_wheel_speeds(sum1/tot, sum2/tot)

# ***** Running in interpretive mode. *****************  

# When I start up Webots, I do it from a unix terminal shell.  That enables my
# Python path information to be combined with Webot's pathes, PLUS it gives me
# an input buffer into which I can type robot commands when I use the
# run_toy and interp_command methods below.  This "interactive" robot mode is
# just for fun, and not used when controlling a robot via a neural network.

  def interp_command(self,string):
      items = string.split() # Use white space to separate command and each arg
      command = items[0]
      args =[float(item) for item in items[1:]]
      if command == 'quit':
          print "Ending the run."
          return False
      if command == 'forward':
        self.forward(speed = 1.0, duration = args[0])
      elif command == 'backward':
        self.backward(speed = 1.0, duration = args[0])
      elif command == 'left':
        self.turn_left()
      elif command =='right':
        self.turn_right()
      elif command == 'spin':
        self.spin_angle(args[0])
      elif command == 'snap':
        self.snapshot()
      elif command == 'wait':
        self.wait(args[0])
      elif command == 'help':
          help = "\nThe Legal Commands:\n"
          help += "   forward <duration in seconds> - Moves the robot forward.\n"
          help += "   backward <duration in seconds> - Moves the robot backward.\n"
          help += "   right - Turns the robot to the right.\n"
          help += "   left - Turns the robot to the left.\n"
          help += "   spin <angle in degrees> - Spins robot a given angle.\n"
          help += "   snap - Shows the camera image.\n"
          help += "   wait <duration in seconds> - robot does nothing for the specified period \n"
          help += "   quit - Quit this program.\n"
          print help 
      else:
          print "Unknown command"
      return True

# An action script is read from a file and then interpreted, line by line.  Each line will
# correspond to a movement command.  The list of acceptable commands (shown in the big if statement of
# the interp_command method) can easily be extended to reading sensors, taking
# snapshots, etc.

  def run_action_script(self,fid = "action1"):
      path = "data/" + fid + ".dat" 
      lines = load_file_lines(path)
      for l in lines:
        self.interp_command(l)

  def run_toy(self):
      result = True
      print "Enter robot commands.  Type 'help for the command list and 'quit to stop"
      while result:
          print "Command: "
          command = raw_input()
          result = self.interp_command(command)


# *** MAIN ****

# This creates an instance of your EpuckBasic subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.  This code (or something like it) should only appear
# here (uncommented) if this is the HIGHEST-LEVEL epuck controller.  If you create subclass S
# from epuck_basic, then you should include similar code that: a) creates, b) initializes, and c) runs
# your controller at the bottom of the file for S.

#controller = EpuckBasic()
#controller.basic_setup()
#controller.continuous_run()

