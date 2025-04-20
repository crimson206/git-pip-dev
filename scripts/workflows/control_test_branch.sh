git checkout -b test/<uuid-or-timestamp>

# 커밋 예시
echo "# test commit" >> dummy.txt
git add dummy.txt
git commit -m "test commit"

# 고유 태그
git tag v1.2.3-test-<uuid>
git push origin v1.2.3-test-<uuid>

# 태그 삭제
git push origin :refs/tags/v1.2.3-test-<uuid>

# 브랜치 삭제
git push origin --delete test/<uuid>

