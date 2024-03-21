import gremlin
import gremlin.event_handler
from gremlin.user_plugin import *

### Joystick Gremlin UI

mode = ModeVariable("Mode", "The mode in which to use this mapping")

joy_action_btn = PhysicalInputVariable(
        "Joystick Button - Action",
        "The main joystick button to which you want to create a mapping.",
        [gremlin.common.InputType.JoystickButton]
)

joy_modifier_btn = PhysicalInputVariable(
        "Joystick Button - Modifier",
        "The modifier joystick button.",
        [gremlin.common.InputType.JoystickButton]
)

vjoy_main_action_btn = VirtualInputVariable(
        "vJoy Button - Main Action",
        "The vjoy button to press when only the 'Joystick Button - Action' is pressed.",
        [gremlin.common.InputType.JoystickButton]
)

vjoy_modifier_action_btn = VirtualInputVariable(
        "vJoy Button - Modifier Action",
        "The vjoy button to press when both the 'Joystick Button - Action' and 'Joystick Button - Modifier' is pressed.",
        [gremlin.common.InputType.JoystickButton]
)

### Vars setup

d_joy_main_btn     = joy_action_btn.create_decorator(mode.value)
d_joy_modifier_btn = joy_modifier_btn.create_decorator(mode.value)

g_vjoy = gremlin.joystick_handling.VJoyProxy()
g_joy_main_btn_active     = False
g_joy_modifier_btn_active = False

### Plugin logic

def update_vjoy_buttons_state(is_vjoy_main_btn_active, is_vjoy_modifier_btn_active):
    global g_vjoy

    g_vjoy[vjoy_main_action_btn.vjoy_id].button(vjoy_main_action_btn.input_id).is_pressed         = is_vjoy_main_btn_active
    g_vjoy[vjoy_modifier_action_btn.vjoy_id].button(vjoy_modifier_action_btn.input_id).is_pressed = is_vjoy_modifier_btn_active

def update_vjoy():
    global g_joy_main_btn_active, g_joy_modifier_btn_active

    if (g_joy_main_btn_active and not g_joy_modifier_btn_active):
        update_vjoy_buttons_state(True, False)
        
    elif (g_joy_main_btn_active and g_joy_modifier_btn_active):
        update_vjoy_buttons_state(False, True)
        
    else:
        update_vjoy_buttons_state(False, False)

@d_joy_main_btn.button(joy_action_btn.input_id)
def joy_main_button_cb(event):
    global g_joy_main_btn_active
    
    g_joy_main_btn_active = event.is_pressed
    update_vjoy()
        
@d_joy_modifier_btn.button(joy_modifier_btn.input_id)
def joy_modifier_btn_cb(event):
    global g_joy_modifier_btn_active
    
    g_joy_modifier_btn_active = event.is_pressed 
    update_vjoy()
