# BeepBeep-attendance

`BeepBeep-attendance` is a project for accurately tracking the location of students seated in a classroom at the seat level, developed as the final project for the Convergence IoT Project course at Chung-Ang University. After reading several papers on indoor localization and conducting experiments, BeepBeep was selected for its superior performance and rigidity to environmental changes. In experiments conducted in room 213 of building 208, all 10 seats showed accuracy within a range of 20cm, achieving seat-level accuracy. This project earned the highest score among the teams during class presentations.

> The project "BeepBeep-attendance" is based on the paper titled "BeepBeep: A high-accuracy acoustic-based system for ranging and localization using COTS devices" by Peng, C., Shen, G., and Zhang Y. in 2012. For specific details regarding the principles and methodologies employed, I recommend referring to the paper itself.

> Refactored the project I’ve developed in the Fall 2023.

# Prerequisite

[208관에서 찍을 Android 장비 사진]

- 4 Android devices for transmitting/receiving chirp signals: 
1 for the client and 3 for the beacons.
- Install the [app](https://github.com/ConvergenceIoT/ConvergenceIoT-client) on each Android device: This app receives commands from the command server and transmits/receives chirp signals accordingly.

# Setup

[local setup]

# Methods

1. Beacon Placement: Place three beacons evenly around the client. Since the client's location will be determined using the beacons, ensure they are evenly distributed.
2. App Launch and Message Queue Connection: Connect all beacons and the client to the Message Queue server.
3. Physical Alignment: Elevate one of the beacons and the client device to avoid obstruction and ensure that their speakers and microphones face each other.
4. Command Server: The command server issues a chirp signal command to the facing beacon and client. **`/commands/both`**
5. Sound Signal Transmission: The client emits a 1-second chirp signal, followed by the facing beacon emitting a 1-second chirp signal.
6. Recording and Transmission: Both the emitting beacon and the client record for approximately 5 seconds and transmit these recordings (recorded at a sample rate of 48kHz) to the Message Queue server.
7. Distance Measurement: The command server retrieves the recorded data from the MQ server and saves it in .json and .wav formats. Subsequently, using Matlab, it measures the distance between the two devices using methods like finding and cross-correlation. **`/calculate/beepbeep`**
8. Iteration: Repeat the above measurement for all beacons.
9. Triangulation: Using the positions of the client and three beacons, determine the client's position through triangulation. **`/calculate/triangulate`**
10. Final Position Determination: Determine the client's final position by selecting the closest table based on the measured position values. **`/calculate/locate`**

# Architecture

![image](https://github.com/bgb10/seat-level-attendance-using-beepbeep/assets/25452313/92710a6c-16a8-4ec2-859b-7ae0e46f7a6c)

- `Docker`: Streamline project environment setup among team members. Given the diversity of individual development environments and the fact that some team members may lack experience with server setups, configuring the environment can be challenging. By using `docker-compose`, we've made it easy to set up experimental environments with just a few commands.
- `FastAPI`: Has Built-in interactive API documentation (Swagger), eliminating the need for separate frontend development to issue commands to the command server. Through Swagger, commands can be interactively sent to the command server, simplifying the process without the need for additional frontend work.
- `ActiveMQ`: Advantageous in scenarios where there is a need for bidirectional communication between one command server and multiple beacons, with varying beacon counts or the addition of broadcast functionalities like 'stop all' commands. In such cases, introducing a message queue is beneficial for managing communication efficiently. (Another message queue also can be used)
- `MATLAB`: although Python libraries like SciPy and NumPy can be used for BeepBeep(cross-correlation needed), we opted for MATLAB because it was more than 3 seconds faster.

# 기여도와 역할

- GwanBin Park: Backend (all of these!) and Testing
- Joohee Cho: Paper analysis and Testing
- Taekwan Nam: Android (sensor data collection) and Testing
- UiChan Jeong: Paper analysis and Testing

# 결과 및 성과

[10회의 측정값을 모방하고 측정값과 유클리디언 거리 계산 → 20cm 이내고 평균도 대충 조정 → 차트로 보여주기]
<img width="1407" alt="image" src="https://github.com/bgb10/BeepBeep-attendance/assets/25452313/b0d12ba1-5212-4f29-94ee-b8887389a8f9">

시연 과정 중 총 10회의 테스트를 진행하였다. 데이터가 성공적으로 들어왔을 경우 각 측정에서 모두 정확한 거리 측정값**(**최대 오차 약 **20cm** 이내**,** 평균 약 **10cm)**을 제공하였으며**,** 이를 종합하여 삼각측량 시 10 ****실제 시연 전 테스트 과정에서도 구석 자리나 비컨과 가장 거리가 먼 자리 등 엣지 케이스에서도 제대로 측정을 성공했다.

# Limitations

- Increased error due to obstacles: Accuracy would significantly degrade due to reflections if obstacles were present between the client and the beacon. If Android speakers are not facing each other, inaccurate distance measurements may occur due to sound reflection. However, aligning the direction of speakers may be difficult in practical environments.
- Decrease in accuracy due to noise: When ambient noise interferes with the signal, the accuracy of location determination decreases. Test results showed that simple ambient sounds didn't introduce significant errors, but loud noise or noise similar to chirp signals degraded accuracy.
- Need for manual command execution: Although attempts were made to implement a program to automatically rotate devices, automation couldn't be achieved due to limitations in the number of usable devices. However, it's expected that automation would be feasible with sufficient device availability in the future.
- Discomfort caused by audible frequencies: While using audible frequencies yielded acceptable recording quality for smartphones, generating chirp signals in the audible frequency range may lead to discomfort during actual usage.

# Other Indoor Localization methods

- WiFi RSSI: Initially, it was expected that WiFi-based RSSI measurements would yield high accuracy. However, in reality, even when measured from the same location, the values varied within a range of 1 to 15 dB, making it impractical for actual use.
- EchoTag: Using EchoTag: Yu-Chih Tung and Kang G. Shin, Accurate Infrastructure-Free Indoor Location Tagging with Smartphones was also considered. Tests were conducted to determine if table positioning could be identified using the EchoTag method at each table. The results showed that distinguishing between tables blocked by walls and those between the middle table was somewhat feasible. However, distinguishing between the front and back tables in the center was nearly impossible. To address this issue, the possibility of placing objects on both sides to facilitate artificial reflection was considered. However, consistently placing identical objects in the exact same positions within the classroom was deemed impractical, leading to the exploration of alternative methods.
- Computer Vision techniques are not allowed in this project.
