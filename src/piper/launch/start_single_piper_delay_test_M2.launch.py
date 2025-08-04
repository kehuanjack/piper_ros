from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # Declare the launch arguments
    can_port_arg = DeclareLaunchArgument(
        'can_port',
        default_value='can0',
        description='CAN port to be used by the Piper node.'
    )
    auto_enable_arg = DeclareLaunchArgument(
        'auto_enable',
        default_value='true',
        description='Automatically enable the Piper node.'
    )

    rviz_ctrl_flag_arg = DeclareLaunchArgument(
        'rviz_ctrl_flag',
        default_value='false',
        description='Start rviz flag.'
    )

    gripper_exist_arg = DeclareLaunchArgument(
        'gripper_exist',
        default_value='true',
        description='gripper'
    )

    gripper_val_mutiple_arg = DeclareLaunchArgument(
        'gripper_val_mutiple',
        default_value='1',
        description='gripper'
    )

    delay_test_mode = DeclareLaunchArgument(
        'delay_test_mode',
        default_value='M2',
        description='delay_test'
    )

    delay_test_node = Node(
        package='piper',
        executable='delay_test',
        name='delay_test_node',
        output='screen',
        parameters=[{
            'delay_test_mode': LaunchConfiguration('delay_test_mode'),
        }]

    )

    # Define the node
    piper_node = Node(
        package='piper',
        executable='piper_single_ctrl_delay_test',
        name='piper_ctrl_single_node',
        output='screen',
        parameters=[{
            'can_port': LaunchConfiguration('can_port'),
            'auto_enable': LaunchConfiguration('auto_enable'),
            'gripper_val_mutiple': LaunchConfiguration('gripper_val_mutiple'),
            'gripper_exist': LaunchConfiguration('gripper_exist'),
            'delay_test_mode': LaunchConfiguration('delay_test_mode'),
        }],
        remappings=[
            ('joint_ctrl_single', '/joint_states'),
        ]
    )

    # Return the LaunchDescription
    return LaunchDescription([
        can_port_arg,
        auto_enable_arg,
        gripper_exist_arg,
        gripper_val_mutiple_arg,
        delay_test_mode,
        delay_test_node,
        piper_node
    ])
