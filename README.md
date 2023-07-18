# Collection of personnal Gremlin Plugins
A collection of [Joystick Gremlin](https://github.com/WhiteMagic/JoystickGremlin) plugins I developed/adapted/collected.

_Side note: use the Release 13.3 Debug or higher. Otherwise you may encounter a bug where the user UI input box cannot accept negative numbers._  

## List of plugins
* _kalman_filter.py_ : 
  Use and extend the Kalman algorithm to be applied to an axis to smooth out jitters. Instead of applying the algorithm consistently to the full range of motion (which will create lag to catch up fast change of direction), the algorithm is smartly applied to the current localized point and deactivated for fast and dynamic change. The initial parameters for the algorithm have especially been fine tuned for a X52.

* _btn_with_modifier_reevaluation.py_ : 
  Map a physicial button to a vJoy button and to another vJoy button while a modifier is held. Originally if we hold the physical button, which output a vJoy button, and use the modifier while the phyisical button is held, then the second vJoy button is not activted and the output is stuck on the first vJoy button. This plugin fixes that behavior to consistently reevaluate current state.

## License
Feel free to do whatever you want. The repo is released under the [MIT](./LICENSE.md) license.