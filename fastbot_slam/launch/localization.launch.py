from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PythonExpression, PathJoinSubstitution
from launch.conditions import IfCondition
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():

    map_basename = "fastbot_home_sim_map.yaml"
    map_file_path = PathJoinSubstitution([FindPackageShare('fastbot_slam'),'config', map_basename])

    amcl_basename = "amcl_config.yaml"
    amcl_yaml_path = PathJoinSubstitution([FindPackageShare('fastbot_slam'), 'config', amcl_basename])

    rviz_basename = "localization.rviz"
    rviz_config = PathJoinSubstitution([FindPackageShare('fastbot_slam'), 'rviz', rviz_basename])
    

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': True}, 
                    {'yaml_filename':map_file_path} 
                    ])

    amcl_node = Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[amcl_yaml_path,{'use_sim_time': True}]
    )

    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            name='rviz_node_localization',
            parameters=[
                {'use_sim_time': True}
            ],
            arguments=['-d', rviz_config]
        )
    
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localizer',
        output='screen',
        parameters=[{'use_sim_time': True},
                    {'autostart': True},
                    {'node_names': ['map_server', 'amcl']}])


    return LaunchDescription(
        [
            map_server_node,
            amcl_node,
            rviz_node,
            lifecycle_manager_node
        ]
    )