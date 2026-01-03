#!/bin/bash
# 图片检查脚本 - 检查哪些图片存在，哪些缺失

echo "========================================="
echo "     移动住房项目 - 图片检查工具"
echo "========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📁 项目目录: $PROJECT_ROOT"
echo ""

# 统计变量
total_images=0
missing_images=0
existing_images=0

echo "🔍 检查图片引用..."
echo ""

# 检查函数
check_chapter() {
    local chapter_file=$1
    local chapter_name=$2
    
    if [ ! -f "$chapter_file" ]; then
        return
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 $chapter_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 提取所有图片引用
    grep -o '!\[.*\](.*\.jpg\|.*\.png\|.*\.jpeg\|.*\.gif)' "$chapter_file" | while IFS= read -r line; do
        # 提取图片描述和路径
        description=$(echo "$line" | sed -n 's/!\[\(.*\)\](.*/\1/p')
        image_path=$(echo "$line" | sed -n 's/.*(\(.*\))/\1/p')
        
        # 转换为绝对路径
        if [[ "$image_path" == ../* ]]; then
            # 相对于 docs/ 目录
            full_path="$PROJECT_ROOT/$(echo $image_path | sed 's|^\.\./||')"
        else
            full_path="$PROJECT_ROOT/$image_path"
        fi
        
        total_images=$((total_images + 1))
        
        # 检查文件是否存在
        if [ -f "$full_path" ]; then
            echo -e "  ${GREEN}✓${NC} $description"
            echo -e "    ${GREEN}存在:${NC} $image_path"
            existing_images=$((existing_images + 1))
        else
            echo -e "  ${RED}✗${NC} $description"
            echo -e "    ${RED}缺失:${NC} $image_path"
            missing_images=$((missing_images + 1))
        fi
        echo ""
    done
}

# 检查各章节
check_chapter "docs/chapter01.md" "第一章：移动房的概念"
check_chapter "docs/chapter02.md" "第二章：中国户籍与教育"
check_chapter "docs/chapter03.md" "第三章：电动房车公寓"
check_chapter "docs/chapter04.md" "第四章：移动商业空间"
check_chapter "docs/chapter05.md" "第五章：自动驾驶"
check_chapter "docs/chapter06.md" "第六章：人工智能"
check_chapter "docs/chapter07.md" "第七章：电池技术"
check_chapter "docs/chapter08.md" "第八章：电动飞行器"
check_chapter "docs/chapter09.md" "第九章：未来展望"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 统计结果"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "  总图片数:   ${YELLOW}$total_images${NC}"
echo -e "  ${GREEN}已存在:${NC}     $existing_images"
echo -e "  ${RED}缺失:${NC}       $missing_images"
echo ""

if [ $missing_images -eq 0 ]; then
    echo -e "${GREEN}🎉 所有图片都已准备好！${NC}"
else
    echo -e "${YELLOW}⚠️  发现 $missing_images 张图片缺失${NC}"
    echo ""
    echo "📖 下一步操作："
    echo "  1. 查看 docs/图片下载指南.md 获取详细下载说明"
    echo "  2. 访问 https://www.pexels.com/zh-cn/ 下载图片"
    echo "  3. 或运行 'bash scripts/remove_missing_images.sh' 删除缺失图片引用"
fi

echo ""
echo "========================================="

