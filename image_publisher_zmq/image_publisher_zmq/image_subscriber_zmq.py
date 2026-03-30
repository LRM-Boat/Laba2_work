#!/usr/bin/env python3
"""
Допишите код для приема изображений
"""

import rclpy


class ZMQSyncNode(Node):

    def __init__(self):
        super().__init__('zmq_sync_node')

def main(args=None):
    rclpy.init(args=args)
    node = ZMQSyncNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
