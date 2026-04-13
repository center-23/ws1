import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from ros_gz_bridge.actions import RosGzBridge
from ros_gz_sim.actions import GzServer

def generate_launch_description():
    pkg_share = get_package_share_directory('sim')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
    
    # パス設定
    gz_spawn_model_launch_source = os.path.join(ros_gz_sim_share, "launch", "gz_spawn_model.launch.py")
    default_model_path = os.path.join(pkg_share, 'urdf', 'A_description.urdf.xacro')
    world_path = os.path.join(pkg_share, 'world', 'warehouse.sdf')
    bridge_config_path = os.path.join(pkg_share, 'config', 'bridge_config.yaml')

    # Gazeboモデルパスの設定（倉庫モデルを表示するため）
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[os.path.join(get_package_share_directory('nav2_minimal_tb4_sim'), 'models')]
    )

    # 1. ロボットの状態を配信（URDFをTFに変換）
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', LaunchConfiguration('model')]),
            'use_sim_time': True
        }]
    )

    # 2. Gazeboサーバーの起動
    gz_server = GzServer(
        world_sdf_file=world_path,
        container_name='ros_gz_container',
        create_own_container='True',
        use_composition='True',
    )

    # 3. Gazebo GUI (クライアント) の起動
    gz_gui = ExecuteProcess(cmd=['gz', 'sim', '-g'], output='screen')

    # 4. ROS-Gazebo ブリッジ（トピックの橋渡し）
    ros_gz_bridge = RosGzBridge(
        bridge_name='ros_gz_bridge',
        config_file=bridge_config_path,
        container_name='ros_gz_container',
        create_own_container='False',
        use_composition='True',
    )

    # 5. ロボットをスポーン
    spawn_entity = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_spawn_model_launch_source),
        launch_arguments={
            'world': 'warehouse',
            'topic': '/robot_description',
            'entity_name': 'ws1_bot',
            'z': '0.65',
        }.items(),
    )

    # 6. 自己位置推定用 EKF
    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_node',
        output='screen',
        parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': True}],
    )

    return LaunchDescription([
        set_gz_resource_path,
        DeclareLaunchArgument(name='model', default_value=default_model_path),
        gz_server,
        gz_gui,
        robot_state_publisher_node,
        ros_gz_bridge,
        spawn_entity,
        robot_localization_node,
    ])