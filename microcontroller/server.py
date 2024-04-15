import machine
import network
import socket
import uasyncio

from PinDefinitions import button_led_pin, green_led_pin, orange_led_pin, red_led_pin, rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, sda_pin, scl_pin, potentiometer_pin, button_change_task


async def run_server():
    ap = network.WLAN (network.AP_IF)
    ap.active (True)
    ap.config (essid = 'ESP32-WIFI-NAME')
    ap.config (authmode = 3, password = 'WiFi-password')

    pins = {'Button led pin' : button_led_pin, 'Green led pin' : green_led_pin, 'Orange led pin' : orange_led_pin, 'Red led pin' : red_led_pin, 'RGB led red pin' : rgb_led_red_pin, 'RGB led green pin' : rgb_led_green_pin, 'RGB led blue pin' : rgb_led_blue_pin, 'SDA pin' : sda_pin, 'SCL pin' : scl_pin, 'Potentiometer pin' : potentiometer_pin, 'Button change task' : button_change_task}

    html = """
    <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body>
    <div class="body-container">
      <h1>ESP32 Pins</h1>
      <div class="table-container">
        <table>
          <thead>
            <tr class="table100-head">
              <th>Pin</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            %s
          </tbody>
        </table>
      </div>
    </div>
  </body>
  %s
</html>

"""
    style = """
<style>
    * {
      box-sizing: border-box;
      padding: 0px;
      margin: 0px;
    }
    html {
      height: 100%;
      width: 100%;
    }
    body {
      display: flex;
      justify-content: center;
      height: 100%;
      width: 100%;
      background: linear-gradient(45deg, #4158d0, #c850c0);
    }
    h1 {
      height: 4rem;
      line-height: 4rem;
      text-align: center;
      color: #eee;
    }
    table {
      border: solid 0px black;
      border-radius: 1rem;
      overflow: hidden;
      border-spacing: 0;
    }
    thead {
      background: #36304a;
    }
    tbody {
      background: #e0e0e0;
    }
    th {
      padding: 0rem 2rem;
      text-align: left;
      font-family: OpenSans-Regular;
      font-size: 18px;
      color: #fff;
      line-height: 1.2;
      font-weight: unset;
    }
    th:first-child {
      padding: 0rem 1rem;
    }
    th:last-child {
      padding: 0rem 1rem;
    }
    tr {
      border: 0;
      height: 50px;
      padding: 1rem 0rem;
      display: table-row;
      vertical-align: inherit;
      unicode-bidi: isolate;
      border-color: inherit;
    }
    td {
      border: solid 0px black;
      padding: 0rem 2rem;
    }
    td:first-child {
      padding: 0rem 1rem;
    }
    th:last-child {
      padding: 0rem 1rem;
    }
    .body-container {
      height: 100%;
      width: 100%;
    }
    .table-container {
      display: flex;
      align-items: center;
      justify-content: center;
    }
  </style>
"""
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    async def accept_connection(s):
        return s.accept()

    print('listening on', addr)

    while True:
        cl, addr = await uasyncio.create_task(accept_connection(s))
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            print(line)
            if not line or line == b'\r\n':
                break
        rows = ['<tr><td>%s</td><td>%d</td></tr>' % (name, pin.value()) for name, pin in pins.items()]
        response = html % ('\n'.join(rows), style)
        cl.send(response)
        cl.close()