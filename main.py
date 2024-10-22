import serial.tools.list_ports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

class SerialPortApp(App):
    def build(self):
        self.selected_port = None

        # Main layout
        self.layout = BoxLayout(orientation='vertical')

        # Spinner for serial ports selection
        self.spinner = Spinner(text="Select COM Port", size_hint=(1, 0.2))

        # List all serial ports and add them to spinner options
        ports = self.list_serial_ports()
        if ports:
            self.spinner.values = [port.device for port in ports]
        else:
            self.spinner.text = "No COM Ports Found"

        # Bind event when selecting a port
        self.spinner.bind(text=self.on_port_selected)

        # Button to confirm the selection and connect
        self.button = Button(text="Connect", size_hint=(1, 0.2))
        self.button.bind(on_press=self.connect_to_port)

        # Label to show the selected port
        self.label = Label(text="No Port Selected", size_hint=(1, 0.2))

        # Add widgets to layout
        self.layout.add_widget(self.spinner)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.label)

        return self.layout

    def list_serial_ports(self):
        # Lists all available serial ports
        ports = list(serial.tools.list_ports.comports())
        return ports

    def on_port_selected(self, spinner, text):
        # Event handler when a port is selected
        self.selected_port = text
        self.label.text = f"Selected Port: {self.selected_port}"

    def connect_to_port(self, instance):
        # Function to connect to the selected port
        if self.selected_port:
            self.label.text = f"Connecting to {self.selected_port}..."
            # Here you can open the serial connection
            # You can extend this to open the port and read/write data
            try:
                ser = serial.Serial(self.selected_port, 115200, timeout=1)
                self.label.text = f"Connected to {self.selected_port}"
                ser.close()  # Close after testing
            except serial.SerialException as e:
                self.label.text = f"Failed to connect: {str(e)}"
        else:
            self.label.text = "No Port Selected"

if __name__ == "__main__":
    SerialPortApp().run()
