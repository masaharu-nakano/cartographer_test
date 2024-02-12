from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='serial_arduino',
            namespace='serial_arduino',
            executable='serial_test3',
        ),
        
    ])
