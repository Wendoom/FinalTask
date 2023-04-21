#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Header
from geometry_msgs.msg import Vector3

rospy.init_node('imu_publisher')

imu_pub = rospy.Publisher('/imu', Imu, queue_size=10)

rate = rospy.Rate(10) # 10hz

header = Header(frame_id='base_link')

imu = Imu()
imu.header = header

linear_acceleration = Vector3()
angular_velocity = Vector3()

# initialize sensor values
accel_x = 0.0
accel_y = 0.0
accel_z = 9.8
gyro_x = 0.0
gyro_y = 0.0
gyro_z = 0.0

# filter coefficients
alpha = 0.5
beta = 1.0 - alpha

start_time = rospy.Time.now()

while not rospy.is_shutdown():

    elapsed_time = (rospy.Time.now() - start_time).to_sec()

    # generate accelerometer data
    accel_x = 0.5 * accel_x + 0.5 * (2.0 * (elapsed_time ** 2.0) + 3.0 * elapsed_time + 1.0)
    accel_y = 0.5 * accel_y + 0.5 * (3.0 * (elapsed_time ** 2.0) + 2.0 * elapsed_time + 1.0)
    accel_z = 0.5 * accel_z + 0.5 * (4.0 * (elapsed_time ** 2.0) + 1.0)

    # generate gyroscope data
    gyro_x = 0.5 * gyro_x + 0.5 * (2.0 * elapsed_time + 1.0)
    gyro_y = 0.5 * gyro_y + 0.5 * (3.0 * elapsed_time + 2.0)
    gyro_z = 0.5 * gyro_z + 0.5 * (4.0 * elapsed_time + 3.0)

    # # add noise to the sensor values
    # accel_x += 0.05 * (2.0 * rospy.get_param("/accel_noise") - 1.0)
    # accel_y += 0.05 * (2.0 * rospy.get_param("/accel_noise") - 1.0)
    # accel_z += 0.05 * (2.0 * rospy.get_param("/accel_noise") - 1.0)
    # gyro_x += 0.01 * (2.0 * rospy.get_param("/gyro_noise") - 1.0)
    # gyro_y += 0.01 * (2.0 * rospy.get_param("/gyro_noise") - 1.0)
    # gyro_z += 0.01 * (2.0 * rospy.get_param("/gyro_noise") - 1.0)

    # correct the sensor values using a complementary filter
    # imu.linear_acceleration.x = alpha * imu.linear_acceleration.x + beta * accel_x
    # linear_acceleration.y = alpha * imu.linear_acceleration.y + beta * accel_y
    # linear_acceleration.z = alpha * imu.linear_acceleration.z + beta * accel_z - 9.8

    # imu.angular_velocity.x = alpha * angular_velocity.x + beta * gyro_x
    # imu.angular_velocity.y = alpha * angular_velocity.y + beta * gyro_y
    # imu.angular_velocity.z = alpha * angular_velocity.z + beta * gyro_z


    imu.header.stamp = rospy.Time.now()
    imu.header.frame_id = 'imu_link'
    imu.linear_acceleration.x = alpha * imu.linear_acceleration.x + beta * accel_x
    linear_acceleration.y = alpha * imu.linear_acceleration.y + beta * accel_y
    linear_acceleration.z = alpha * imu.linear_acceleration.z + beta * accel_z - 9.8

    imu.angular_velocity.x = alpha * angular_velocity.x + beta * gyro_x
    imu.angular_velocity.y = alpha * angular_velocity.y + beta * gyro_y
    imu.angular_velocity.z = alpha * angular_velocity.z + beta * gyro_z

    imu_pub.publish(imu)
    rate.sleep()