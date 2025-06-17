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
        self.get_topics()

        self.plot_data = {}
        self.lines = {}
        self.fig, self.axs = plt.subplots(
                                        self.len_topics, # rows
                                        1,               # columns  
                                        figsize = (10, 5 * self.len_topics), #TODO(MAKE IT ADJUSTABLE FOR GUI)
                                        squeeze = False)
        self.axs = self.axs = [ax[0] for ax in self.axs]
        for ax in self.axs:
            ax.set_xlabel("Time")
            ax.set_ylabel("Data")
            ax.grid(True)

        for ax, topic_node in zip(self.axs, self.topics):
            self.plot_data[topic_node.topic] = {'x': [], 'y': []}
            self.lines[topic_node.topic], = ax.plot([], [], label=topic_node.topic)
            ax.legend()
        
        plt.ion()
        self.timer = self.create_timer(1.0, self.display)

    def get_topics(self):
        res = self.get_topic_names_and_types() # [(topic, [message_type]), ]

        for topic, message in res:
            self.topics.append(Topic(topic, message)) if topic not in self.blacklisted else None
        
        self.len_topics = len(self.topics)
        if (self.len_topics == 0): raise Exception("No topics found") 
        else: print(f"Found {self.len_topics} topics")

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
        for ax in self.axs:
            ax.relim()
            ax.autoscale_view()
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