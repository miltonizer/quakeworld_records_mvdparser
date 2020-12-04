import struct


class NetMessage:
    MAX_SIZE = 8192

    def __init__(self):
        self.data = None
        self.message_type = None
        self.current_size = None
        self.bad_read = False
        self.read_count = 0

    def increase_read_count(self, by_value):
        self.read_count += by_value

    def read_and_set_message_type_from_byte(self, byte):
        self.message_type = byte[0] & 7

    def read_char(self):
        if self.read_count + 1 > self.current_size:
            self.bad_read = True
            return -1
        self.read_count += 1
        return self.data[self.read_count-1]

    def read_byte(self):
        if self.read_count + 1 > self.current_size:
            self.bad_read = True
            return -1
        self.read_count += 1
        return self.data[self.read_count-1]

    def read_short(self):
        if self.read_count + 2 > self.current_size:
            self.bad_read = True
            return -1
        part1 = self.data[self.read_count]
        part2 = self.data[self.read_count + 1]
        part2_shifted = part2 << 8
        short_integer = self.data[self.read_count] + (self.data[self.read_count + 1] << 8)
        self.read_count += 2
        return short_integer

    def read_long(self):
        if self.read_count + 4 > self.current_size:
            self.bad_read = True
            return -1
        long_integer = (self.data[self.read_count] << 0) + (self.data[self.read_count + 1] << 8) + (self.data[self.read_count + 2] << 16) + (self.data[self.read_count + 3] << 24)
        self.read_count += 4
        return long_integer

    def read_float(self):
        if self.read_count + 4 > self.current_size:
            self.bad_read = True
            return -1
        float_value = struct.unpack('<f', self.data[self.read_count:self.read_count+4])
        self.read_count += 4
        return float(float_value[0])

    def read_string(self):
        string_array = []
        while True:
            byte = self.read_byte()

            if byte == 255:
                # This could cause security problems in older clients and servers, apparently.
                continue
            elif byte == -1 or byte == 0:
                # End of string or message bad read
                break
            string_array.append(chr(byte))
            if len(string_array) >= 2048:
                break

        return string_array

    def read_coord(self, mvd):
        if mvd.big_coords_enabled:
            return self.read_float()
        return self.read_short() * (1.0 / 8)

    def read_angle(self, mvd):
        if mvd.big_coords_enabled:
            return self.read_angle_16()
        return self.read_char() * (360.0 / 256)

    def read_angle_16(self):
        return self.read_short() * (360.0 / 65536)
