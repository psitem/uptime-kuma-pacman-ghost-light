# ESPHome version of Pacman Ghost Light

For posterity's sake, this directory contains the original [ESPHome](https://esphome.io/) version of my Pacman Ghost Light. It does not operate stand-alone — [Home Assistant](https://www.home-assistant.io/) and the [Uptime Kuma integration](https://github.com/meichthys/uptime_kuma) are required.

I run two instances of Uptime Kuma. One runs on my LAN and monitors things from an internal perspective, another runs "in the cloud" and monitors external connectivity to my public services. On the Home Assistant side, I created a sensor in `configuration.yaml` that combines the summary sensors of both instances from the integration into one:

    template:
    - binary_sensor:
        - name: sensor.uptimekuma_summary
            state: >
            {{
                state_attr('sensor.uptimekuma_instance_1', 'monitors_down') == 0
                and state_attr('sensor.uptimekuma_instance_2', 'monitors_down') == 0
            }}

On the device side, `pico-pacghost.yaml` pulls in that Home Assistant entity:

    binary_sensor:
      - platform: homeassistant
          name: "uk_summary"
          id: "uk_summary"
          internal: True
          entity_id: binary_sensor.sensor_uptimekuma_summary
          publish_initial_state: True

It also exposes itself to Home Assistant as a controllable RGB light.

There is other configuration in the YAML that you would need to adjust in order to use this. By the nature of ESPHome, `pico-pacghost.yaml` will generate a firmware that is specific to a Raspberry Pi Pico W board. It should be trivial to change to another supported board and, given the current state of Pico W support in ESPHome, you'd be better off with a more mature platform like the ESP32.

I am no longer using this so please don't ask me for help with anything related to it.