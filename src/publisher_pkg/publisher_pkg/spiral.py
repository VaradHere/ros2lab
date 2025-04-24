import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SpiralPublisher(Node):
    def __init__(self):
        super().__init__('spiral_publisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.linear_x = 0.5  # Start with a small speed
        self.angular_z = 1.0  # Constant rotation
        timer_period = 0.1  # Faster update for smoother spiral
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = self.linear_x
        msg.angular.z = self.angular_z
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Spiral: linear.x={msg.linear.x:.2f}, angular.z={msg.angular.z:.2f}')

        # Gradually increase linear speed to widen the spiral
        self.linear_x += 0.01  # You can tweak this increment

def main(args=None):
    rclpy.init(args=args)
    spiral_publisher = SpiralPublisher()
    rclpy.spin(spiral_publisher)
    spiral_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
    
    
    
    
    

