# 时延测试步骤（夹爪电机）

## 1 获取时延测试专用的固件，并用Windows上位机进行固件的更换

[获取时延测试固件](https://github.com/kehuanjack/piper_sdk/releases/tag/4.0.2_beta_delay_test)

## 2 安装时延测试专用的sdk

```shell
git clone -b delay_test_042beta https://github.com/kehuanjack/piper_sdk.git
```

```shell
cd piper_sdk
pip3 install .
cd ..
```

## 3 克隆时延测试专用的ROS仓库

```shell
git clone -b humble_delay_test https://github.com/kehuanjack/piper_ros.git
```

```shell
cd piper_ros
colcon build
source install/setup.bash
```

## 4 采集数据

### 4.1 使能can模块

```bash
bash can_activate.sh can0 1000000
```

### 4.2 采集M1数据

```shell
ros2 launch piper start_single_piper_delay_test_M1.launch.py
```

### 4.3 采集M2数据

```shell
ros2 launch piper start_single_piper_delay_test_M2.launch.py
```

## 5 处理数据

注意：M1和M2都要采集，夹爪每次回零都会采集一帧数据，数据量可自行把控

```shell
python3 delay_test_process_seq.py
```

## 6 说明

主控会记录seq,seq1,seq2,seq3

主控会以1ms的间隔对seq进行累加，直至溢出重置，每个seq各占16bit，大约每隔一分钟会重置一次

夹爪每次回零或小于等于零主控会记录各阶段的seq数，给予其他大于零的值会主动重置所有的seq数

```python
print("SEQ DEFINITIONS:")
print("- seq_start: 下发159控制指令时的seq数")
print("- seq_end:   接收到seq3 != 0时的seq数")
print("- seq1:      主控接收到控制指令的seq数")
print("- seq2:      运动完成的seq数")
print("- seq3:      接收到上位机101反馈指令的seq数")
print("\nMOTION COMPLETION CRITERIA:")
print("- M1: 主控判断运动完成 (seq2 != 0)")
print("- M2: 上位机判断运动完成 (gripper_angle <= 0)")
print("\nTIME DIFFERENCE DEFINITIONS:")
print("- T0: seq1 - seq_start (指令传输时间)")
print("- T1: seq2 - seq1 (运动执行时间)")
print("- T2: seq3 - seq2 (反馈传输时间)")
```