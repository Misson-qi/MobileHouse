#!/bin/bash
# 删除缺失图片引用的脚本 - 清理无法显示的图片链接

echo "========================================="
echo "  移动住房项目 - 删除缺失图片引用"
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

echo -e "${YELLOW}⚠️  警告：此操作将删除所有指向不存在图片的引用！${NC}"
echo ""
echo "按 Ctrl+C 取消，或按 Enter 继续..."
read

removed_count=0

# 处理函数
process_chapter() {
    local chapter_file=$1
    local chapter_name=$2
    
    if [ ! -f "$chapter_file" ]; then
        return
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 处理 $chapter_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 创建临时文件
    temp_file="${chapter_file}.tmp"
    cp "$chapter_file" "$temp_file"
    
    # 读取文件，检查每个图片引用
    while IFS= read -r line; do
        # 检查是否是图片引用行
        if echo "$line" | grep -q '!\[.*\](.*\.jpg\|.*\.png\|.*\.jpeg\|.*\.gif)'; then
            # 提取图片路径
            image_path=$(echo "$line" | sed -n 's/.*(\(.*\))/\1/p')
            
            # 转换为绝对路径
            if [[ "$image_path" == ../* ]]; then
                full_path="$PROJECT_ROOT/$(echo $image_path | sed 's|^\.\./||')"
            else
                full_path="$PROJECT_ROOT/$image_path"
            fi
            
            # 检查文件是否存在
            if [ ! -f "$full_path" ]; then
                description=$(echo "$line" | sed -n 's/!\[\(.*\)\](.*/\1/p')
                echo -e "  ${RED}删除:${NC} $description"
                echo -e "    ${RED}路径:${NC} $image_path"
                
                # 从临时文件中删除这一行
                sed -i '' "/$(echo "$line" | sed 's/[\/&]/\\&/g')/d" "$temp_file"
                
                # 同时删除下一行如果是图片说明（*xxx*格式）
                removed_count=$((removed_count + 1))
            fi
        fi
    done < "$chapter_file"
    
    # 替换原文件
    mv "$temp_file" "$chapter_file"
    echo ""
}

# 处理各章节
process_chapter "docs/chapter01.md" "第一章"
process_chapter "docs/chapter02.md" "第二章"
process_chapter "docs/chapter03.md" "第三章"
process_chapter "docs/chapter04.md" "第四章"
process_chapter "docs/chapter05.md" "第五章"
process_chapter "docs/chapter06.md" "第六章"
process_chapter "docs/chapter07.md" "第七章"
process_chapter "docs/chapter08.md" "第八章"
process_chapter "docs/chapter09.md" "第九章"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 处理完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✓ 已删除 $removed_count 个缺失图片的引用${NC}"
echo ""
echo "📖 后续建议："
echo "  • 查看 docs/图片下载指南.md 下载所需图片"
echo "  • 使用 git diff 查看具体删除了哪些引用"
echo ""
echo "========================================="

