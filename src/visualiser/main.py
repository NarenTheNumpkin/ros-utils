import rclpy
from rclpy.node import Node
from topic import Topic
from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

class Snooper(Node):

    def __init__(self):
        super().__init__("Snooper")
        self.blacklisted = ["/parameter_events", "/rosout"]
        self.topics = []
        self.timer = self.create_timer(1.0, self.display)
        self.get_topics()

    def get_topics(self):
        res = self.get_topic_names_and_types() # [(topic, [message_type]), ]

        for topic, message in res:
            self.topics.append(Topic(topic, message)) if topic not in self.blacklisted else None
        
        if (len(self.topics) == 0): raise Exception("No topics found")

    def display(self):
        print(self.topics[0].retreive(1))

def main():
    rclpy.init()
    snooper = Snooper()
    executor = MultiThreadedExecutor()

    executor.add_node(snooper)
    for node in snooper.topics:
        executor.add_node(node)

    try:
        executor.spin()
    finally:
        snooper.destroy_node()
        for node in snooper.topics:
            node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()