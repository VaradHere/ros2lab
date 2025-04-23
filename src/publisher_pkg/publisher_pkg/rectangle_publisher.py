import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RectanglePublisher(Node):
    def __init__(self):
        super().__init__('rectangle_publisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer_period = 0.5  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.state = 'forward'
        self.forward_count = 0
        self.turn_count = 0
        self.side_index = 0  # 0=long, 1=short, 2=long, 3=short

        # Rectangle: alternate between long and short forward movement
        self.forward_limits = [10, 5, 10, 5]  # Adjust these for size
        self.turn_limit = 6  # 90-degree turn (adjust if needed)

    def timer_callback(self):
        msg = Twist()

        if self.side_index >= len(self.forward_limits):
            # Stop movement after rectangle
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('Rectangle complete. Stopping turtle.')
            self.publisher_.publish(msg)
            self.destroy_timer(self.timer)
            return

        if self.state == 'forward':
            msg.linear.x = 1.0
            msg.angular.z = 0.0
            self.forward_count += 1
            self.get_logger().info(f'Moving forward (side {self.side_index + 1})')

            if self.forward_count >= self.forward_limits[self.side_index]:
                self.forward_count = 0
                self.state = 'turn'

        elif self.state == 'turn':
            msg.linear.x = 0.0
            msg.angular.z = 0.53
            self.turn_count += 1
            self.get_logger().info(f'Turning 90° (after side {self.side_index + 1})')

            if self.turn_count >= self.turn_limit:
                self.turn_count = 0
                self.side_index += 1
                self.state = 'forward'

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RectanglePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()