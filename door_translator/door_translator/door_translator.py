#!/usr/bin/env python3

from __future__ import division  # support for python2
import sys
sys.path.insert(0, "..")

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from rmf_msgs.msg import DoorState
from opcua import Client, ua
from threading import Thread, Condition
from datetime import datetime
import concurrent.futures
import logging
import json
import threading
import time
import configparser
import os
try:
    from urllib.parse import urlparse
except ImportError:  # support for python2
    from urlparse import urlparse
from opcua.common.node import Node
from opcua.common.manage_nodes import delete_nodes
use_crypto = True
try:
    from opcua.crypto import uacrypto
except ImportError:
    logging.getLogger(__name__).warning("cryptography is not installed, use of crypto disabled")
    use_crypto = False




class DoorTranslator(Node):
    """This class methods are called whenever there is a xmlrpc request from the AGV"""
    def __init__(self):
        super().__init__("door_translator")
        self.is_connected = False
        self.connect_response = 1
        self.response = 1
        self.door_status_ = False
        # Type the URL
        self.opc_server_url = "opc:tcp://10.233.29.29:21381"
        self.general_timeout = 30
        self.timer_publish_period = 2

    #     try:
    #         #todo: Change to ROS parameter
    #         # Initialising the config file 
    #         self.msg = DoorState()
    #         self.door_id = self.msg.door_name
    #         self.door_state_publisher_ = self.create_publisher(DoorState, 'door_request_topic', 10)
    #         self.timer_publish_event = self.create_timer(self.timer_publish_period, self.timer_publish_callback)
    #         self.door_state_subscriber = self.create_subscription(DoorState, 'door_state_topic', self.call_back_method, 10)
    #         # self.parameters_parser = configparser.RawConfigParser()
    #         # self.parameters_parser.readfp(open('parameters.config')) 
    #         self.opc_connect()
    #         # self.testing_phase = self.parameters_parser.get('Kone_OPC_parameters','testing_phase')
    #         # logging.info("self.testing_phase = {}".format(self.testing_phase))
    #     except Exception as err_:
    #         logging.info("Issue while opening the parameters file. Error: {}".format(err_))
    #         raise

    # #======================================================================================================================================
    # #
    # #                                           opc_connect() method
    # #
    # #=======================================================================================================================================

    # def opc_connect(self):
    #     """This method connects to the OPC Tunneller whose opc_server_url is obtained from the config file"""
    #     try:
    #         self.client = Client(self.opc_server_url)
    #         self.client.connect()
    #         logging.info("Client is connected to the OPC Server")
    #         self.connect_response = 0
    #         self.is_connected = True
    #     except Exception as err_:
    #         logging.info("Exception occured while connecting to OPC Server. Error: {}".format(err_))
    #         self.connect_response = 1
    #         self.is_connected = False
    #         raise

    # #======================================================================================================================================
    # #
    # #                                           opc_disconnect() method
    # #
    # #=======================================================================================================================================
       
    # def opc_disconnect(self):
    #     """This method disconnects the OPC client from the OPC Tunneller"""
    #     try:
    #         self.client.disconnect()
    #         # raise Exception('test')
    #     except Exception as errors:
    #         logging.error("Disconnect not successful: {}".format(errors))
    #     finally:
    #         self.is_connected = False
    
    
    # #======================================================================================================================================
    # #
    # #                                           opc_write_Bool() method
    # #
    # #=======================================================================================================================================

    # # def opc_write_Bool(self, rmf_msg):
    # #     """This method writes values to the opc_attribute"""
    # #     try:
    # #         set_val_=self.client.get_node(self.msg.door_name)
    # #         set_val_.set_value(ua.DataValue(ua.Variant(write_value, ua.VariantType.Boolean)))
    # #     except Exception as err_:
    # #         logging.info("Error: {}".format(err_))
    # #         self.response = 1
    # #         self.opc_disconnect()
    # #         raise

    # #======================================================================================================================================
    # #
    # #                                           opc_read() method
    # #
    # #=======================================================================================================================================

    # def opc_read(self, lift_id_, opc_attribute_):
    #     """This method reads values from the opc_attribute"""
    #     try:
    #         lift_id_path = self.parameters_parser.get('Kone_OPC_parameters',lift_id_)
    #         return self.client.get_node(lift_id_path + "." + opc_attribute_)
    #     except Exception as err_:
    #         logging.info("Error: {}".format(err_))
    #         self.response = 1
    #         self.opc_disconnect()
    #         raise

    # #======================================================================================================================================
    # #
    # #                                           check_timeout() method
    # #
    # #=======================================================================================================================================

    # def check_timeout(self, start_time):
    #     """This method checks for the timeout which is tunable in the config file"""
    #     time_delta = datetime.now() - start_time
    #     if (time_delta.total_seconds() >= int(self.general_timeout)):
    #         return True
    #     else:
    #         return False

    # def timer_publish_callback(self):
    #     self.msg.door_name = self.door_id
    #     self.msg.door_state = self.door_status_
    #     self.publisher_.publish(self.msg)
    #     self.get_logger().info("Publishing data")


    # def call_back_method(self, rmf_msg):
        # if not(self.is_connected):
        #     self.opc_connect()
        # if(self.is_connected):
        #     self.get_logger().info("OPC Server is connected")
        #     self.door_id = rmf_msg.door_name
        #     set_val_=self.client.get_node(rmf_msg.door_name)
        #     set_val_.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
        #     if(rmf_msg.door_state == rmf_msg.DOOR_OPEN):
        #         set_val_=self.client.get_node(DoorOpenCommand)
        #         set_val_.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
        #         self.get_logger().info("Setting True on Door Open => Door Open Command Set")
        #         start_time = datetime.now()
        #         self.door_status_ = self.client.get_node(DoorStatus)
        #         while not (self.door_status_):
        #                 self.get_logger().info("Timeout!!")
        #                 break
        #     elif(rmf_msg.door_state == rmf_msg.DOOR_CLOSED):
        #         set_val_=self.client.get_node(DoorCloseCommand)
        #         set_val_.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
        #         self.get_logger().info("Setting True on Door Close => Door Close Command Set")
        #         start_time = datetime.now()
        #         self.door_status_ = self.client.get_node(DoorStatus)
        #         while(self.door_status_):
        #             if(self.check_timeout(start_time)):
        #                 self.get_logger().info("Timeout!!")
        #                 break
        # else:
        #     self.get_logger().info("Couldn't connect to OPC Server")
            

def main(args=None):
    rclpy.init(args=args)

    door_translator = DoorTranslator()

    rclpy.spin(door_translator)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    door_translator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()