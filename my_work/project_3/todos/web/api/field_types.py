from typing import Annotated

from fastapi import Path
from pydantic import Field

Min3Field = Annotated[str, Field(min_length=3)]
Min3Max100Field = Annotated[str, Field(min_length=3, max_length=100)]
PriorityField = Annotated[int, Field(ge=1, le=5)]
Min8Field = Annotated[str, Field(min_length=8)]
Id = Annotated[int, Path(ge=1)]
