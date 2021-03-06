import serial


class PressureSender:
    def __init__(self):
        self._water_level = 0
        self._set = False
        self._ser = -1
        self._water_density = 997  # default

    def get_state(self):
        return self._set

    def get_water_level(self, water_temperature):

        if self._set == False:
            try:
                self._ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
                self._ser.reset_input_buffer()
                self._ser.readline()
                self._set = True
            except:
                self._set = False
                self._water_level = -1
                return self._water_level

        offset = 5

        try:
            value = float(self._ser.readline().decode().strip('\r\n'))
            if value == 0:
                return self._water_level
        except:
            return self._water_level

        if(value < 0.5):
            value = 0.5
            offset = 0

        elif(water_temperature != -85):

            # Water's density is calculated with Kell's formula, should be valid for 0-150'C

            self._water_density = (999.83952+16.945176*water_temperature-(7.987040*10**-3)*water_temperature**2-(46.170461*10**-6)*water_temperature**3 +
                                   (105.56302*10**-9)*water_temperature**4-(280.54253*10**-12)*water_temperature**5)/(1+16.897850*10**-3*water_temperature)

        psi = 5*(value-0.5)/(4.5-0.5)
        pa = psi*6894.76  # 1 psi is 6894.76 pascals
        h_cm = 100*(pa / (self._water_density*9.81)) + offset
        self._water_level = format(h_cm, '.1f')
        return self._water_level
