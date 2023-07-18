# Collection of personnal Gremlin Plugins
A collection of [Joystick Gremlin](https://github.com/WhiteMagic/JoystickGremlin) plugins I developed or adapted.

## List of plugins
* _kalman_filter.py_ : Use and extend the Kalman algorithm to be applied to an axis to smooth out jitters. Instead of applying the algorithm consistently to the full range of motion (which will create lag to catch up fast change of direction), the algorithm is smartly applied to the current localized point and deactivated for fast and dynamic change. The initial parameters for the algorithm have especially been fine tuned for a X52.

## License
Feel free to do whatever you want. The repo is released under the [MIT](./LICENSE.md) license.