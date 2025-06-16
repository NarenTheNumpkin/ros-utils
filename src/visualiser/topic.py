import rclpy
from rclpy.node import Node
from importlib import import_module
import time
from queue import SimpleQueue
from ros2topic.api import get_msg_class

class Topic(Node):

    def __init__(self, topic, message):
        super().__init__(f"topic_{topic[1:]}")
        print(f"created topic_{topic[1:]}")
        self.topic = topic 
        self.data = SimpleQueue() 
        self.message_type = get_msg_class(self, topic)

        self.subscriber_ = self.create_subscription(self.message_type, 
                                                    self.topic, 
                                                    self.sub_callback, 
                                                    qos_profile = 10)
        
    def retreive(self, length):
        return [self.data.get() for i in range(length)]

    def sub_callback(self, msg):
        stamp = time.time()
        #print(f"{self.topic} : {msg.data} : {time.time() - x}")             # TODO(implement custom message field parser by looking at .msg files)
        self.data.put((stamp, msg.data))
        
