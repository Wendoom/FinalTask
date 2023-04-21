#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
import numpy as np

# Define the frequency of the IMU data
freq = 100

# Define the initial values of the accelerometer and gyroscope
accel_init = np.array([0, 0, 9.8])
gyro_init = np.array([0, 0, 0])


# Define the correction matrices for the accelerometer and gyroscope
accel_correction = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
gyro_correction = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

# Define the ROS node and publisher
rospy.init_node('imu_generator')
pub = rospy.Publisher('imu/data', Imu, queue_size=10)

k = 0

# Define the loop that generates and publishes the IMU data
start_time = rospy.get_time()
rate = rospy.Rate(freq)
while not rospy.is_shutdown() and rospy.get_time() - start_time < 10.0:
     
    # Generate the accelerometer and gyroscope values
    k += 0.001
    accel = accel_init + np.array([k,k,0])
    gyro = gyro_init + np.array([k,k,k])

    # Apply the correction matrices to the accelerometer and gyroscope
    accel_corr = np.dot(accel_correction, accel)
    gyro_corr = np.dot(gyro_correction, gyro)

    # Create the IMU message and populate it with the data
    imu_msg = Imu()
    imu_msg.header.stamp = rospy.Time.now()
    imu_msg.header.frame_id = 'imu_link'
    imu_msg.linear_acceleration.x = accel_corr[0]
    imu_msg.linear_acceleration.y = accel_corr[1]
    imu_msg.linear_acceleration.z = accel_corr[2]
    imu_msg.angular_velocity.x = gyro_corr[0]
    imu_msg.angular_velocity.y = gyro_corr[1]
    imu_msg.angular_velocity.z = gyro_corr[2]

    # Publish the IMU message
    pub.publish(imu_msg)

    # Sleep to maintain the frequency
    rate.sleep()