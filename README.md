# BirdPROBE

BirdPROBE does offline live monitoring of bird vocals using the [BirdNET artificial neural network](https://birdnet.cornell.edu/).

## Design

BirdPROBE consists of several components loosley connected through a MQTT broker:

- `birdprobe-detection` - records audio and does detection based on *BirdNET*, publishes it's detections via MQTT
- `birdprobe-display` - displays detections and status informations via external displays by listening to MQTT events
- `birdprobe-location` - publishes location information via MQTT from different providers (`none`, `static`, `gpsd`)
- `birdprobe-record` - records detection events *TBD*

## Status

This is project is in WIP and not ready to use, yet.

## Usage

### MQTT Broker

You need a MQTT broker. You can use a local *mosquitto*:

```console
# apt-get install mosquitto mosquitto-clients
```

### Install

Clone this repository:

```console
$ git clone https://codeberg.org/liske/BirdPROBE.git
```

Create a python3 virtualenv

```console
$ cd BirdPROBE
$ virtualenv -p python3 venv
$ . venv/bin/activate
```

Install *BirdPROBE*:
```console
$ pip install -e .
```

You can add optional features:

- `gps` - *gpsd* based location provider
- `ws-epd`- *waveshare-epaper* display support

```console
$ pip install -e '.[gps,ws-epd]'
```

### Run

The components provide appropriate commands in the virtualenv to start them.

Run the detection component:

```console
$ birdprobe-detector -c /path/to/config.ini
```

Run the location provider:

```console
$ birdprobe-location -c /path/to/config.ini
```

Monitor MQTT messages:

```console
$ mosquitto_sub -v -t 'BirdPROBE/#'
```


## TODO
- provide some packaging
- finish components
- more optimization for low power setups
  - use some binary rather than JSON message format
  - update prediction only if location has significant changes
  - update week_48 less often
