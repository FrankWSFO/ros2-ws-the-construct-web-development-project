from example_interfaces.action import Fibonacci
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse

class TestAction(Node):
    def __init__(self):
        super().__init__('test_action_node')

        self.get_logger().set_level(rclpy.logging.LoggingSeverity.DEBUG)

        self._late_init_timer = self.create_timer(0.0, self._late_init)

        self.get_logger().info("Test action server constructor finished")

    def _late_init(self):
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'test_action',
            execute_callback=self.execute_cb,
            goal_callback=self.goal_request_cb,
            cancel_callback=self.cancel_cb
        )
        self.get_logger().info("Action server initialized after spin")
        self._late_init_timer.cancel()

    def goal_request_cb(self, goal_request):
        self.get_logger().info("Goal request received: %s" % str(goal_request))
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        self.get_logger().info("Cancel request received")
        return CancelResponse.ACCEPT

    async def execute_cb(self, goal_handle):
        self.get_logger().info("Execute callback started")
        feedback = Fibonacci.Feedback()
        feedback.sequence = [0]
        goal_handle.publish_feedback(feedback)
        result = Fibonacci.Result()
        result.sequence = [0]
        goal_handle.succeed()
        return result

def main(args=None):
    rclpy.init(args=args)
    # rclpy.get_logger().debug("After init rclpy")
    node = TestAction()
    node.get_logger().info("After node construction in main")
    try:
        node.get_logger().info("Just before attempt to spin in main")
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()