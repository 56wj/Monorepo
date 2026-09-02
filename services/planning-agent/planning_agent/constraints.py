import re
from typing import Any, Dict, List, Optional, Tuple


NUMBER = r"(\d+(?:\.\d+)?)"
UNIT = r"(kg|KG|千克|公斤|t|T|吨|mm|MM|毫米|cm|CM|厘米|m|M|米)?"


FIELD_PATTERNS = {
    "max_weight_kg": [
        re.compile(r"(?:最大(?:载重|承重)|载重上限|max(?:imum)?\s*(?:load|weight))\s*[:：]?\s*" + NUMBER + r"\s*" + UNIT),
    ],
    "max_height_mm": [
        re.compile(r"(?:最大高度|高度上限|max(?:imum)?\s*height)\s*[:：]?\s*" + NUMBER + r"\s*" + UNIT),
    ],
    "roll_diameter_mm": [
        re.compile(r"(?:纸卷|卷材|卷筒)?(?:直径|外径|diameter)\s*[:：]?\s*" + NUMBER + r"\s*" + UNIT),
    ],
    "roll_weight_kg": [
        re.compile(r"(?:单卷(?:重量|重)|纸卷重量|卷重|roll\s*weight)\s*[:：]?\s*" + NUMBER + r"\s*" + UNIT),
    ],
}


def extract_constraints(query: str, order_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    constraints: Dict[str, Any] = {}
    context = order_context or {}
    for key in FIELD_PATTERNS:
        if key in context and context[key] is not None:
            constraints[key] = _positive_number(context[key], key)

    for key, patterns in FIELD_PATTERNS.items():
        for pattern in patterns:
            match = pattern.search(query)
            if match:
                constraints[key] = _normalize(float(match.group(1)), match.group(2), key)
                break

    if re.search(r"(?:禁止|不允许|不能|不可|不要)混装|分批装载", query):
        constraints["allow_mixed_batch"] = False
    elif re.search(r"(?:允许|可以|可)混装", query):
        constraints["allow_mixed_batch"] = True
    elif "allow_mixed_batch" in context:
        constraints["allow_mixed_batch"] = bool(context["allow_mixed_batch"])

    if re.search(r"悬挂|吊装|suspend", query, re.IGNORECASE):
        constraints["packing_mode"] = "SUSPEND"
    elif re.search(r"二次(?:装箱|规划)|second", query, re.IGNORECASE):
        constraints["packing_mode"] = "PALLET_SECOND"
    else:
        constraints["packing_mode"] = str(context.get("packing_mode", "PALLET"))

    if re.search(r"利用率|空间最优|装载率", query):
        constraints["optimization_goal"] = "MAX_UTILIZATION"
    elif re.search(r"最少(?:托盘|车次|车辆)|减少(?:托盘|车次)", query):
        constraints["optimization_goal"] = "MIN_CONTAINER_COUNT"
    else:
        constraints["optimization_goal"] = str(context.get("optimization_goal", "BALANCED"))
    return constraints


def validate_constraints(constraints: Dict[str, Any]) -> Tuple[List[str], List[str], List[str]]:
    required = ["max_weight_kg", "max_height_mm"]
    missing = [field for field in required if field not in constraints]
    violations: List[str] = []
    warnings: List[str] = []

    for field in ("max_weight_kg", "max_height_mm", "roll_diameter_mm", "roll_weight_kg"):
        value = constraints.get(field)
        if value is not None and value <= 0:
            violations.append(f"{field} must be positive")
    if constraints.get("roll_weight_kg", 0) > constraints.get("max_weight_kg", float("inf")):
        violations.append("roll_weight_kg exceeds max_weight_kg")
    if constraints.get("max_height_mm", 0) > 5000:
        warnings.append("max_height_mm is outside the normal synthetic fixture range")
    if constraints.get("allow_mixed_batch") is None:
        warnings.append("allow_mixed_batch was not specified; downstream default applies")
    return missing, violations, warnings


def job_type_for(constraints: Dict[str, Any]) -> str:
    mode = constraints.get("packing_mode")
    if mode == "SUSPEND":
        return "SUSPEND_FIRST"
    if mode == "PALLET_SECOND":
        return "PALLET_SECOND"
    return "PALLET_FIRST"


def _positive_number(value: Any, field: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field} must be numeric") from error


def _normalize(value: float, unit: Optional[str], field: str) -> float:
    normalized_unit = (unit or ("kg" if field.endswith("_kg") else "mm")).lower()
    if field.endswith("_kg"):
        if normalized_unit in ("t", "吨"):
            value *= 1000
        elif normalized_unit not in ("kg", "千克", "公斤"):
            raise ValueError(f"invalid weight unit for {field}: {unit}")
    else:
        if normalized_unit in ("m", "米"):
            value *= 1000
        elif normalized_unit in ("cm", "厘米"):
            value *= 10
        elif normalized_unit not in ("mm", "毫米"):
            raise ValueError(f"invalid length unit for {field}: {unit}")
    return round(value, 3)
