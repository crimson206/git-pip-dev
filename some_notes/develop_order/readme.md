

- git-pip core
    개발이 간단함. code를 외부에 공개하지 않고서 mwd를 이어나갈 수 있음

- git-pip db
    git-pip을 pypi에서 검색하며 쓰는 것 처럼 쓰기 위해서 우선적으로 필요함
    mwd를 위해서도 당연히 사용될 수 있음

- dep-frontend
    dependency를 그려주는 .ts 모듈이 될 것.
    그냥 가벼운 network를 생성해주는 모듈을 개발시 빠르게 개발 가능. git-pip db와 일찍이 사용가능

- git-pip frontend
    git-pip db와 관련된 기능들을 사용하기 위한 곳
    이것 없이도 위의 기능들을 개발하고 사용하는데 문제가 없음.

- mwd git-core
    git-pip 관련 대부분의 모듈들이 이미 개발되는 것이 좋음
    ai를 여기서 개발하지 않을 것임. 대신에 AI가 사용할 툴을 제공하는 것이 중요
    때에 따라서 여러 repository를 clone하거나 하는 것이 필요한 것
    pre publish에 신경을 쓸 것. 다른 모듈들에 가해지는 충격을 줄임. 어차피 자동화. pre publish를 귀찮아 하지 말 것.
    abstraction들의 경우, db로 부터 한번에 모을 수 있음.
    abstraction의 경우 용량을 제한하는 옵션을 둘 것. 길면 애초에 mwd가 아니고, ai가 읽을 수 없음.
    더 큰 data는 repository를 클론해서, 모든 파일을 거기서 참고할 것.

- mwd-pip
    mwd를 적용하요 개발되는 pypi모듈들의 경우, 설정들이 필요할 것인데,
    그 설정을 위한 것. 기존의 pypi나 git-pip을 쓰지만, 여기에 abstraction과 같은 부분을 유저들이 설정하게 하는 것이 필요


- mwd-frontend
    microwise의 homepage를 개발하는 일
    mwd git-core, dep-frontend, git-pip 등등을 소개할 것
    git-pip의 경우, git-pip의 기능성에 신경쓸 것. mwd는 이후에 여기서 제공되는 정보를 재구성하여 역할을 수행하는 것으로 늦지 않음

- mwd-automation
    하나씩 개발하면서 별로라도 공개해 나갈 것임
    공모페이지를 언제 만들지?


- py-completion
    여기에 cil를 정의해는 부분을 두지 말 것.
    python과 상관없이, 여러 언어에서 사용할 수 있는 모듈을 만들어줄 것.

- py-cil
    cil는 여기서 구현. 나중에 py-completion의 도움을 받을 것.

- mwd dependency bot
    db에 있는 data를 기반으로 dependency를 수정할 부분을 추적해야 하는데,
    필요할 시, 자동으로 test를 수행해서, dependency의 범위를 한정지을 것.
    기본적으로 위쪽 방향으로 열어두지만, dependency의 새 버전이 update시 test진행, fail하면 dependency범위를 닫아 줌.
    mwd db에 dependency범위를 저장해두고, 

- git-pip to pypi?
    그냥 알아서 하면 되는거 아님? 뭐 팀단위로, 수많은 모듈을 공개하고 싶으면 필요할 수 있겠다.

- ts로 확장할 것

- 다른 언어들에 대한 확장?
    투자가 필요함. 내가 개발할 수 있는 부분이 아님.
