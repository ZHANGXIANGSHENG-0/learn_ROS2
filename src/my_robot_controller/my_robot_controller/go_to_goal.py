import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class GoToGoal(Node):

    def __init__(self):
        super().__init__('go_to_goal')

        self.cmd_pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # 👉 目標點
        self.waypoints = [
            (9.0, 9.0),
            (2.0, 8.0),
            (2.0, 2.0),
            (9.0, 2.0),
        ]

        self.current_goal_index = 0

        self.current_pose = None
        
        self.finished = False

    def pose_callback(self, msg):
        self.current_pose = msg
        self.control_loop()

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle   

    def control_loop(self):
        if self.current_pose is None:
            return

        twist = Twist()

        if self.finished:
            self.cmd_pub.publish(twist)
            return

        goal_x, goal_y = self.waypoints[self.current_goal_index]
        dx = goal_x - self.current_pose.x
        dy = goal_y - self.current_pose.y

        distance = math.sqrt(dx**2 + dy**2)

        # 👉 目標方向角
        target_angle = math.atan2(dy, dx)

        # 👉 角度誤差
        angle_error = self.normalize_angle(
            target_angle - self.current_pose.theta
        )     
        
        # 👉 控制
        if distance > 0.1:

            # 👉 如果角度還沒對齊
            if abs(angle_error) > 0.1:  
            #0.1 × 180 / π ≈ 5.73°
            #abs(x)：取x絕對值
                twist.linear.x = 0.0
                twist.angular.z = 2.0 * angle_error
                self.get_logger().info('Turning...')

            # 👉 角度差不多了，才前進
            else:
                twist.linear.x = 1.0 * distance
                twist.angular.z = 0.0
                self.get_logger().info('Moving forward')
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

            self.get_logger().info(
                f'Reached waypoint {self.current_goal_index}: ({goal_x}, {goal_y})'
            )

            self.current_goal_index += 1

            if self.current_goal_index >= len(self.waypoints):
                self.get_logger().info('All waypoints reached')
                self.finished = True
                return

        self.cmd_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()