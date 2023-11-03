import re

with open("frosttypes/types.py", "r") as f:
    content = f.read()
    content_new = content.replace(
        "from typing import Any", "from typing import TypeVar"
    )
    content_new = content_new.replace(
        "Model = Any",
        """
        FrostType = TypeVar("FrostType", str, int, float)
        class RequestsResonseJsonError(TypedDict):
            code: NotRequired[str]
            message: NotRequired[str]
            reason: NotRequired[str]
        """,
    )
    content_new = content_new.replace(" Any", " str | int | float")
    content_new = re.sub("class (\w*)", r"class Frost\1", content_new, flags=re.M)
    content_new = re.sub(
        "(\w*)( = TypedDict\(\n\s*')(\w*)0",
        r"Frost\1\2Frost\3",
        content_new,
        flags=re.M,
    )
    content_new = re.sub(
        "\[(?!List|NotRequired|Dict)([A-Z]\ w*)", r"[Frost\1", content_new, flags=re.M
    )

with open("frosttypes/fixed-types.py", "w") as f:
    f.write(content_new)
