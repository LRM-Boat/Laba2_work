#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, LaserScan
from message_filters import Subscriber, ApproximateTimeSynchronizer


class CameraLaserSyncNode(Node):
    def __init__(self):
        super().__init__('camera_laser_sync_node')

        # Подписка на топики
        # Оформите подписку на топики изображения и лазерного сканера
        self.image_sub = Subscriber(self, Image, '...')
        self.scan_sub = Subscriber(self, LaserScan, '...')

        # Синхронизатор по времени
        # Допишите его
        # Максимальная разница по времени между топиками не более 0.05 сек.
        self.ts = ApproximateTimeSynchronizer(
            [...],
            
        )
        self.ts.registerCallback(self.sync_callback)

        # Публикация синхронизированных данных
        self.image_pub = self.create_publisher(Image, '....', 10)
        self.scan_pub = self.create_publisher(LaserScan, '....', 10)

        self.get_logger().info('Camera-Laser synchronizer started')

    def sync_callback(self, image_msg: Image, scan_msg: LaserScan):

        self.image_pub.publish(image_msg)
        self.scan_pub.publish(scan_msg)

        img_t = image_msg.header.stamp.sec + image_msg.header.stamp.nanosec * 1e-9
        scan_t = scan_msg.header.stamp.sec + scan_msg.header.stamp.nanosec * 1e-9
        dt = abs(img_t - scan_t)

        self.get_logger().info(
            f'Synced pair published. |dt| = {dt:.4f} s'
        )


def main(args=None):
    rclpy.init(args=args)
    node = CameraLaserSyncNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()