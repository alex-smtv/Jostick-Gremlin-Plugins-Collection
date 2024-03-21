import gremlin
import gremlin.event_handler
from gremlin.user_plugin import *
from gremlin.sendinput import MouseButton, mouse_press, mouse_release

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

### Vars setup

d_joy_main_btn     = joy_action_btn.create_decorator(mode.value)
d_joy_modifier_btn = joy_modifier_btn.create_decorator(mode.value)

g_joy_main_btn_active     = False
g_joy_modifier_btn_active = False

g_mouse_left_active  = False
g_mouse_right_active = False

### Plugin logic

def update_mouse():
    global g_joy_main_btn_active, g_joy_modifier_btn_active, g_mouse_left_active, g_mouse_right_active

    if (g_joy_main_btn_active and not g_joy_modifier_btn_active):
        if g_mouse_right_active:
            mouse_release(MouseButton.Right)
            g_mouse_right_active = False

        mouse_press(MouseButton.Left)
        g_mouse_left_active  = True
        
    elif (g_joy_main_btn_active and g_joy_modifier_btn_active):
        if g_mouse_left_active:
            mouse_release(MouseButton.Left)
            g_mouse_left_active  = False

        mouse_press(MouseButton.Right)
        g_mouse_right_active = True
        
    else:
        if g_mouse_left_active:
            mouse_release(MouseButton.Left)
            g_mouse_left_active  = False

        if g_mouse_right_active:
            mouse_release(MouseButton.Right)
            g_mouse_right_active = False

@d_joy_main_btn.button(joy_action_btn.input_id)
def joy_main_button_cb(event):
    global g_joy_main_btn_active
    
    g_joy_main_btn_active = event.is_pressed
    update_mouse()
        
@d_joy_modifier_btn.button(joy_modifier_btn.input_id)
def joy_modifier_btn_cb(event):
    global g_joy_modifier_btn_active
    
    g_joy_modifier_btn_active = event.is_pressed 
    update_mouse()
