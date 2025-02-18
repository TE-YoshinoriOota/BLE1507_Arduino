/*
 * BLE1507_write.ino
 * Copyright (c) 2024 Yoshinori Oota
 *
 * This is an example of BLE1507
 *
 * This is a free software; you can redistribute it and/or
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


/****************************************************************************
 * Included Files
 ****************************************************************************/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "BLE1507.h"

/****************************************************************************
 * Pre-processor Definitions
 ****************************************************************************/

#define UUID_SERVICE  0x3802
#define UUID_CHAR     0x4a02

/****************************************************************************
 * ble parameters
 ****************************************************************************/
static BT_ADDR addr = {{0x19, 0x84, 0x06, 0x14, 0xAB, 0xCD}};
static char ble_name[BT_NAME_LEN] = "SPR-PERIPHERAL";

BLE1507 *ble1507;


/****************************************************************************
 * ble write callback function
 ****************************************************************************/

void BleCB(struct ble_gatt_char_s *ble_gatt_char) {
  printf("write_callback!\n");
  printf("value : ");
  printf("%s", &ble_gatt_char->value.data[0]);
  printf("\n");
}


void setup() {
  ble1507 = BLE1507::getInstance();
  ble1507->begin(ble_name, addr, UUID_SERVICE, UUID_CHAR);
  ble1507->setWriteCallback(BleCB);
}

void loop() {

}
