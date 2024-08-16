# Phi Pilot

PhiPilot allows you to run [Microsoft Phi](https://azure.microsoft.com/products/phi-3) on a Raspberry Pi to bring a local SLM (Small language model) to your home network for privacy or IoT projects.

## Run this project

You can run this project on any device that can run Python, such as your laptop, but the goal here is to provide an implementation to run on a headless Raspberry Pi.

### Hardware

For the Raspberry Pi, you will need:

- Ideally a Raspberry Pi 5 as this is CPU intensive
- 8GB RAM
- Ideally an SSD instead of an SD card

Your Raspberry Pi should have the latest Raspberry Pi OS with all the relevant updates. You don't need the desktop version, the lite version is fine.

### Software

To run this project:

1. On your Raspberry Pi, install [Ollama](https://ollama.com/download/linux) with the following command:

    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```

1. Download the Phi-3 model from Ollama:

    ```bash
    ollama pull phi3
    ```

1. Install [Poetry](https://python-poetry.org) with the following command:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

1. Clone this repo

    ```bash
    git clone https://github.com/jimbobbennett/phipilot
    ```

1. Change to the repo directory

    ```bash
    cd phipilot
    ```

1. Run the app using Poetry

    ```bash
    poetry run start
    ```

### Run this project on device startup

There is a helper script to start this project, [`scripts/start-poetry.sh](./scripts/start-poetry.sh). You can call this using `systemctl` to start the project when your Pi boots up.

1. Create a `systemctl` file:

    ```bash
    sudo nano /etc/systemd/system/phipilot.service 
    ```

1. Add the following to this file:

    ```
    [Unit]
    Description=Run copilot over ngrok
    After=multi-user.target

    [Service]
    Type=idle
    User=<user>
    ExecStart=/home/<user>/phipilot/scripts/start-poetry.sh

    [Install]
    WantedBy=multi-user.target
    ```

    Replace `<user>` in the `User` and `ExecStart` fields with your username, and ensure the `ExecStart` has the right path that you cloned the repo to.

1. Enable and start the service:

    ```bash
    sudo systemctl enable phipilot.service
    sudo systemctl start phipilot.service
    ```

This will now run, and restart when you reboot the Pi.

### Access Phipilot over the internet

If you want to access your PhiPilot remotely over the internet, you can use [Ngrok](https://ngrok.com).

## Microsoft Phi-3

Phi-3 is an SML (described [below](#what-is-a-slm)) that is small enough to run on a Raspberry Pi. It has 3.82B parameters, is 2.2GB in size and can easily run on an 8GB Raspberry Pi. It is on par with GPT-3.5, and outperforms Gemini 1.0 on a number of popular benchmarks.

You can read more about this model on the [Ollama Phi-3 model page](https://ollama.com/library/phi3).

## What is a SLM?

A SLM, or small language model is like an LLM, a large language model, just smaller!

LLMs, like ChatGPT, are huge and require racks of hardware to run, using multiple powerful graphics cards. They can be multiple terabytes in size. SLMs on the other hand are smaller, often a few gigabytes in size, and can be run on commodity hardware, such as your laptop, desktop, or even smaller devices like a Raspberry Pi.

As they are smaller, they are not as capable as a full cloud deployed LLM, but they are still pretty powerful.

The advantages of using an SLM are:

- Privacy - Nothing leaves your network to go to a public cloud LLM
- Cost - There are no costs beyond running your won hardware
- Air gapped - If you are in an air-gapped environment such as a network that as no internet access for security purposes, or in a location with no internet such as a disaster zone or off-shore, then you can still take advantage of an LLM

## Run an SLM on a Raspberry Pi

Raspberry Pis are small, single board computers. They are reasonably cheap for a computer, and pretty powerful for their size. They are general purpose computing devices, in that they run Linux so can run pretty much any task that you want of them. However, they run best when they do one thing and one thing only. So rather than think of them as a server that can run multiple jobs, it's better to think of running a range of Pis across your network distributing tasks to each one as necessary.

This is the idea behind PhiPilot - it converts a single Raspberry Pi to an SLM that runs on your network. You can then farm out jobs to it as needed from other devices.

For example, if you wanted to control your house with your voice, you might have 3 Pis set up:

1. A Pi running Whisper to do speech to text
1. A Pi as an orchestrator
1. A Pi running PhiPilot to respond to text
1. A Pi running home assistant to manage your house

You would use another device to respond to your audio, such as a smart speaker or other embedded device. It would stream the audio to the Whisper Pi, that would then send the text to another Pi running as an orchestrator. This adds the text to a prompt with a relevant system prompt to understand the intent of your voice. It would send this to the PhiPilot, get back an intent, and use that to control your house via home assistant.

You could run this all on one device, but it would be potentially slow, especially if there are multiple actions happening at once. A more typical way to scale this is to just have the hardware you need for each node, so you can manage deployments to them individually. Your home assistant could be a Pi zero to save cost and power, the PhiPilot would have more RAM/SSD to respond faster, the orchestrator could have less RAM and so on.
