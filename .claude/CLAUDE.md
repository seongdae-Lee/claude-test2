# Claude Team Configuration

## 🧠 소통 방식

- 응답은 **한국어**로 작성
- 코드 변경 전 반드시 현재 코드를 먼저 파악하고 계획을 설명한 뒤 진행
- 한 번에 너무 많은 파일을 수정하지 말 것 — 단계별로 진행
- 작업 완료 후 변경된 파일 목록과 이유를 간단히 요약
- 확실하지 않은 부분은 임의로 구현하지 말고 반드시 먼저 질문할 것
- 기능 구현 시 엣지 케이스와 예외 상황도 함께 언급

---

## 🎨 코딩 스타일

### 공통

- 주석은 **한국어**로 작성
- 복잡한 로직에는 반드시 설명 주석 추가
- `TODO:`, `FIXME:` 형식으로 작업 표시

### Frontend (Next.js + TypeScript)

- 언어: TypeScript (strict mode, `any` 사용 금지)
- 들여쓰기: 2 spaces, single quote, 세미콜론 없음
- 파일명: `kebab-case.ts`, 컴포넌트명: `PascalCase`, 변수/함수명: `camelCase`
- 컴포넌트: 함수형 컴포넌트만 사용 (클래스형 금지)
- `use client`는 필요한 경우에만 최소한으로 사용
- 스타일: Tailwind CSS만 사용 (inline style 금지)
- 상태관리: 서버 상태는 TanStack Query, 클라이언트 상태는 Zustand
- 이미지는 반드시 `next/image` 사용
- `@ts-ignore`, `@ts-nocheck`, `eslint-disable` 사용 금지

### Backend (.NET / C#)

- 언어: C# 12, .NET 8 이상
- 네이밍 컨벤션:
  - 클래스/메서드/프로퍼티: `PascalCase`
  - 지역 변수/파라미터: `camelCase`
  - private 필드: `_camelCase`
  - 상수: `PascalCase`
  - 인터페이스: `I` 접두사 (예: `IUserService`)
- 아키텍처: Clean Architecture 레이어 구조 유지
  ```
  API (Controllers) → Application (Services, DTOs) → Domain (Entities) → Infrastructure (DB, External)
  ```
- 모든 비동기 메서드는 `Async` 접미사 붙이기 (예: `GetUserAsync`)
- `async/await` 사용, `.Result` / `.Wait()` 호출 금지 (데드락 위험)
- `var` 사용 가능하나 타입이 명확한 경우에만 허용
- nullable 참조 타입 활성화 (`#nullable enable`), null 체크 철저히
- `record` 타입을 DTO에 적극 활용
- 예외 처리는 글로벌 미들웨어로 통합 (`IExceptionHandler`)
- API 응답 형식 통일:
  ```csharp
  // 성공
  { "success": true, "data": T }
  // 실패
  { "success": false, "error": "메시지", "code": "ERROR_CODE" }
  ```
- 의존성 주입(DI) 필수 사용, `new`로 직접 인스턴스 생성 금지
- 매직 넘버/문자열은 `const` 또는 `enum`으로 정의

---

## 🔒 보안

- **절대 하드코딩 금지**: API 키, 비밀번호, 커넥션 스트링은 반드시 `appsettings.json` + 환경변수 또는 Azure Key Vault 사용
- 새로운 환경변수 추가 시 `appsettings.example.json`도 함께 업데이트
- 사용자 입력값은 항상 서버 사이드에서 유효성 검사 (FluentValidation 사용)
- EF Core 파라미터 바인딩 사용, raw SQL 최소화 (필요 시 파라미터 바인딩 필수)
- 인증이 필요한 엔드포인트에는 반드시 `[Authorize]` 어트리뷰트 확인
- 민감한 정보는 로그에 출력하지 않을 것 (Serilog structured logging 사용)
- CORS 설정은 허용 도메인을 명시적으로 지정 (와일드카드 금지)
- 패스워드는 반드시 `BCrypt` 또는 ASP.NET Core Identity로 해싱
- JWT 토큰 만료 시간 설정 필수, Refresh Token 로직 포함

---

## 🧪 테스트

- 새 기능 구현 시 단위 테스트 함께 작성 (선택이 아닌 필수)
- 테스트 프레임워크: xUnit
- Mocking: Moq 또는 NSubstitute
- 테스트 파일 위치: `*.Tests` 프로젝트 내 동일한 네임스페이스 구조 유지
- 테스트 커버리지 목표: 핵심 비즈니스 로직 (Application/Domain 레이어) 80% 이상
- 테스트 구조는 `AAA 패턴` 준수:
  ```csharp
  // Arrange - 준비
  // Act - 실행
  // Assert - 검증
  ```
- 외부 의존성(DB, 외부 API)은 반드시 mock 처리
- 테스트 메서드명은 한국어로 명확하게:
  ```csharp
  [Fact]
  public async Task 이메일_형식이_잘못된_경우_ValidationException을_반환한다()
  ```
- Integration 테스트: `WebApplicationFactory` 사용
- E2E 테스트: 주요 유저 플로우는 Playwright로 작성

---

## 📁 파일 생성 규칙

- 새 API 엔드포인트 추가 시 `docs/API.md`도 함께 업데이트
- DB 스키마 변경 시 EF Core 마이그레이션 파일 반드시 생성 (`dotnet ef migrations add`)
- 직접 DB 스키마 수정 금지
- 공통으로 사용되는 타입/DTO는 `Application/DTOs/` 디렉토리에 정의
- 새 서비스 추가 시 인터페이스 먼저 정의 후 구현체 작성
- 프론트엔드 새 컴포넌트 생성 시 같은 디렉토리에 `index.ts` barrel export 유지

---

## 📝 Git 커밋/브랜치 규칙

### 브랜치 전략

```
main         # 프로덕션 배포 브랜치 (직접 push 금지)
develop      # 평소 작업 브랜치
hotfix/      # 긴급 프로덕션 수정 (예: hotfix/payment-error)
```

- 모든 작업은 `develop`에서 진행
- 기능 완성 후 `develop → main` 머지 시 자동 배포
- 긴급 수정만 `hotfix/` 브랜치를 `main`에서 분기해서 처리

### 커밋 메시지 컨벤션 (Conventional Commits)

```
<type>: <한국어 설명>

feat: 유저 로그인 기능 추가
fix: JWT 토큰 만료 시 리다이렉트 오류 수정
docs: API 명세 업데이트
style: 코드 포맷 정리
refactor: UserService 레이어 분리
test: 로그인 단위 테스트 추가
chore: NuGet 패키지 업데이트
```

### 커밋 규칙

- 하나의 커밋은 하나의 목적만 가질 것 (기능 + 버그수정 혼합 금지)
- 커밋 전 반드시 `lint`, `build` 통과 확인
- `main` 브랜치에 직접 push 금지 — 반드시 `develop`에서 머지
- 머지 방식: `Squash and Merge` 사용 (히스토리 깔끔하게 유지)
- `.env`, `appsettings.local.json` 등 민감한 파일 커밋 금지
- 커밋 메시지에 비밀번호, 토큰 등 민감 정보 포함 금지

---

## 🚀 서버 배포 규칙

### 배포 흐름

```
develop 작업 → 테스트 통과 → develop → main 머지 → 자동 배포 → Production
```

### 배포 전 체크리스트

- [ ] 모든 테스트 통과 확인 (`dotnet test` / `npm run test`)
- [ ] 빌드 오류 없음 확인 (`dotnet build` / `npm run build`)
- [ ] 새로운 환경변수가 있다면 서버에 미리 등록
- [ ] DB 마이그레이션이 있다면 배포 전 별도 적용
- [ ] `docs/PROGRESS.md` 배포 내용 업데이트

### 배포 규칙

- 배포 실패 시 즉시 이전 버전으로 롤백
- 롤백 방법을 항상 사전에 확인해두고 배포할 것

### GitHub Actions CI/CD

- `develop` push 시 자동으로 빌드 + 테스트 실행
- 테스트 실패 시 `main` 머지 불가
- `main` 머지 시 자동 프로덕션 배포 트리거

---

## 🚫 하지 말아야 할 것들

- `Console.WriteLine` 디버깅 코드 커밋 금지 (Serilog 사용)
- `.Result`, `.Wait()` 사용 금지
- `var` 남용 금지 — 타입이 불명확한 경우 명시적 타입 선언
- `dynamic` 타입 사용 금지
- `static` 클래스/메서드 남용 금지 (DI 원칙 위반)
- 미사용 using, 변수 방치 금지
- 하나의 PR에 너무 많은 변경사항 포함 금지
