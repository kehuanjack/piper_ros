import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from piper_sdk import C_PiperInterface_V2

class DelayTest(Node):
    def __init__(self):
        super().__init__('delay_test_node')
        self.declare_parameter('delay_test_mode', 'M1')
        self.delay_test_mode = self.get_parameter('delay_test_mode').get_parameter_value().string_value
        self.get_logger().info(f"delay_test_mode is {self.delay_test_mode}")

        if self.delay_test_mode == 'M2':
            self.subscription = self.create_subscription(
                JointState,
                'joint_states_single',
                self.M2,
                1
            )
        else:
            self.subscription = self.create_subscription(
                JointState,
                'joint_states_single',
                self.M1,
                1
            )
        self.subscription  # 防止未使用变量警告

        self.piper = C_PiperInterface_V2()
        self.piper.ConnectPort()

    def M1(self, msg):
        # 何时给主控下发101反馈指令
        seq2 = self.piper.GetArmSeq().seq.seq2
        if seq2 != 0:
            self.piper.GripperTest()

    def M2(self, msg):
        # 何时给主控下发101反馈指令
        angle = msg.position[6]
        if angle <= 0:
            self.piper.GripperTest()

def main(args=None):
    rclpy.init(args=args)
    subscriber = DelayTest()
    try:
        rclpy.spin(subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    '''需先运行本节点，再运行single节点'''
    main()
