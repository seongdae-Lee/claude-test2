# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
python app.py
```

http://localhost:5000 에서 접속. DB 파일(`board.db`)은 최초 실행 시 자동 생성된다.

정적 파일만 서빙할 때:

```bash
python -m http.server 8080
```

## Project Structure

- `app.py` - Flask 앱 진입점. 라우팅, DB 초기화, CRUD 로직 포함
- `templates/` - Jinja2 템플릿
  - `base.html` - 공통 레이아웃 (헤더, 공통 CSS, `.btn` 스타일)
  - `index.html` - 게시글 목록
  - `write.html` - 글쓰기 폼 
  - `view.html` - 게시글 상세 + 삭제
- `board.db` - SQLite DB 파일 (gitignore 권장)
- `index.html` - 원본 Hello World 정적 페이지 (Flask와 무관)

## Architecture

Flask + SQLite 단일 파일 구조. `get_db()`가 요청마다 커넥션을 열고 `with` 블록으로 자동 커밋/닫기 처리한다. `init_db()`는 `app.py` 직접 실행 시에만 호출된다.

posts 테이블: `id`, `title`, `author`, `content`, `created_at`
