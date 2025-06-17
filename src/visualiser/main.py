import rclpy
from rclpy.node import Node
from topic import Topic
from rclpy.executors import SingleThreadedExecutor
import matplotlib.pyplot as plt
import threading

class Snooper(Node):

    def __init__(self):
        super().__init__("Snooper")
        self.blacklisted = ["/parameter_events", "/rosout"]
        self.topics = []
        self.timer = self.create_timer(1.0, self.display)
        self.get_topics()

        self.plot_data = {}
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("Time (ms)")
        self.ax.set_ylabel("Value")
        self.lines = {}

        for topic_node in self.topics:
            self.plot_data[topic_node.topic] = {'x': [], 'y': []}
            self.lines[topic_node.topic], = self.ax.plot([], [], label=topic_node.topic)
        self.ax.legend()

    def get_topics(self):
        res = self.get_topic_names_and_types() # [(topic, [message_type]), ]

        for topic, message in res:
            self.topics.append(Topic(topic, message)) if topic not in self.blacklisted else None
        
        if (len(self.topics) == 0): raise Exception("No topics found")

    def display(self):
        for topic_node in self.topics:
            while not topic_node.data.empty():
                stamp, msg_data = topic_node.data.get()
                try:
                    value = float(msg_data.split()[-1])
                except Exception:
                    continue

                self.plot_data[topic_node.topic]['x'].append(stamp)
                self.plot_data[topic_node.topic]['y'].append(value)
                self.lines[topic_node.topic].set_data(self.plot_data[topic_node.topic]['x'],
                                                      self.plot_data[topic_node.topic]['y'])
        self.ax.relim()
        self.ax.autoscale_view()
        plt.draw()
        plt.pause(0.001)

def main():
    rclpy.init()
    snooper = Snooper()
    executor = SingleThreadedExecutor()
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