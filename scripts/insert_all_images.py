#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动插入图片到第6-9章
"""

import re

# 定义所有需要插入的图片
inserts = {
    'chapter06.md': [
        {
            'after': '## 6.3 机器学习到底是怎么学的？',
            'insert': '\n![机器学习](../assets/images/chapter06/machine_learning.jpg)\n*机器学习的三种学习方式*\n'
        },
        {
            'after': '## 6.4 神经网络：模仿大脑的学习方式',
            'insert': '\n![神经网络](../assets/images/chapter06/neural_network.jpg)\n*神经网络结构示意图*\n'
        },
        {
            'after': '### 例子3：智能家居',
            'insert': '\n![智能家居](../assets/images/chapter06/smart_home.jpg)\n*移动住房智能家居系统*\n'
        },
        {
            'after': '计算机视觉（Computer Vision）：让电脑"看懂"图片和视频',
            'insert': '\n![计算机视觉](../assets/images/chapter06/computer_vision.jpg)\n*计算机视觉技术应用*\n'
        },
        {
            'after': '自然语言处理（NLP）：让电脑"听懂"人话',
            'insert': '\n![自然语言处理](../assets/images/chapter06/natural_language.jpg)\n*自然语言处理系统*\n'
        },
        {
            'after': '机器人（Robotics）：能动的AI',
            'insert': '\n![AI机器人](../assets/images/chapter06/ai_robot.jpg)\n*智能机器人应用*\n'
        }
    ],
    'chapter07.md': [
        {
            'after': '# 第七章 电池技术',
            'insert': '\n![锂电池](../assets/images/chapter07/lithium_battery.jpg)\n*锂离子电池结构示意图*\n'
        },
        {
            'after': '## 7.2 磷酸铁锂（LFP）电池',
            'insert': '\n![磷酸铁锂电池](../assets/images/chapter07/lfp_battery.jpg)\n*LFP电池技术*\n'
        },
        {
            'after': '## 7.4 固态电池',
            'insert': '\n![固态电池](../assets/images/chapter07/solid_state_battery.jpg)\n*固态电池结构与传统电池对比*\n'
        },
        {
            'after': '### 7.5.1 技术原理',
            'insert': '\n![氢电池](../assets/images/chapter07/hydrogen_battery.jpg)\n*固体氢电池技术原理*\n'
        },
        {
            'after': '电池包设计',
            'insert': '\n![电池包](../assets/images/chapter07/battery_pack.jpg)\n*电池包设计与布局*\n'
        },
        {
            'after': '充电技术',
            'insert': '\n![充电技术](../assets/images/chapter07/charging_technology.jpg)\n*快速充电技术*\n'
        },
        {
            'after': '电池管理系统',
            'insert': '\n![电池管理系统](../assets/images/chapter07/battery_management.jpg)\n*BMS电池管理系统*\n'
        },
        {
            'after': '能量密度对比',
            'insert': '\n![能量密度对比](../assets/images/chapter07/energy_density.jpg)\n*各类电池能量密度对比*\n'
        }
    ],
    'chapter08.md': [
        {
            'after': '# 第八章 电动飞行器',
            'insert': '\n![eVTOL飞行器](../assets/images/chapter08/evtol_aircraft.jpg)\n*电动垂直起降飞行器*\n'
        },
        {
            'after': '### 垂直起降',
            'insert': '\n![垂直起降](../assets/images/chapter08/vertical_takeoff.jpg)\n*垂直起降技术演示*\n'
        },
        {
            'after': '飞行汽车',
            'insert': '\n![飞行汽车](../assets/images/chapter08/flying_car.jpg)\n*飞行汽车概念*\n'
        },
        {
            'after': '## 8.6 静音飞行器技术突破',
            'insert': '\n![流体推进系统](../assets/images/chapter08/fluidic_propulsion.jpg)\n*FPS流体推进系统*\n'
        },
        {
            'after': '空中出租车',
            'insert': '\n![空中出租车](../assets/images/chapter08/air_taxi.jpg)\n*eVTOL空中出租车*\n'
        },
        {
            'after': '低空飞行',
            'insert': '\n![低空飞行](../assets/images/chapter08/low_altitude_flight.jpg)\n*低空经济应用场景*\n'
        },
        {
            'after': '电动飞机',
            'insert': '\n![电动飞机](../assets/images/chapter08/electric_aircraft.jpg)\n*电动飞机技术*\n'
        },
        {
            'after': '未来交通',
            'insert': '\n![未来交通](../assets/images/chapter08/future_transportation.jpg)\n*未来立体交通网络*\n'
        }
    ],
    'chapter09.md': [
        {
            'after': '# 第九章 未来展望',
            'insert': '\n![未来展望](../assets/images/chapter09/future_outlook.jpg)\n*移动住房时代的未来图景*\n'
        },
        {
            'after': '## 9.1 移动房对生活的影响',
            'insert': '\n![移动生活方式](../assets/images/chapter09/mobile_lifestyle.jpg)\n*移动住房改变生活方式*\n'
        },
        {
            'after': '## 9.2 社会结构的变化',
            'insert': '\n![未来城市](../assets/images/chapter09/future_city.jpg)\n*未来城市形态演变*\n'
        },
        {
            'after': '智慧城市',
            'insert': '\n![智慧城市](../assets/images/chapter09/smart_city.jpg)\n*智慧城市基础设施*\n'
        },
        {
            'after': '## 9.4 环境影响',
            'insert': '\n![可持续生活](../assets/images/chapter09/sustainable_living.jpg)\n*可持续环保生活*\n'
        },
        {
            'after': '## 9.5 技术融合与生态系统',
            'insert': '\n![技术融合](../assets/images/chapter09/technology_convergence.jpg)\n*多技术融合架构*\n'
        }
    ]
}

print("图片插入配置已准备")
print(f"共需处理 {len(inserts)} 个章节文件")
for chapter, items in inserts.items():
    print(f"  - {chapter}: {len(items)} 张图片")

