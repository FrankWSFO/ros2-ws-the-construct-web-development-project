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
    amcl_basename = "amcl_config.yaml"
    
    map_file_path = PathJoinSubstitution([FindPackageShare('fastbot_slam'),'config', map_basename])
    amcl_yaml_path = PathJoinSubstitution([FindPackageShare('fastbot_slam'), 'config', amcl_basename])

    bt_xml = PathJoinSubstitution([FindPackageShare('fastbot_slam'), 'config', 'navigate_w_replanning_and_recovery.xml'])

    planner_basename = "planner.yaml"
    controller_basename = "controller.yaml"
    bt_navigator_basename = "bt_navigator.yaml"
    recovery_basename = "recoveries.yaml"

    planner_yaml = PathJoinSubstitution([FindPackageShare('fastbot_slam'), 'config', planner_basename])
    controller_yaml = PathJoinSubstitution([FindPackageShare('fastbot_slam'), 'config', controller_basename])
    bt_navigator_yaml = PathJoinSubstitution([FindPackageShare('fastbot_slam'), 'config', bt_navigator_basename])
    recovery_yaml = PathJoinSubstitution([FindPackageShare('fastbot_slam'), 'config', recovery_basename])

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': True}, 
                    {'yaml_filename':map_file_path} 
                    ]
    )

    amcl_node = Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[amcl_yaml_path,{'use_sim_time': True}]
    )

    planner_server_node = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[planner_yaml, {'use_sim_time': True}], 
        arguments=[ '--ros-args', '--log-level', 'nav2_planner:=debug', '--log-level', 'nav2_navfn_planner:=debug' ],
    )

    controller_server_node = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[controller_yaml, {'use_sim_time': True}],
        remappings=[
            ('cmd_vel', '/fastbot_1/cmd_vel')
        ],
        arguments=[ '--ros-args', '--log-level', 'nav2_controller:=debug', '--log-level', 'dwb_core:=debug', '--log-level', 'dwb_plugins:=debug' ],
    )
            
    bt_navigator_node = Node(            
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[bt_navigator_yaml, {'default_nav_to_pose_bt_xml': bt_xml}, {'use_sim_time': True}],
    )

    recoveries_server_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[recovery_yaml, {'use_sim_time': True}],
        remappings=[
            ('cmd_vel', '/fastbot_1/cmd_vel')
        ],
    )

    rviz_config = os.path.join(get_package_share_directory('fastbot_slam'), 'rviz', 'navigation.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        name='rviz_node_pathplanning',
        parameters=[
            {'use_sim_time': True}
        ],
        arguments=['-d', rviz_config],
    )
    
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localizer',
        output='screen',
        parameters=[{'use_sim_time': True},
                    {'autostart': True},
                    {'node_names': ['map_server', 'amcl', 'planner_server', 'controller_server', 'bt_navigator', 'behavior_server']}]
    )


    return LaunchDescription(
        [
            map_server_node,
            amcl_node,
            planner_server_node,
            controller_server_node,
            bt_navigator_node,
            recoveries_server_node, 
            rviz_node,
            lifecycle_manager_node
        ]
    )