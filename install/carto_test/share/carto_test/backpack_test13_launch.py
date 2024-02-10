"""
  Copyright 2018 The Cartographer Authors
  Copyright 2022 Wyca Robotics (for the ros2 conversion)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

from launch import LaunchDescription
#※ from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetRemap
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

# from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
# from launch.conditions import IfCondition, UnlessCondition
# from launch.substitutions import LaunchConfiguration
# from launch_ros.actions import Node, SetRemap
# from launch_ros.substitutions import FindPackageShare
# from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import Shutdown



def generate_launch_description():

    ## ***** Launch arguments *****
    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value = 'False')

    #def generate_launch_description():
    ## ***** Launch arguments *****
    bag_filename_arg = DeclareLaunchArgument('bag_filename')

    ## ***** File paths ******絶対パス
    # pkg_share = FindPackageShare('cartographer_ros').find('cartographer_ros')
    # urdf_dir = os.path.join(pkg_share, 'urdf')
    # urdf_file = os.path.join(urdf_dir, 'backpack_2d.urdf')
    urdf_file = '/home/masa/Downloads/backpack_2d_test.urdf'
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    ## ***** Nodes *****
    robot_state_publisher_node = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        parameters=[
            {'robot_description': robot_desc},
            {'use_sim_time': LaunchConfiguration('use_sim_time')}],
        output = 'screen'
        )

    cartographer_node = Node(
        package = 'cartographer_ros',
        executable = 'cartographer_node',
        parameters = [{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        arguments = [
            '-configuration_directory', FindPackageShare('cartographer_ros').find('cartographer_ros') + '/configuration_files',
            '-configuration_basename', 'backpack_2d.lua'],
        remappings = [
            ('echoes', 'horizontal_laser_2d')],
        output = 'screen'
        )

    cartographer_occupancy_grid_node = Node(
        package = 'cartographer_ros',
        executable = 'cartographer_occupancy_grid_node',
        parameters = [
            {'use_sim_time': True},
            {'resolution': 0.05}],
        )

    ## ***** Nodes *****
    # backpack_2d_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(FindPackageShare('carto_test').find('carto_test') + '/launch/backpack_2d_launch.py'),
    #     launch_arguments = {'use_sim_time': 'True'}.items()
    #     )

    rviz_node = Node(
        package = 'rviz2',
        executable = 'rviz2',
        on_exit = Shutdown(),
        arguments = ['-d', 'demo_test.rviz'],
        parameters = [{'use_sim_time': True}],
    )

    ros2_bag_play_cmd = ExecuteProcess(
        cmd = ['ros2', 'bag', 'play', LaunchConfiguration('bag_filename'), '--clock'],
        name = 'rosbag_play',
    )


    return LaunchDescription([
        use_sim_time_arg,
        # Launch arguments
        bag_filename_arg,

        # Nodes
        robot_state_publisher_node,
        cartographer_node,
        cartographer_occupancy_grid_node,
        # Nodes
        # backpack_2d_launch,
        rviz_node,
        ros2_bag_play_cmd

    ])

