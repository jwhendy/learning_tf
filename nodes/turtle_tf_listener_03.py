#!/usr/bin/env python

## Learning about tf and time (Python)
## http://wiki.ros.org/tf/Tutorials/tf%20and%20Time%20%28Python%29
## from Sec 2 where waitForTransform() is introduced

import rospy
import tf
import turtlesim.srv
import geometry_msgs.msg
import math

if __name__ == '__main__':
    rospy.init_node('tf_turtle')

    listener = tf.TransformListener()

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4, 2, 0, 'turtle2')

    turtle_vel = rospy.Publisher('turtle2/cmd_vel',
                                 geometry_msgs.msg.Twist,
                                 queue_size=1)

    rate = rospy.Rate(10.0)

    listener.waitForTransform('/turtle2', '/carrot1', rospy.Time(), rospy.Duration(4.0))
    while not rospy.is_shutdown():
        try:
            now = rospy.Time.now()
            listener.waitForTransform('/turtle2', '/carrot1', now, rospy.Duration(4.0))
            (trans, rot) = listener.lookupTransform('/turtle2',
                                                    '/carrot1',
                                                    now)
        ## except(tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        except(tf.LookupException, tf.ConnectivityException):
            
            continue

        angular = 4 * math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)

        rate.sleep()
