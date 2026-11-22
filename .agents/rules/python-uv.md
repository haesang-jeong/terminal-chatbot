---
trigger: always_on
description: "Python 버전 설치, 가상환경, 패키지 관리, 스크립트·테스트 실행 등 모든 Python 작업 시 반드시 uv만 사용하도록 강제하는 규칙"
---

# Python 작업 시 `uv` 필수 사용

- 이 워크스페이스의 모든 Python 작업(버전 설치, 가상환경, 패키지 관리, 스크립트·테스트·CLI 도구 실행)에는 반드시 `uv`만 사용한다.
- 시스템의 `python`, `python3`, `pip`, `pip3`, `venv`, `virtualenv` 등을 직접 호출하지 않는다.
- `uv`가 실행되지 않거나 `PATH`에서 찾을 수 없는 경우에도 시스템 `python`/`pip`으로 대체하지 말고, `uv` 경로를 확인하거나 사용자에게 알린다.
