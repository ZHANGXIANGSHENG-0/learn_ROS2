import rclpy 
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

#定義大腦

class TurtleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('turtle_avoidance_node')
        # 創建一個發布者：往 'turtle1/cmd_vel' 發送 Twist 訊息，隊列長度 10
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # 創建一個訂閱者：監聽 'turtle1/pose'，收到後執行 self.pose_callback
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        # 1. 定義狀態：0 代表前進，1 代表避障
        self.state = "FORWARD"

        # 2. 紀錄避障開始的時間點
        self.avoid_start_time = None

#決策邏輯

    def pose_callback(self, msg):
        cmd = Twist()
        now = self.get_clock().now()

    # --- 狀態 1：避障模式 (優先權最高) ---
        if self.state == "AVOID":
        # 計算已經躲了多久
            duration = (now - self.avoid_start_time).nanoseconds / 1e9
        
            if duration < 0.5:
            # 動作：這 2 秒內，我們「不看感測器」，專心轉彎
                cmd.linear.x = 0.5
                cmd.angular.z = 2.0 
            else:
            # 2 秒到了，切換狀態
                self.state = "FORWARD"
                self.get_logger().info("避障完成，恢復前進")

    # --- 狀態 2：偵測模式 (只有在非避障時才執行) ---
        elif msg.x > 9.0 or msg.x < 2.0 or msg.y > 9.0 or msg.y < 2.0:
            self.state = "AVOID"
            self.avoid_start_time = now
            self.get_logger().warn("偵測到牆壁！切換至避障模式")

    # --- 狀態 3：正常前進 ---
        else:
            cmd.linear.x = 2.0
            cmd.angular.z = 0.0

        self.publisher_.publish(cmd)
        #把填好的「指令單 (cmd)」塞進準備好的「發佈機 (self.publisher_)」發送出去。

#啟動

def main(args=None):
    rclpy.init(args=args)
    node = TurtleAvoidanceNode()
    rclpy.spin(node) # 讓程式持續運行，等待訊息
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':    #避免讓別人借用我的程式時，在錯誤的時機點開始執行程式，而只是複製以上的程式碼，並沒有真的執行
    main()

#第四階段：正確的寫程式流程 (Engineer's Workflow)

#寫完代碼後，不要直接按右鍵執行 Python，正確的 ROS 2 流程是：

#修改 setup.py：你需要告訴 ROS 2 哪裡是程式入口（這部分需要我幫你調整嗎？）。

#編譯 (Build)：回到 learn_ROS2 根目錄，執行 colcon build。

#環境設定 (Source)：執行 source install/setup.bash，讓系統找到你的新程式。

#執行 (Run)：用 ros2 run 來啟動。