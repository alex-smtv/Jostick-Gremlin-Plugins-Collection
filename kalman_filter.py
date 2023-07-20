import gremlin
from gremlin.user_plugin import *

class KalmanFilter():
    def __init__(self, process_noise, sensor_noise, estimated_error, radius = None, delay_radius_count = 1):
        """
            Kalman Filter adapted for dynamic movement. 
            
            When localized around a point the kalman filter is applied to smooth out the jitters.
            When moving out of the localized point the kalman filter is deactivated and activated back when the dynamic movement stops to a new localized point.

            The radius defines how big the area around the localized point is considered for the kalman filter to apply.
            
            The estimated_error of the model will be adjusted during the process.

            The process_noice accounts for deviation from the motion model.
            A low process noise may cause the filter to ignore rapid deviations from the true trajectory and instead favor the motion model.
            A high process noise admits greater local deviations from the motion model but makes the filter too sensitive to noisy measurements.

            The sensor_noise is the measurement noise which helps inform the filter how much it should weight the new measurements versus the current motion model.
            Specifying a high measurement noise indicates that the measurements are inaccurate and causes the filter to favor the existing motion model and react 
            more slowly to deviations from the motion model. 

            The ratio between the process noise and the measurement noise determines whether the filter follows closer to the motion model, if the process noise 
            is smaller, or closer to the measurements, if the measurement noise is smaller. 

            Inspirations:
                http://interactive-matter.eu/blog/2009/12/18/filtering-sensor-data-with-a-kalman-filter/
                https://github.com/denyssene/SimpleKalmanFilter/blob/master/src/SimpleKalmanFilter.cpp
                https://github.com/denyssene/SimpleKalmanFilter
                https://www.mathworks.com/help/fusion/ug/tuning-kalman-filter-to-improve-state-estimation.html
        """
        self.err_process = 1.0 * process_noise      # process noise covariance
        self.err_measure = 1.0 * sensor_noise       # measurement noise covariance
        self.err_estimation = 1.0 * estimated_error # estimation error covariance

        self.current_estimate = None # will hold the iterated filtered value

        self.threshold = None if radius is None else abs(radius)
        self.delay_count = delay_radius_count
        self.counter = self.delay_count
        self.threshold_reached = False

        if self.threshold is not None:
            # Duplicate value to get a reference to the initial condition that will be used when we move out of the threshold
            self.err_estimation_initial = self.err_estimation

    def apply_filter(self, new_value):

        if self.current_estimate is None:
                self.current_estimate = new_value
                return self.current_estimate
        else:
            diff = abs(new_value - self.current_estimate)

            if self.threshold is not None and diff > self.threshold:
                self.threshold_reached = True
                self.err_estimation    = self.err_estimation_initial
                self.current_estimate  = new_value
                
                return self.current_estimate

            else:
                if self.threshold_reached:
                    if self.counter > 0:
                        self.counter -= 1
                        self.current_estimate = new_value

                        return self.current_estimate
                    else:
                        self.threshold_reached = False
                        self.counter = self.delay_count

                else:
                    last_estimate = self.current_estimate

                    kalman_gain           = self.err_estimation / (self.err_estimation + self.err_measure)
                    self.current_estimate = last_estimate + kalman_gain * (new_value - last_estimate)
                    self.err_estimation   = (1.0 - kalman_gain) * self.err_estimation + abs(last_estimate - self.current_estimate) * self.err_process

                    return self.current_estimate

                    ### Old algorithm for legacy purpose
                    # # prediction update
                    # self.p = self.p + self.q

                    # # measurement update
                    # k = self.p / (self.p + self.r)
                    # self.x = self.x + k * (new_value - self.x)
                    # self.p = (1.0 - k) * self.p

                    # return self.x

### Joystick Gremlin UI

mode = ModeVariable("Mode", "The mode in which to use this mapping")

joy_axis = PhysicalInputVariable(
        "Physical input axis",
        "The physical input axis being filtered.",
        [gremlin.common.InputType.JoystickAxis]
)

vjoy_axis = VirtualInputVariable(
        "Virtual output axis",
        "The vJoy axis to send the filtered output to.",
        [gremlin.common.InputType.JoystickAxis]
)

invert_axis = BoolVariable(
        "Invert axis",
        "If checked, the axis will be inverted.",
        False
)

center_dz_upper = IntegerVariable(
        "Center deadzone in %: upper limit",
        "In conjunction with the lower limit setting, define an area (expressed in percentage) around the neutral point that will be treated as 0.",
        0,
        0,
        100
)

center_dz_lower = IntegerVariable(
        "Center deadzone in %: lower limit",
        "In conjunction with the upper limit setting, define an area (expressed in percentage) around the neutral point that will be treated as 0.",
        0,
        -100,
        0
)

output_max = FloatVariable(
        "Upper saturation: coef ",
        "Upper saturation of the axis expressed with a coefficient. 1.0 = no saturation, 0.0 = full saturation.",
        1.0,
        0.0,
        1.0
)

output_min = FloatVariable(
        "Lower saturation: coef ",
        "Lower saturation of the axis expressed with a coefficient. -1.0 = no saturation, 0.0 = full saturation.",
        -1.0,
        -1.0,
        0.0
)

### Vars setup

d_axis = joy_axis.create_decorator(mode.value)

g_vjoy = gremlin.joystick_handling.VJoyProxy()
g_joy_axis_max = 1 # empirical test tells us gremlin returns value from -1 to 1, neutral at 0.

# Filter specialy tailored for my X52.
g_filter_kalman = KalmanFilter(
    process_noise   = 1    * g_joy_axis_max, 
    sensor_noise    = 0.1  * g_joy_axis_max, 
    estimated_error = 0.1  * g_joy_axis_max, 
    radius          = 0.07 * g_joy_axis_max
)

v_output_max = output_max.value
v_output_min = output_min.value
v_invert = invert_axis.value

v_center_dz_upper_limit = (center_dz_upper.value/100.0) * g_joy_axis_max
v_center_dz_lower_limit = (center_dz_lower.value/100.0) * g_joy_axis_max

### Plugin logic

def update_vjoy(new_value):
    global g_filter_kalman, g_vjoy, g_joy_axis_max

    # Center deadzone
    if (new_value >= v_center_dz_lower_limit and new_value <= v_center_dz_upper_limit):
        new_value = 0

    # Upper saturation
    elif (new_value >= v_output_max):
        new_value = v_output_max

    # Lower saturation
    elif (new_value <= v_output_min):
        new_value = v_output_min

    # Max limit reached
    elif (abs(new_value) == g_joy_axis_max):
        # If we are at the limit of the axis, don't do any algorithm smoothing and send back the original value.
        pass

    # Time to apply the filter if we're out of special cases
    else:
        kalman_val = g_filter_kalman.apply_filter(new_value)

        # Bypass a bug with JG rarely occuring, kalman_val could be None even though kalman function returns a value (checked with log debugging). Reason unknown.
        if kalman_val is None:
            return

        new_value = kalman_val

    if (v_invert):
        new_value = -new_value

    g_vjoy[vjoy_axis.vjoy_id].axis(vjoy_axis.input_id).value = new_value

@d_axis.axis(joy_axis.input_id)
def axis_cb(event):
    update_vjoy(event.value)