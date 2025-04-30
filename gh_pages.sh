# 1. 새 orphan 브랜치 생성 (기존 이력 없음)
git checkout --orphan gh-pages

# 2. 기존 파일들 전부 제거 (tracked 포함)
git rm -rf .

# 3. 필요한 정적 파일만 생성 또는 복사
mkdir -p simple/dev
cp path/to/index.html simple/dev/index.html

# 4. 커밋 및 푸시
git add .
git commit -m "Initialize GitHub Pages"
git push origin gh-pages
