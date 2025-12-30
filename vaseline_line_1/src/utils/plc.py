# import logging
# from datetime import datetime
# import snap7
# import snap7.util

# class PLC:
#     """
#     Manages connection and communication with Siemens PLC using Snap7.
#     Supports triggering both a primary bit and a recipe bit.
#     """

#     def __init__(self, plc_ip, rack, slot, db_number,
#                  start_offset, bit_offset,
#                  recipe_start_offset, recipe_bit_offset,
#                  value=True):

#         self.plc_ip = plc_ip
#         self.rack = rack
#         self.slot = slot
#         self.db_number = db_number

#         # Primary trigger
#         self.start_offset = start_offset
#         self.bit_offset = bit_offset

#         # Recipe trigger
#         self.recipe_start_offset = recipe_start_offset
#         self.recipe_bit_offset = recipe_bit_offset

#         self.value = value

#     # --------------------------------------------------------
#     # Connection Handling
#     # --------------------------------------------------------
#     def initialize_plc_connection(self):
#         try:
#             plc = snap7.client.Client()
#             plc.connect(self.plc_ip, self.rack, self.slot)

#             if plc.get_connected():
#                 logging.info(f"Connected to PLC at {self.plc_ip}")
#                 return plc
#             else:
#                 logging.error("PLC connection failed.")
#                 return None

#         except Exception as e:
#             logging.error(f"PLC connection error: {e}")
#             return None

#     def reset_plc(self, plc):
#         try:
#             if plc:
#                 plc.disconnect()

#             logging.warning("Reconnecting to PLC...")
#             plc = snap7.client.Client()
#             plc.connect(self.plc_ip, self.rack, self.slot)

#             if plc.get_connected():
#                 logging.info("PLC reconnected successfully.")
#                 return plc

#             logging.error("PLC reconnection failed.")
#             return None

#         except Exception as e:
#             logging.error(f"PLC reconnection error: {e}")
#             return None

#     # --------------------------------------------------------
#     # Bit Writer
#     # --------------------------------------------------------
#     def _write_bit(self, plc, byte_offset, bit_offset):
#         try:
#             # logging.info(f"PLC Stuff: {dir(plc)}")
#             # if not plc.get_connected():
#             #     plc = self.reset_plc(plc)
#             #     if plc is None:
#             #         return None

#             # Read 1 byte from DB
#             data = plc.db_read(self.db_number, byte_offset, 1)

#             # Modify single bit
#             snap7.util.set_bool(data, 0, bit_offset, self.value)

#             # Write back
#             plc.db_write(self.db_number, byte_offset, data)

#             ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
#             logging.info(
#                 f"[{ts}] PLC Write -> DB{self.db_number} Byte {byte_offset} Bit {bit_offset} = {self.value}"
#             )

#         except Exception as e:
#             logging.error(f"PLC write error: {e}")
#             plc = self.reset_plc(plc)

#         return plc

#     # --------------------------------------------------------
#     # Public Bit Triggers
#     # --------------------------------------------------------
#     def trigger_plc(self, plc):
#         return self._write_bit(plc, self.start_offset, self.bit_offset)

#     def trigger_recipe(self, plc):
#         return self._write_bit(plc, self.recipe_start_offset, self.recipe_bit_offset)

#     def trigger_both(self, plc):
#         """Trigger both primary and recipe bits."""
#         self.trigger_plc(plc)      
#         self.trigger_recipe(plc)
#         return plc

# if __name__ == "__main__":
#     plc_ip = '192.168.21.10'
#     # # self.data_collection = (
#     # #     r"Z:\Data_collection\ocr_line_2"
#     # )
#     rack = 0
#     slot = 1
#     db_number = 1
#     start_offset = 1
#     bit_offset = 0

#     plc = PLC(plc_ip, rack, slot, db_number, start_offset, bit_offset,2, 0, value=True)

#     actual_plc = plc.initialize_plc_connection()
#     import time

#     for i in range(10):
#         actual_plc.get_connected()
#         plc.value = True
#         actual_plc = plc.trigger_both(actual_plc)

#         time.sleep(1)
#         actual_plc.get_connected()
#         plc.value = False
#         actual_plc = plc.trigger_plc(actual_plc)

#         time.sleep(1)
#         break

import logging
from datetime import datetime
import snap7
import snap7.util

class PLC:
    """
    Manages connection and communication with Siemens PLC using Snap7.
    Supports triggering both a primary bit and a recipe bit.
    """

    def __init__(self, plc_ip, rack, slot, db_number,
                 start_offset, bit_offset,
                 recipe_start_offset, recipe_bit_offset,
                 value=True):

        self.plc_ip = plc_ip
        self.rack = rack
        self.slot = slot
        self.db_number = db_number

        # Primary trigger
        self.start_offset = start_offset
        self.bit_offset = bit_offset

        # Recipe trigger
        self.recipe_start_offset = recipe_start_offset
        self.recipe_bit_offset = recipe_bit_offset

        self.value = value

        self.plc = None

    # --------------------------------------------------------
    # Connection Handling
    # --------------------------------------------------------
    def initialize_plc_connection(self):
        try:
            plc = snap7.client.Client()
            plc.connect(self.plc_ip, self.rack, self.slot)

            if plc is not None:
                if plc.get_connected():
                    logging.info(f"Connected to PLC at {self.plc_ip}")
                    self.plc = plc
                    return plc
                else:
                    logging.error("PLC connection failed.")
                    return None
            else:
                logging.error("PLC connection failed.")
                return None

        except Exception as e:
            logging.error(f"PLC connection error: {e}")
            return None

    def reset_plc(self, plc):
        try:
            if self.plc:
                self.plc.disconnect()

            logging.warning("Reconnecting to PLC...")
            plc = snap7.client.Client()
            plc.connect(self.plc_ip, self.rack, self.slot)

            if plc is not None:
                if plc.get_connected():
                    logging.info("PLC reconnected successfully.")
                    self.plc = plc
                    return plc
            self.plc = None

            logging.error("PLC reconnection failed.")
            return None

        except Exception as e:
            logging.error(f"PLC reconnection error: {e}")
            return None

    # --------------------------------------------------------
    # Bit Writer
    # --------------------------------------------------------
    def _write_bit(self, plc, byte_offset, bit_offset):
        try:
            if self.plc is not None:
                plc = self.plc
                if not plc.get_connected():
                    plc = self.reset_plc(plc)
                    if plc is None:
                        self.plc = None
                        return None
            plc = self.plc
            # Read 1 byte from DB
            data = plc.db_read(self.db_number, byte_offset, 1)

            # Modify single bit
            snap7.util.set_bool(data, 0, bit_offset, self.value)

            # Write back
            plc.db_write(self.db_number, byte_offset, data)

            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            logging.info(
                f"[{ts}] PLC Write -> DB{self.db_number} Byte {byte_offset} Bit {bit_offset} = {self.value}"
            )

        except Exception as e:
            logging.error(f"PLC write error: {e}")
            plc = self.reset_plc(plc)

        return plc

    # --------------------------------------------------------
    # Public Bit Triggers
    # --------------------------------------------------------
    def trigger_plc(self, plc):
        return self._write_bit(plc, self.start_offset, self.bit_offset)

    def trigger_recipe(self, plc):
        return self._write_bit(plc, self.recipe_start_offset, self.recipe_bit_offset)

    def trigger_both(self, plc):
        """Trigger both primary and recipe bits."""
        plc = self.trigger_plc(plc)      
        plc = self.trigger_recipe(plc)
        return plc