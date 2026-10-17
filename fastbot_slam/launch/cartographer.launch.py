from launch import LaunchDescription

from launch_ros.actions import Node

from launch.actions import DeclareLaunchArgument

from launch.substitutions import LaunchConfiguration, PythonExpression, PathJoinSubstitution

from launch_ros.substitutions import FindPackageShare

import launch.logging

from ament_index_python.packages import get_package_share_directory

import os

# launch.logging.get_logger().setLevel('DEBUG')
# cmd to save map: ros2 run nav2_map_server map_saver_cli -f <desired name>


def generate_launch_description():

    cartographer_config_dir = os.path.join(
        get_package_share_directory('fastbot_slam'), 'config')
    configuration_basename = "cartographer.lua"

    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[
            {'use_sim_time': False}
        ],
        arguments=['-configuration_directory', cartographer_config_dir,
                   '-configuration_basename', configuration_basename,
                   # '--ros-args', '--log-level', 'DEBUG'
                   ],
        # Cartographer expects scan and odom, so we remap so that wherever cartographer node says "look for scan", it actually looks for "/fastbot_1/scan"
        # It's like DNS record name resolution of urls to ips apparently ok
        remappings=[
            ('scan', '/fastbot/scan'),
            ('odom', '/fastbot/odom')
        ],
    )

    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        output='screen',
        name='occupancy_grid_node',
        parameters=[
            {'use_sim_time': False}
        ],
        arguments=['-resolution', '0.03', '-publish_period_sec', '1.0',
                   # '--ros-args', '--log-level', 'DEBUG'
                   ]
    )

    rviz_config = os.path.join(get_package_share_directory(
        'fastbot_slam'), 'rviz', 'cartography.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        name='rviz_node',
        parameters=[
                {'use_sim_time': False}
        ],
        arguments=['-d', rviz_config]
    )

    # create and return launch description object
    return LaunchDescription(
        [
            cartographer_node,
            occupancy_grid_node,
            rviz_node
        ]
    )

# save generated map command
# ros2 run nav2_map_server map_saver_cli -f turtlebot_area
