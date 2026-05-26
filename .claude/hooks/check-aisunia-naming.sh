#!/bin/bash
# Aisunia の誤表記を Write/Edit 直前に検知してブロックするPreToolUse hook
# 出典：homepage-builder/docs/design-system.md L140-142
# 同一hookが homepage-factory にも配置されとる

input=$(cat)

# 除外ファイル：NG表記の「ルール解説」を書く必要があるため
file_path=$(echo "$input" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')

# パス区切り正規化（バックスラッシュ→スラッシュ）
file_path_norm="${file_path//\//}"
file_path_norm="${file_path_norm//\/}"

case "$file_path_norm" in
  *CLAUDE.md|*hooks*|*MEMORY*|*memory*|*design-system.md|*meishi.html|*cards/README.md|*brand/cards*)
    exit 0
    ;;
esac

# 禁止パターン
FORBIDDEN_PATTERNS=(
  "アイサニア・コンサルティング"
  "アイサニアコンサルティング"
  "アイスニア"
  "あいすにあ"
  "Aisunia / アイサニア・コンサルティング"
  "Aisunia/アイサニア・コンサルティング"
  "Aisunia / アイサニアコンサルティング"
)

for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
  if echo "$input" | grep -qF "$pattern"; then
    cat >&2 <<MSG
========================================
❌ Aisunia表記NG検出 — Write/Editをブロック
========================================

ファイル：$file_path
検出パターン：「$pattern」

【ルール（出典：homepage-builder/docs/design-system.md L140-142）】
・正式な屋号は **Aisunia のみ**（個人事業主・開業届提出済み）
・読みは **アイサニア**（「アイスニア」「あいすにあ」は誤読）
・「アイサニア・コンサルティング」は **名刺の補足表記** のみ
  → HP・プライバシーポリシー・提案資料・PDF・公式文書・メール本文では **絶対に使わない**

【除外ファイル】
CLAUDE.md / hooks/ / memory/ / MEMORY.md / design-system.md / meishi.html / brand/cards/

修正してから再実行してください。
MSG
    exit 2
  fi
done

exit 0
