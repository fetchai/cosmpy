from typing import Any, Dict, List, Optional, Union

Primitive = Union[str, int, bool, float]
_JSONDict = Dict[Any, Any]  # temporary placeholder
_JSONList = List[Any]  # temporary placeholder
_JSONType = Optional[Union[Primitive, _JSONDict, _JSONList]]
JSONLike = Dict[str, _JSONType]

