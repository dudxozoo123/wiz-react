# WIZ React Base Template

[WIZ React IDE](https://github.com/ImuruKevol/wiz-react-ide)

## TODO

> `WIZ React IDE` 와 일괄 관리

### architecture

- [ ] 기존 wiz에서 빌드 구조 변경되면서 사용하지 않는 것들 정리
- [ ] 디렉토리 구조 재설계
- [ ] 페이지, 컴포넌트 단위 설계
- [ ] k8s 컨테이너화

### socket

- [ ] build error message wiz socket 전송
- [ ] 저장 시 실시간 웹 갱신(socket) - watch 기능
    - [ ] webpack-dev-server 검토
    - [ ] nodemon 검토
    - [ ] esbuild watch 기능 확인

### wrapping

- [ ] dictionary 기능 재활성화
- [ ] 라우팅 테이블 수정 페이지 개발
    - 코드 작성 말고 key-value 식의 수정 페이지
    - 오른쪽 사이드 서브 메뉴에?
- [ ] default loading component - not react; window.loading(true); 이런 식으로 사용;
    - 또는 로딩 빌더 개발 - 부모 지정
- [ ] angularjs 사용하기 편하게
    - 현재의 wiz처럼; app.controller 숨기고 앱 단위 코딩;
- [ ] styled-component 기능 개발
    - [ ] styled-component 개발 메뉴 생성
    - [ ] import 시 포맷 설계
- [ ] readme, gitignore 편집 기능

### etc

- [ ] 스토리북?
- [ ] eslint, prettier 오토 포매팅 기능
    - .eslintrc 수정 기능?
- [ ] 커맨드 팔레트 개발
