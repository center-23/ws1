import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('sim')
    nav2_bringup_share = get_package_share_directory('nav2_bringup')

    # 地図とパラメータのパス
    map_yaml_file = os.path.join(pkg_share, 'maps', 'my_warehouse_map.yaml')
    params_file = os.path.join(pkg_share, 'config', 'nav2_params.yaml')
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'nav2_view.rviz')

    # Nav2 Bringupの起動
    # Nav2 Bringupの起動
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_share, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_yaml_file,
            'params_file': params_file,
            'use_sim_time': 'True',
            'autostart': 'True',
            'use_composition': 'False',
            # ここが重要：Jazzyの引数名に合わせる
            'use_dock_server': 'False',    # 'ing'なし
            'use_route_server': 'False',   # これも使わないならFalse
            'use_waypoint_follower': 'True',
        }.items()
    )

    # RViz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        nav2_bringup,
        rviz_node
    ])