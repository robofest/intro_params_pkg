# A simple program with 2 ROS2 params

## Test 1: Use ros2 param get/set commands to change the parameters
```bash
$ ros2 run intro_params_pkg intro_params_node_exe
```

## Test 2: Provide parameters via command line arguments
```bash
$ ros2 run intro_params_pkg intro_params_node_exe --ros-args -p message:="Custopm CLI message" -p frequence:=0.2
```

## Test 3: Provide parameters via rqt/dyn reconfigure GUI
```bash