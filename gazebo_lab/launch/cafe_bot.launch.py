from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_my_lab = get_package_share_directory('gazebo_lab')
    pkg_tb3_gazebo = get_package_share_directory('turtlebot3_gazebo')

    world = os.path.join(pkg_my_lab, 'worlds', 'cafe.world')
    robot_sdf = os.path.join(
        pkg_tb3_gazebo,
        'models',
        'turtlebot3_waffle_pi',
        'model.sdf'
    )

    gazebo_model_path = os.path.join(pkg_tb3_gazebo, 'models')

    return LaunchDescription([
        SetEnvironmentVariable(
            name='GAZEBO_MODEL_PATH',
            value=gazebo_model_path + ':' + os.environ.get('GAZEBO_MODEL_PATH', '')
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={'world': world}.items()
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'tb3',
                '-file', robot_sdf,
                '-x', '1.0',
                '-y', '-2.0',
                '-z', '0.03'
            ],
            output='screen'
        ),
    ])