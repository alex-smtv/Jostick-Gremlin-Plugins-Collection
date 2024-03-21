# Collection of personnal Gremlin Plugins
A collection of [Joystick Gremlin](https://github.com/WhiteMagic/JoystickGremlin) plugins I developed/adapted/collected.

_Side note: When using plugins Joystick Gremlin may produce a bug with his user interface input box (cannot accept negative numbers) and for that reason it is advised to use the Release 13.3 Debug or higher._

## List of plugins
* _kalman_filter.py_ : 
  Use and extend the Kalman algorithm to be applied to an axis to smooth out jitters. Instead of applying the algorithm consistently to the full range of motion (which will create lag to catch up fast change of direction), the algorithm is smartly applied to the current localized point and deactivated for fast and dynamic change. The initial parameters for the algorithm have especially been fine tuned for a X52.

* _bind-to-btn_with_modifier_reevaluation.py_ : 
  Bind a physical button to one vJoy button amongst two depending on whether or not a specified modifier physical button is held. By Joystick Gremlin design if we hold a physical button which outputs a vJoy button press and then use all the while a modifier while the physical button is held, then the second vJoy button press that must occur with the modifier combination is not activated and the output is stuck on the first vJoy button press. This plugin bypasses and fixes that behavior to consistently reevaluate the current state.

* _bind-to-mouse-fixed_with_modifier_reevaluation.py_ : 
  The concept is the same as _bind-to-btn_with_modifier_reevaluation.py_ , but applied to mouse buttons instead of vJoy buttons. Choose a physical Joystick button and a modifier. A bind will then occur to mouse Left Click when no modifier is held and to mouse Right Click when the modifier is held. This plugin is called _fixed_ because it is not possible to alter which mouse buttons are activated through the Joystick Gremlin UI.

## License
Feel free to do whatever you want. The repo is released under the [MIT](./LICENSE.md) license.