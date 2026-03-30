import rclpy
from rclpy.node import Node
import zmq
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class ImagePublisherZMQ(Node):
    def __init__(self):
        super().__init__('image_publisher_zmq')

        # ZeroMQ для отправки изображений
        zmq_pub_ip = "127.0.0.1"
        zmq_pub_port = "...."

        self.zmq_context = zmq.Context()
        # допишите код ...
        # создайте сокет типа pub
        self.socket.setsockopt(zmq.CONFLATE, 1)
        self.socket.bind(f"tcp://{zmq_pub_ip}:{zmq_pub_port}")

        # Подписка на изображения
        self.image_subscription = self.create_subscription(
            Image,
            '...',
            self.image_callback,
            10
        )

        self.bridge = CvBridge()
        self.get_logger().info("ZeroMQ Image Publisher Initialized")

    def image_callback(self, msg: Image):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        # Кодируем в JPEG
        ok, buffer = cv2.imencode('.jpg', cv_image)
        if not ok:
            self.get_logger().error("Failed to encode image to JPEG")
            return

        # Отправляем только JPEG-байты
        try:
            self.socket.send(buffer.tobytes(), flags=zmq.NOBLOCK)
        except zmq.ZMQError as e:
            self.get_logger().error(f"Failed to send image via ZeroMQ: {e}")
            return

        self.get_logger().debug("Image sent via ZeroMQ")

    def destroy_node(self):
        try:
            self.socket.close()
            self.zmq_context.term()
        except Exception:
            pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    image_publisher = ImagePublisherZMQ()

    try:
        rclpy.spin(image_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        image_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()