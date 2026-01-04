#!/bin/bash
# 为第4-9章添加图片

echo "========================================="
echo "  为第4-9章添加图片"
echo "========================================="
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SOURCE_DIR="assets/images/chapter01/docx_images"
TARGET_DIR="assets/images"

# 创建目录
mkdir -p "$TARGET_DIR/chapter04"
mkdir -p "$TARGET_DIR/chapter05"
mkdir -p "$TARGET_DIR/chapter06"
mkdir -p "$TARGET_DIR/chapter07"
mkdir -p "$TARGET_DIR/chapter08"
mkdir -p "$TARGET_DIR/chapter09"

copied=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第四章：移动商业空间（6张）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a chapter4_images=(
    "mobile_meeting_room.jpg:docx_139_image80.png:移动会议室"
    "mobile_hotel.jpg:docx_99_image44.jpeg:移动酒店/胶囊旅馆"
    "mobile_restaurant.jpg:docx_73_image20.jpeg:移动餐厅/餐车"
    "mobile_gym.jpg:docx_88_image34.jpeg:移动健身房"
    "mobile_library.jpg:docx_133_image75.png:移动图书馆"
    "mobile_business.jpg:docx_140_image81.png:移动商业综合体"
)

for mapping in "${chapter4_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    target_path="$TARGET_DIR/chapter04/$target"
    source_path="$SOURCE_DIR/$source"
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        copied=$((copied + 1))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第五章：自动驾驶（8张）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a chapter5_images=(
    "autonomous_vehicle.jpg:docx_106_image50.png:自动驾驶汽车"
    "tesla_fsd.jpg:docx_114_image58.jpeg:特斯拉FSD"
    "lidar_sensor.jpg:docx_144_image85.png:激光雷达传感器"
    "camera_vision.jpg:docx_145_image86.png:视觉摄像头"
    "v2x_communication.jpg:docx_109_image53.png:V2X通信"
    "autonomous_levels.jpg:docx_108_image52.png:自动驾驶等级"
    "high_precision_map.jpg:docx_115_image59.png:高精度地图"
    "ai_chip.jpg:docx_146_image87.png:AI芯片"
)

for mapping in "${chapter5_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    target_path="$TARGET_DIR/chapter05/$target"
    source_path="$SOURCE_DIR/$source"
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        copied=$((copied + 1))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第六章：人工智能（7张）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a chapter6_images=(
    "neural_network.jpg:docx_147_image88.png:神经网络"
    "machine_learning.jpg:docx_148_image89.png:机器学习"
    "ai_application.jpg:docx_150_image90.png:AI应用"
    "smart_home.jpg:docx_93_image39.png:智能家居"
    "computer_vision.jpg:docx_96_image41.png:计算机视觉"
    "natural_language.jpg:docx_83_image3.png:自然语言处理"
    "ai_robot.jpg:docx_151_image91.jpeg:AI机器人"
)

for mapping in "${chapter6_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    target_path="$TARGET_DIR/chapter06/$target"
    source_path="$SOURCE_DIR/$source"
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        copied=$((copied + 1))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第七章：电池技术（8张）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a chapter7_images=(
    "lithium_battery.jpg:docx_152_image92.png:锂电池"
    "lfp_battery.jpg:docx_154_image94.png:磷酸铁锂电池"
    "solid_state_battery.jpg:docx_155_image95.png:固态电池"
    "hydrogen_battery.jpg:docx_157_image97.png:氢电池"
    "battery_pack.jpg:docx_158_image98.jpeg:电池包"
    "charging_technology.jpg:docx_84_image30.png:充电技术"
    "battery_management.jpg:docx_77_image24.png:电池管理系统"
    "energy_density.jpg:docx_153_image93.jpeg:能量密度对比"
)

for mapping in "${chapter7_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    target_path="$TARGET_DIR/chapter07/$target"
    source_path="$SOURCE_DIR/$source"
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        copied=$((copied + 1))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第八章：电动飞行器（8张）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a chapter8_images=(
    "evtol_aircraft.jpg:docx_75_image22.jpeg:eVTOL飞行器"
    "vertical_takeoff.jpg:docx_74_image21.jpeg:垂直起降"
    "flying_car.jpg:docx_71_image19.jpeg:飞行汽车"
    "fluidic_propulsion.jpg:docx_70_image18.jpeg:流体推进系统"
    "air_taxi.jpg:docx_69_image17.jpeg:空中出租车"
    "low_altitude_flight.jpg:docx_78_image25.jpeg:低空飞行"
    "electric_aircraft.jpg:docx_79_image26.jpeg:电动飞机"
    "future_transportation.jpg:docx_81_image28.jpeg:未来交通"
)

for mapping in "${chapter8_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    target_path="$TARGET_DIR/chapter08/$target"
    source_path="$SOURCE_DIR/$source"
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        copied=$((copied + 1))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第九章：未来展望（6张）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a chapter9_images=(
    "future_city.jpg:docx_137_image79.png:未来城市"
    "mobile_lifestyle.jpg:docx_97_image42.jpeg:移动生活方式"
    "technology_convergence.jpg:docx_98_image43.jpeg:技术融合"
    "sustainable_living.jpg:docx_86_image32.jpeg:可持续生活"
    "smart_city.jpg:docx_85_image31.jpeg:智慧城市"
    "future_outlook.jpg:docx_82_image29.jpeg:未来前景"
)

for mapping in "${chapter9_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    target_path="$TARGET_DIR/chapter09/$target"
    source_path="$SOURCE_DIR/$source"
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        copied=$((copied + 1))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 处理完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✓ 新增复制 $copied 张图片${NC}"
echo ""
echo "📝 后续步骤："
echo "  1. 手动在各章节 Markdown 文件中插入图片引用"
echo "  2. 使用格式: ![描述](../assets/images/chapterXX/xxx.jpg)"
echo "  3. 或运行自动插入脚本（下一步创建）"
echo ""
echo "========================================="

