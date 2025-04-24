import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from experiment_interfaces.action import GenerateEvenNumbers

class EvenNumbersClient(Node):
    def __init__(self):
        super().__init__('even_numbers_client')
        self._action_client = ActionClient(
            self,
            GenerateEvenNumbers,
            'generate_even_numbers'
        )
        self.get_logger().info('Even Numbers Action Client started')

    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()
       
        goal_msg = GenerateEvenNumbers.Goal()
        self.get_logger().info('Sending goal...')
       
        future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.current_number}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.even_numbers}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    client = EvenNumbersClient()
    client.send_goal()
    try:
        rclpy.spin(client)
    except KeyboardInterrupt:
        pass
    finally:
        client.destroy_node()

if __name__ == '__main__':
    main()
