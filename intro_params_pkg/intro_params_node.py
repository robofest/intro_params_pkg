import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class HelloWorldNode(Node):
    def __init__(self):
        super().__init__('intro_params_node')

        # 1. Declare parameters with default values
        # (These defaults are overridden if parameters are passed via the command line)
        self.declare_parameter('message', 'Hello World to test Params')
        self.declare_parameter('frequency', 1.0) # Frequency in Hz

        # 2. Read initial values
        self.message = self.get_parameter('message').value
        frequency = self.get_parameter('frequency').value
        # --- Guard against zero or negative frequencies at startup ---
        if frequency <= 0.0:
            self.get_logger().fatal(
                f"Invalid frequency configuration: {frequency} Hz. "
                "Frequency must be strictly greater than 0.0. Terminating node!"
            )
            # Raising an exception here cleanly halts initialization
            raise RuntimeError(f"Invalid initial frequency: {frequency}")
        
        # Calculate initial period
        self.timer_period = 1.0 / frequency

        # 3. Create the timer
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # 4. Add a callback to handle dynamic parameter updates at runtime
        self.add_on_set_parameters_callback(self.parameter_callback)
       
        self.get_logger().info(f"Node started. Msg: '{self.message}', Freq: {frequency}Hz")

    def timer_callback(self):
        # Always prints the current message variable
        # self.message = self.get_parameter('message').value
        self.get_logger().info(self.message)

    def parameter_callback(self, params):
        """This function triggers whenever a parameter is changed via ROS2 CLI"""
        for param in params:
            # Handle message change
            if param.name == 'message' and param.type_ == param.Type.STRING:
                self.message = param.value
                self.get_logger().info(f"Updated message to: '{self.message}'")
            
            # Handle frequency change. Allow only DOUBLE type
            elif param.name == 'frequency' and param.type_ == param.Type.DOUBLE:
                new_frequency = param.value  # No float() conversion needed since it's guaranteed to be a double
    
                if new_frequency <= 0.0:
                    return SetParametersResult(successful=False, reason="Frequency must be greater than 0")
    
                # Update the timer period directly in nanoseconds
                # 1 second = 1,000,000,000 nanoseconds
                new_period_ns = int((1.0 / new_frequency) * 1e9) 
                self.timer.timer_period_ns = new_period_ns
                self.timer.reset()
    
                self.get_logger().info(f"Successfully updated frequency to {new_frequency} Hz")
                
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args) # This parses any command line arguments passed to the ROS2 ecosystem
    node = HelloWorldNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()