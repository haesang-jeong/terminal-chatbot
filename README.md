# Terminal Chatbot (Gemini Interactions API)

`google-genai` SDK의 **Interactions API**와 **`gemini-3.1-flash-lite`** 모델을 사용하는 메모리 없는(단발성) 터미널 챗봇입니다.

## 설정

1. `.env.example`을 복사해 `.env` 파일을 생성합니다.
   ```powershell
   Copy-Item .env.example .env
   ```
2. [Google AI Studio](https://aistudio.google.com/apikey)에서 발급받은 API 키를 `.env`에 입력합니다.
   ```env
   GEMINI_API_KEY=your-api-key-here
   GEMINI_MODEL=gemini-3.1-flash-lite
   ```

## 실행

```powershell
uv run chatbot
```

> `uv`가 `PATH`에 없다면 `C:\Users\touch\.local\bin\uv.exe run chatbot`으로 실행할 수 있습니다.

## 내장 명령어

- `/help`: 도움말 표시
- `/exit` 또는 `/quit`: 종료 (`Ctrl+C`도 가능)

## 테스트 및 린트

```powershell
uv run pytest -v
uv run ruff check .
```
