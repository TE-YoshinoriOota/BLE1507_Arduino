/*
 * BLE1507.h
 * Copyright (c) 2024 Yoshinori Oota
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

#ifndef BLE1507_HEADER_GUARD__
#define BLE1507_HEADER_GUARD__

#include <bluetooth/ble_gatt.h>

#define BONDINFO_FILENAME "/mnt/spif/BONDINFO"

typedef void (*NotifyCallback)(struct ble_gatt_char_s*);
typedef void (*WriteCallback)(struct ble_gatt_char_s*);
typedef void (*ReadCallback)(struct ble_gatt_char_s*);

/****************************************************************************
 * helper wrapper class definition
 ****************************************************************************/
class BLE1507 {
  private:
    BLE1507();
    ~BLE1507();
  public:
    static BLE1507* getInstance() {
      if (theInstance == nullptr) {
        theInstance = new BLE1507();
      }
      return theInstance;
    }
    bool begin(char *ble_name, BT_ADDR addr, uint32_t uuid_service, uint32_t uuid_char);
    bool writeNotify(uint8_t data[], uint32_t data_size);
    bool is_ble_notify_enabled();
    void setNotifyCallback(NotifyCallback notify_cb);
    void setWriteCallback(WriteCallback write_cb);
    void setReadCallback(ReadCallback read_cb);
    bool removeBondInfo();

  private:
    static BLE1507 *theInstance;
};




#endif // BLE1507_HEADER_GUARD__
