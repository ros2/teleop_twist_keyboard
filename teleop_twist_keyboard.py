# Copyright 2011 Brown University Robotics.
# Copyright 2017 Open Source Robotics Foundation, Inc.
# All rights reserved.
#
# Software License Agreement (BSD License 2.0)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the Willow Garage nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import threading

import geometry_msgs.msg
import rclpy
import yaml
import rclpy.parameter

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


class KeyMapper:

    def __init__(self, mappings_file):
        self._mappings_file = mappings_file

        # Declare default lexical mappings
        self._key_mappings = {
            'speed_up': 'q',
            'speed_down': 'z',
            'linear_speed_up': 'w',
            'linear_speed_down': 'x',
            'angular_speed_up': 'e',
            'angular_speed_down': 'c',
            'forward': 'i',
            'forward_right': 'o',
            'turn_left': 'j',
            'turn_right': 'l',
            'forward_left': 'u',
            'backward': ',',
            'backward_right': '.',
            'backward_left': 'm',
            'forward_right_strafe': 'O',
            'forward_strafe': 'I',
            'strafe_left': 'J',
            'strafe_right': 'L',
            'forward_left_strafe': 'U',
            'backward_strafe': '<',
            'backward_right_strafe': '>',
            'backward_left_strafe': 'M',
            'up': 't',
            'down': 'b'
        }

        self.read_keymapping(mappings_file)

        self.create_bindings()

    def create_bindings(self):
        self._move_bindings = {
            self._key_mappings['forward']: (1, 0, 0, 0),
            self._key_mappings['forward_right']: (1, 0, 0, -1),
            self._key_mappings['turn_left']: (0, 0, 0, 1),
            self._key_mappings['turn_right']: (0, 0, 0, -1),
            self._key_mappings['forward_left']: (1, 0, 0, 1),
            self._key_mappings['backward']: (-1, 0, 0, 0),
            self._key_mappings['backward_right']: (-1, 0, 0, 1),
            self._key_mappings['backward_left']: (-1, 0, 0, -1),
            self._key_mappings['forward_right_strafe']: (1, -1, 0, 0),
            self._key_mappings['forward_strafe']: (1, 0, 0, 0),
            self._key_mappings['strafe_left']: (0, 1, 0, 0),
            self._key_mappings['strafe_right']: (0, -1, 0, 0),
            self._key_mappings['forward_left_strafe']: (1, 1, 0, 0),
            self._key_mappings['backward_strafe']: (-1, 0, 0, 0),
            self._key_mappings['backward_right_strafe']: (-1, -1, 0, 0),
            self._key_mappings['backward_left_strafe']: (-1, 1, 0, 0),
            self._key_mappings['up']: (0, 0, 1, 0),
            self._key_mappings['down']: (0, 0, -1, 0),
        }

        self._speed_bindings = {
            self._key_mappings['speed_up']: (1.1, 1.1),
            self._key_mappings['speed_down']: (.9, .9),
            self._key_mappings['linear_speed_up']: (1.1, 1),
            self._key_mappings['linear_speed_down']: (.9, 1),
            self._key_mappings['angular_speed_up']: (1, 1.1),
            self._key_mappings['angular_speed_down']: (1, .9),
        }

    def read_keymapping(self, file):
        if file is None:
            return

        with open(file, 'r') as f:
            config = yaml.safe_load(f)

        # Check there are not repeated values
        if len(list(config.values())) != len(set(config.values())):
            raise RuntimeError("Repeated keys in the yaml file.")

        self._key_mappings.update(config)

        # Check the new mappings don't have repeated values
        if len(list(self._key_mappings.values())) \
                != len(set(self._key_mappings.values())):
            raise RuntimeError("Repeated elements in the mappings.")

    def speed_bindings(self):
        return self._speed_bindings

    def move_bindings(self):
        return self._move_bindings

    def msg(self):
        return (
            '---------------------------\n'
            'Moving around:\n'
            f'{self._key_mappings["forward_left"]}    '
            f'{self._key_mappings["forward"]}    '
            f'{self._key_mappings["forward_right"]}\n'
            f'{self._key_mappings["turn_left"]}         '
            f'{self._key_mappings["turn_right"]}\n'
            f'{self._key_mappings["backward_left"]}    '
            f'{self._key_mappings["backward"]}    '
            f'{self._key_mappings["backward_right"]}\n'
            '\n'
            'For Holonomic mode (strafing), hold down the shift key:\n'
            '---------------------------\n'
            f'{self._key_mappings["forward_left_strafe"]}    '
            f'{self._key_mappings["forward_strafe"]}    '
            f'{self._key_mappings["forward_right_strafe"]}\n'
            f'{self._key_mappings["strafe_left"]}         '
            f'{self._key_mappings["strafe_right"]}\n'
            f'{self._key_mappings["backward_left_strafe"]}    '
            f'{self._key_mappings["backward_strafe"]}    '
            f'{self._key_mappings["backward_right_strafe"]}\n'
            '\n'
            f'{self._key_mappings["up"]} : up (+z)\n'
            f'{self._key_mappings["down"]} : down (-z)\n'
            '\n'
            'anything else : stop\n'
            '\n'
            f'{self._key_mappings["speed_up"]}/'
            f'{self._key_mappings["speed_down"]} : '
            'increase/decrease max speeds by 10%\n'
            f'{self._key_mappings["linear_speed_up"]}/'
            f'{self._key_mappings["linear_speed_down"]} : '
            'increase/decrease only linear speed by 10%\n'
            f'{self._key_mappings["angular_speed_up"]}/'
            f'{self._key_mappings["angular_speed_down"]} : '
            'increase/decrease only angular speed by 10%\n'
            '\n'
            'CTRL-C to quit\n')


def getKey(settings):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)


def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def vels(speed, turn):
    return 'currently:\tspeed %s\tturn %s ' % (speed, turn)


def main():
    settings = saveTerminalSettings()

    rclpy.init()

    node = rclpy.create_node('teleop_twist_keyboard')

    # parameters
    stamped = node.declare_parameter('stamped', False).value
    frame_id = node.declare_parameter('frame_id', '').value
    key_mappings_file = node.declare_parameter(
        'key_mappings_file', rclpy.parameter.Parameter.Type.STRING).value
    key_mapper = KeyMapper(key_mappings_file)

    moveBindings = key_mapper.move_bindings()
    speedBindings = key_mapper.speed_bindings()

    if not stamped and frame_id:
        raise Exception("'frame_id' can only be set when 'stamped' is True")

    if stamped:
        TwistMsg = geometry_msgs.msg.TwistStamped
    else:
        TwistMsg = geometry_msgs.msg.Twist

    pub = node.create_publisher(TwistMsg, 'cmd_vel', 10)

    spinner = threading.Thread(target=rclpy.spin, args=(node,))
    spinner.start()

    speed = 0.5
    turn = 1.0
    x = 0.0
    y = 0.0
    z = 0.0
    th = 0.0
    status = 0.0

    twist_msg = TwistMsg()

    if stamped:
        twist = twist_msg.twist
        twist_msg.header.stamp = node.get_clock().now().to_msg()
        twist_msg.header.frame_id = frame_id
    else:
        twist = twist_msg

    try:
        print(key_mapper.msg())
        print(vels(speed, turn))
        while True:
            key = getKey(settings)
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]

                print(vels(speed, turn))
                if (status == 14):
                    print(key_mapper.msg())
                status = (status + 1) % 15
            else:
                x = 0.0
                y = 0.0
                z = 0.0
                th = 0.0
                if (key == '\x03'):
                    break

            if stamped:
                twist_msg.header.stamp = node.get_clock().now().to_msg()

            twist.linear.x = x * speed
            twist.linear.y = y * speed
            twist.linear.z = z * speed
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = th * turn
            pub.publish(twist_msg)

    except Exception as e:
        print(e)

    finally:
        if stamped:
            twist_msg.header.stamp = node.get_clock().now().to_msg()

        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        pub.publish(twist_msg)
        rclpy.shutdown()
        spinner.join()

        restoreTerminalSettings(settings)


if __name__ == '__main__':
    main()
