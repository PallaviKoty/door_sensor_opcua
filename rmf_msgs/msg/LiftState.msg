builtin_interfaces/Time lift_time
string lift_name
string session_id
string[] available_floors
string current_floor
string destination_floor
uint8 door_state   # 0 - close, 2 - open
uint8 DOOR_OPEN=2
uint8 DOOR_MOVING=1
uint8 DOOR_CLOSED=0
uint8 motion_state
uint8 MOTION_STOPPED=0
uint8 MOTION_UP=1
uint8 MOTION_DOWN=2
uint8 MOTION_UNKNOWN=3
uint8[] available_modes
uint8 current_mode
uint8 MODE_UNKNOWN=0
uint8 MODE_HUMAN=1
uint8 MODE_AGV=2
uint8 MODE_FIRE=3
uint8 MODE_OFFLINE=4
uint8 MODE_EMERGENCY=5

