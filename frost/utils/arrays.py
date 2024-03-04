from typing import List


def param_to_array(param: str | List[str]) -> List[str]:
    """Utillity function to make sure that input param is a list of strings

    :param str | List[str] param: the input, either a string or a list
    :return List[str]: returns a list of strings
    """
    _params = []
    if type(param) == str:
        _params = param.split(",")

    for _p in _params:
        _p = _p.strip()

    return _params


def array_to_param(param: str | List[str] | None) -> str | None:
    if param == None:
        return None

    _param = param if type(param) == str else ""

    if type(param) == list:
        for _p in param:
            _p = _p.strip()

        _param = ",".join(param)

    _param = _param.strip()

    return _param
