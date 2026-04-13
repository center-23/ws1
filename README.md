topic and msg change
ex
/demo/... x /... o
TwistStamped x Twist o
important is ctrl+s

more use cmd
colcon build --symlink-install
colcon build --symlink-install --packages-select
. install/setup.bash
grep -rn "/demo"
ros2 run rqt_graph rqt_graph

use cmd
ros2 launch sim A_display.launch.py
ros2 launch sim A_nav2.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 run rviz2 rviz2
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/A/sam_bot_description/maps/my_warehouse_map