import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from experiment_interfaces.action import GenerateEvenNumbers

from rclpy.action import GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from action_msgs.msg import GoalStatus

import time

class EvenNumbersServer(Node):

    def __init__(self):
        super().__init__('even_numbers_server')
        self._action_server = ActionServer(
            self,
            GenerateEvenNumbers,
            'generate_even_numbers',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )
        self.get_logger().info('Even Numbers Action Server started')

    def goal_callback(self, goal_request):
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info('Executing goal...')
        feedback_msg = GenerateEvenNumbers.Feedback()
        result = GenerateEvenNumbers.Result()
        even_numbers = []

        # Generate first 10 even numbers
        for i in range(1, 22, 2):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result.even_numbers = even_numbers
                return result

            feedback_msg.current_number = i
            goal_handle.publish_feedback(feedback_msg)
            even_numbers.append(i)
            self.get_logger().info(f'Feedback: {i}')
            time.sleep(1)

        goal_handle.succeed()
        result.even_numbers = even_numbers
        self.get_logger().info(f'Result: {even_numbers}')
        return result


def main(args=None):
    rclpy.init(args=args)
    server = EvenNumbersServer()
    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        pass
    finally:
        server.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

