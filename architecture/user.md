기본설치

git-pip install user/repo==version

유저등록

crimson206 -> crimson or cm
여러개 등록 허용해줘?

git-pip install -cm my-module

여기서 모듈이름은 그대로 가져와서 깔게 할 것.

git-pip module-name (--mm) user/repo

이러면 my-module이 뜰 것.

저기서 여러개 쓰는 옵션을 허락 안하는게 좋을 듯.

micro wise development를 할 것을 고려하여, crimson.my_module같은 식의 약속이 정해지는 것이 좋음.

---


그냥 public 공간에서 namespace가 겹칠 시, user_name을 명시해서 구분하는 식으로 하는게 좋을 듯.


git-pip install -cm my-module

error, there are at least two `-cm my-module`s.
please clarify the git id.

git-pip install -crimson206 -cm my-module

이런 식으로 사용하게.

그런데, 저거 -가 너무 많이 쓰이면서, 컨트롤이 복잡해질건데,

git-pip install -gi crimson206 -ns cm my-module

이런 식으로 설치하게 해야겠네.

git-pip install -ns cm my-module

그럼 기본적으로 이렇게 설치하고.
그럼 보통 유저가 code로부터 예상해야하는 구조는

from cm.my_module import 알아서 하시고 


이런 식으로 설치하게 하고.

각각의 private git-pip team들이 team-name을 가질 수 있는데,
그럼 -gi 대신에, -tn 으로 대체할 수도 있는거고. tn에서는 하나의 -ns에서 동일한 모듈이름이 허락이 안될거니깐.

---


필요한 것들.

team을 구성하게 해줄 것.

team에 git user를 받는 식으로 team을 키울 수 있음.

그럼 team에서는 어떻게 서로의 모듈에 접근하는가?

뭐 본인들의 github 설정에서 알아서 해야지.

대신에 vscode 같은 곳에서 login하면, 해당 team 계정에 있는 모듈들을 설치가 가능하게 해주고.

해당 team member일 수도 있고(publish할 권한을 가진다는 점에서 특별), 여기서도 서로의 repository의 열람권, contribution등등은 내 소관이 아님.
아니면 해당 팀의 모듈을 설치할 수 있게 권한을 받은 유저일 수도 있고. (해당 팀에게 허가를 받았다는 것이 인증되면, private repo로부터 모듈이 설치 가능. 여전히 repo자체는 열람불가. 이것은 내 service와 상관없음.)


{
    "github_id": "crimson206",
    "team_name": null,  
    "git_pip_name": "cm",
    "namespace": "cm",
    "module_name": "my_module",
    "version": "0.1.2",
    "public": true,
    "hash": "abc123xyz",
    "first_installed_at": "...",
    "last_updated_at": "..."
}

{
    "github_id": "crimson206",
    "team_name": "teamalpha",
    "git_pip_name": "cm",
    "namespace": "core",
    "module_name": "my_module",
    "version": "0.2.0",
    "public": false,
    "hash": null,
    "first_installed_at": "...",
    "last_updated_at": "..."
}

보통 git_pip_name이 namespace가 됨.

namespace를 따로 둘 수 있게 해서, customization 가능하게 허락해줄 것.

- github id: gi
- team name: tn
- git pip name: gpn
- ns: ns

보통 -ns를 두는 것 만으로 충분함.

각각의 유저들은 module이름을 적을 때, 본인의 이름을 추가하는 것 없이, 모듈이름만 적게 허락이 되는 구조.

gitpip.py

설정파일을 쓰게할 것.
이유는 python 자동완성기능을 사용하여, 유저가 설정해야하는 config에 대해 알기 쉽게 해주기 위함.

.yaml도 지원은 해줄 것.

