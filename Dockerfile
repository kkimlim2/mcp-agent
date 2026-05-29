FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# 1) 의존성만 설치 (프로젝트 자체는 아직 빌드 안 함 → 캐시 잘 됨)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 2) 소스 + README 복사
COPY README.md ./
COPY src/ ./src/
COPY sql/ ./sql/

# 3) 이제 프로젝트까지 설치
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "mcp", "run", "src/agent_eval/server.py"]