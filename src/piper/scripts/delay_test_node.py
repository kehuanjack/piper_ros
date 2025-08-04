#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState
from piper_sdk import C_PiperInterface_V2

class DelayTest:
    def __init__(self):
        rospy.init_node('delay_test_node', anonymous=True)
        
        # 获取参数并设置默认值
        self.delay_test_mode = rospy.get_param('~delay_test_mode', 'M1')
        rospy.loginfo(f"delay_test_mode is {self.delay_test_mode}")

        # 根据参数选择回调函数
        if self.delay_test_mode == 'M2':
            self.subscription = rospy.Subscriber(
                'joint_states_single',
                JointState,
                self.M2,
                queue_size=1
            )
        else:
            self.subscription = rospy.Subscriber(
                'joint_states_single',
                JointState,
                self.M1,
                queue_size=1
            )

        self.piper = C_PiperInterface_V2()
        self.piper.ConnectPort()

    def M1(self, msg):
        """M1模式：基于主控序列号触发"""
        seq2 = self.piper.GetArmSeq().seq.seq2
        if seq2 != 0:
            self.piper.GripperTest()

    def M2(self, msg):
        """M2模式：基于关节角度触发"""
        if len(msg.position) > 6:  # 确保有第7个关节数据
            angle = msg.position[6]
            if angle <= 0:
                self.piper.GripperTest()

def main():
    node = DelayTest()
    rospy.spin()

if __name__ == '__main__':
    '''需先运行本节点，再运行single节点'''
    main()