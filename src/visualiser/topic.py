import rclpy
from rclpy.node import Node
from importlib import import_module
import time
from queue import SimpleQueue
from ros2topic.api import get_msg_class
from rclpy.clock import Clock, ClockType

class Topic(Node):

    def __init__(self, topic, message):
        super().__init__(f"topic_{topic[1:]}")
        print(f"created topic_{topic[1:]}")
        self.topic = topic 
        self.data = SimpleQueue() 
        self.message_type = get_msg_class(self, topic)
        self.clock = Clock(clock_type = ClockType.ROS_TIME)
        self.init_time = self.clock.now()

        self.subscriber_ = self.create_subscription(self.message_type, 
                                                    self.topic, 
                                                    self.sub_callback, 
                                                    qos_profile = 10)

    def retreive(self, length):
        return [self.data.get() for i in range(length)]

    def sub_callback(self, msg):
        stamp = (self.clock.now() - self.init_time).nanoseconds / 1_000_000 
        # TODO(implement custom message field parser by looking at .msg files)
        # TODO(fix the delay of messages being sent)
        self.data.put((stamp, msg.data))
        
