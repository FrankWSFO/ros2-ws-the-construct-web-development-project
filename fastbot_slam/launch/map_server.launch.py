from launch import LaunchDescription

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():

    map_file = os.path.join(get_package_share_directory('fastbot_slam'), 'config', 'fastbot_home_sim_map.yaml')

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': True}, 
                    {'yaml_filename':map_file} 
                    ])

    rviz_config = os.path.join(get_package_share_directory('fastbot_slam'), 'rviz', 'map.rviz')

    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            name='rviz_node',
            parameters=[
            {'use_sim_time': True}
            ],
            arguments=['-d', rviz_config]
        )
    

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_mapper',
        output='screen',
        parameters=[{'use_sim_time': True},
                    {'autostart': True},
                    {'node_names': ['map_server']}])


    # create and return launch description object
    return LaunchDescription(
        [
            map_server_node,
            rviz_node,
            lifecycle_manager_node
        ]
    )