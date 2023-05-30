# BirdPROBE Configuration File
#
# Some settings will replace the following well-known placeholders
# with their appropriate values:
#
# ${hostname}      - $(hostname)
# ${fqdn}          - $(hostname)
# ${component}     - name of the BirdPROBE component (location, birdnet, ...)
# ${birdnet_input} - audio input device index used by birdnet
# ${birdnet_label} - detected birdnet label

[DEFAULT]
# -=] Settings used by all components. [=-


# -- MQTT broker settings (paho-mqtt) --

# MQTT unique client id string (default: ${hostname}_${component})
#mqtt_client_id="${fqdn}_${component}"

# MQTT protocol version (default: MQTTv311)
#mqtt_protocol=MQTTv311

# MQTT transport protocol (default: tcp)
#mqtt_transport=tcp


# -- MQTT topic settings --

# Topic prefix
#topic_prefix=BirdPROBE

# Topic for component status
#topic_component=${topic_prefix}/component/${hostname}/${component}

# Topic for location reports
#topic_location=${topic_prefix}/location/${hostname}

# Topic for birdnet detections
#topic_detection=${topic_prefix}/detection/${hostname}/${birdnet_label}


[birdprobe.location]
# -=] Location provider to be used by birdnetlib and bird weather. [=-

# -- `none` provider settings --
# do not provide any location (default)
#provider=none


# -- `static` provider settings --
# provides a hard-coded location
#provider=static

# static location
#static_latitude=51.050407
#static_longitute=13.737262


# -- `gpsd` provider settings --
# use the location from gpsd's time-position-velocity reports
#provider=gpsd

# gpsd connection parameters
#gpsd_host=127.0.0.1
#gpsd_port=2947

# gpsd sleep interval between getting fixes (seconds)
#gpsd_sleep=30


[birdprobe.birdnet]
# -=] Birdnetlib recording and detection settings. [=-

# Device index of the audio input device. The default input device will be
# used if `input_device_index` is not configured (default).
#input_device_index=

# birdnetlib: recording sample rate (default: 48000)
#sample_rate=48000

# birdnetlib: detection sensitivity; higher values result in higher
# sensitivity; values in [0.5, 1.5]; defaults to 1.0
#sensitivity=1.0

# birdnetlib: minimum confidence threshold; values in [0.01, 0.99];
# defaults to 0.1
#min_conf=0.1

# birdnetlib: labels file to use (default: build-in)
#labels_file=labels_de.txt


[birdprobe.display.epaper1]
# -=] Waveshare-e-paper display example. [=-

# Display device class:
#   ws_epd: Waveshare e-paper
class=ws_epd

# Display module, see also:
#  https://github.com/yskoht/waveshare-epaper
module=epd2in7
