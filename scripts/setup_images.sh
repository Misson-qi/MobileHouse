#!/bin/bash
# 图片设置脚本 - 从 docx_images 中选择合适的图片并复制到指定位置

echo "========================================="
echo "  移动住房项目 - 图片自动设置工具"
echo "========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📁 项目目录: $PROJECT_ROOT"
echo ""

# 源图片目录
SOURCE_DIR="assets/images/chapter01/docx_images"
TARGET_DIR="assets/images"

# 确保目标目录存在
mkdir -p "$TARGET_DIR/chapter01"
mkdir -p "$TARGET_DIR/chapter02"
mkdir -p "$TARGET_DIR/chapter03"

copied_count=0

echo "🔍 扫描可用图片..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第一章图片设置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 第一章图片映射
# 格式: "目标文件名:源文件名:描述"
declare -a chapter1_images=(
    "forbidden_city.jpg:docx_94_image4.jpeg:故宫/传统建筑"
    "trailer_rv_1.jpg:docx_100_image45.jpeg:拖挂式房车1"
    "trailer_rv_2.jpg:docx_102_image47.jpeg:拖挂式房车2"
    "mobile_home_camp.jpg:docx_136_image78.jpeg:营地示意图"
    "chassis_layout.jpg:docx_107_image51.png:底盘分布图"
    "mobile_home_design.jpg:docx_112_image56.png:移动房设计图"
    "aluminum_shell.jpg:docx_68_image16.png:铝合金外壳/建筑外观"
    "interior_layout.jpg:docx_95_image40.png:室内布局"
    "optimized_layout.jpg:docx_92_image38.png:优化布局"
    "kitchen_design.jpg:docx_91_image37.png:厨房设计"
    "national_standard.jpg:docx_76_image23.png:国家标准/文档"
)

for mapping in "${chapter1_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    
    target_path="$TARGET_DIR/chapter01/$target"
    source_path="$SOURCE_DIR/$source"
    
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        echo -e "    ${BLUE}复制:${NC} $source → $target"
        copied_count=$((copied_count + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $description"
        echo -e "    ${YELLOW}未找到源文件:${NC} $source"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第二章图片设置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a chapter2_images=(
    "hukou_book.jpg:docx_72_image2.png:户口本/证件"
    "passport.jpg:docx_159_image99.png:护照/证件"
    "starting_line.jpg:docx_138_image8.jpeg:儿童教育"
    "football.jpg:docx_87_image33.jpeg:足球/体育"
    "choir.jpg:docx_125_image68.jpeg:合唱/音乐"
    "watercolor.jpg:docx_127_image7.jpeg:绘画/艺术"
    "library.jpg:docx_133_image75.png:图书馆"
)

for mapping in "${chapter2_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    
    target_path="$TARGET_DIR/chapter02/$target"
    source_path="$SOURCE_DIR/$source"
    
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        echo -e "    ${BLUE}复制:${NC} $source → $target"
        copied_count=$((copied_count + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $description"
        echo -e "    ${YELLOW}未找到源文件:${NC} $source"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 第三章图片设置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a chapter3_images=(
    "electric_rv.jpg:docx_103_image48.jpeg:电动房车"
    "bedroom_folding.jpg:docx_90_image36.png:卧室折叠家具"
    "car_engine.jpg:docx_116_image6.jpeg:汽车发动机"
    "charging_station.jpg:docx_143_image84.png:充电桩"
    "gas_stove.jpg:docx_89_image35.png:燃气灶/厨房设备"
    "vertical_parking.jpg:docx_141_image82.png:立体停车场"
    "buffet.jpg:docx_80_image27.jpeg:自助餐/餐饮"
    "departure.jpg:docx_136_image78.jpeg:出发/旅行"
)

for mapping in "${chapter3_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    
    target_path="$TARGET_DIR/chapter03/$target"
    source_path="$SOURCE_DIR/$source"
    
    if [ -f "$source_path" ]; then
        cp "$source_path" "$target_path"
        echo -e "  ${GREEN}✓${NC} $description"
        echo -e "    ${BLUE}复制:${NC} $source → $target"
        copied_count=$((copied_count + 1))
    else
        echo -e "  ${YELLOW}⚠${NC} $description"
        echo -e "    ${YELLOW}未找到源文件:${NC} $source"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 处理完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✓ 成功复制 $copied_count 张图片${NC}"
echo ""

# 检查还缺少哪些图片
echo "🔍 检查图片完整性..."
echo ""

missing=0
for mapping in "${chapter1_images[@]}" "${chapter2_images[@]}" "${chapter3_images[@]}"; do
    IFS=':' read -r target source description <<< "$mapping"
    
    # 判断是第几章
    if [[ " ${chapter1_images[@]} " =~ " ${mapping} " ]]; then
        chapter="chapter01"
    elif [[ " ${chapter2_images[@]} " =~ " ${mapping} " ]]; then
        chapter="chapter02"
    else
        chapter="chapter03"
    fi
    
    target_path="$TARGET_DIR/$chapter/$target"
    
    if [ ! -f "$target_path" ]; then
        if [ $missing -eq 0 ]; then
            echo -e "${YELLOW}⚠️  以下图片仍然缺失：${NC}"
            echo ""
        fi
        echo -e "  ${RED}✗${NC} $description ($target)"
        missing=$((missing + 1))
    fi
done

if [ $missing -eq 0 ]; then
    echo -e "${GREEN}🎉 所有图片都已设置完成！${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  还有 $missing 张图片需要下载${NC}"
    echo ""
    echo "📖 建议："
    echo "  1. 查看 docs/图片下载指南.md 获取下载说明"
    echo "  2. 访问 https://www.pexels.com/zh-cn/ 下载缺失图片"
    echo "  3. 或调整 docx_images 映射关系"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 后续步骤"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 运行 'bash scripts/check_images.sh' 验证图片"
echo "2. 在 Markdown 中查看图片显示效果"
echo "3. 如需调整，编辑此脚本的映射关系"
echo ""
echo "========================================="

