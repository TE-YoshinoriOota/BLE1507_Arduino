# notify_central.py
# MIT License
# 
# Copyright (c) 2024 Yoshinori Oota
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import time
import struct
import argparse
import concurrent.futures
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.exc import BleakError

char_uuid = "4a02" # default
timeout = 10
data = 0


#
# connect to the base altimeter and handling notifications
#
async def connect_and_write(address, name, uuid):

  if uuid:
    global char_uuid
    char_uuid = uuid

  while True:
    try:
      if address:
        device = await BleakScanner.find_device_by_address(address)
        if device is None:
          print(f"Could not find device with address : {address}")
        else:
          print(f"Device {address} found")
      else:
        device = await BleakScanner.find_device_by_name(name)
        if device is None:
          print(f"Could not find device with name : {name}")
        else:
          print(f"Device {name} found")

      async with BleakClient(device) as client:
        try:              
          if client.is_connected:
            print(f"Already connected to {device.name}")
            while True:
              try: 
                global data
                str_data = str(data)
                await client.write_gatt_char(char_uuid, str_data.encode('utf-8')) 
                print(f"write : {str_data}")
                data = data + 1 
                data = data % 100
              except Exception as e:
                if "Insufficient Authentication" in str(e):
                  print(f"Warning: Insufficient Authentication. Please ensure that {device.name} is properly paired") 
                else:
                  print(f"An error occurred: {e}")
                  print(f"(re)try to connect {name}")
                  break;

              await asyncio.sleep(1)
          else:
            try:
              print(f"Try to connect {address}")
              await asyncio.wait_for(client.connect(), timeout)
              if client.is_connected:
                print(f"Connected to {address}")
              else:
                print(f"Failed to connect {address}")                        

            except asyncio.TimeoutError:
              print(f"Timout retry to connect {address}")

        except Exception as e:
          print(f"Connection lost with {address} : {e}")
          print(f"Warning: Please ensure that {address} is properly paired") 

        finally:
          try:
            await client.stop_notify(char_uuid)
          except BleakError as e:
            print(f"Stop notify error: {e}")

    except BleakError as e:
      print(f"BleakError: {e}")
      print("(re)try to connect to {address}")

    except Exception as e:
      print(f"Unexpected error: {e}")
      print("Terminate this process")
      break

    await asyncio.sleep(1)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  device_group = parser.add_mutually_exclusive_group(required=True)
  device_group.add_argument(
      "--name",
      metavar="<name>",
      help="the name of the buletooth device to connect to",
    )
  device_group.add_argument(
      "--address",
      metavar="<address>",
      help="the address of the buletooth device to connect to",
    )
  parser.add_argument("--uuid", type=str, default="4a02", help="the characteristic uuid for the altimeter devices")

  args = parser.parse_args()
  if args.address:
    print(f"the BLE1507 address is {args.address}")
  if args.name:
    print(f"the BLE1507 name is {args.name}")
  if args.uuid:
    print(f"the characteristic uuid is {args.uuid}")

  asyncio.run(connect_and_write(args.address, args.name, args.uuid))
