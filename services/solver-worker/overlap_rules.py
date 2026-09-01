"""托盘膜叠膜的单位和高度判定规则。

外部货物规格的宽度单位为mm，算法及页面的两个膜叠膜高度上限单位为cm。
"""

import math


MM_PER_CM = 10.0
HEIGHT_EPSILON_CM = 1e-7


def roll_width_mm_to_cm(width_mm):
    """将货物规格宽度(mm)换算为叠膜判定高度(cm)。"""
    return float(width_mm) / MM_PER_CM


def parse_overlap_limits_cm(config):
    """
    返回 ``(overlap_enabled, single_limit_cm, total_limit_cm)``。

    开启膜叠膜时，两个限制都必须是有限正数；关闭时返回两个0。
    """
    overlap_enabled = config.get("overlap") is True or str(config.get("overlap")).lower() == "true"
    if not overlap_enabled:
        return False, 0.0, 0.0

    single_limit = _positive_number(config.get("single_max_height"), "单层膜卷本体高度上限")
    total_limit = _positive_number(config.get("entire_max_height"), "叠后膜卷本体总高度上限")
    return True, single_limit, total_limit


def can_stack_layer(base_partno, candidate_partno, base_is_mixed, candidate_is_mixed,
                    base_goods_height_cm, candidate_goods_height_cm,
                    stacked_goods_height_cm, single_limit_cm, total_limit_cm):
    """判断候选小托能否加到当前膜叠膜组合。"""
    if base_is_mixed or candidate_is_mixed or base_partno != candidate_partno:
        return False

    single_limit = float(single_limit_cm)
    total_limit = float(total_limit_cm)
    base_height = float(base_goods_height_cm)
    candidate_height = float(candidate_goods_height_cm)
    stacked_height = float(stacked_goods_height_cm)

    return (
        base_height <= single_limit + HEIGHT_EPSILON_CM
        and candidate_height <= single_limit + HEIGHT_EPSILON_CM
        and stacked_height + candidate_height <= total_limit + HEIGHT_EPSILON_CM
    )


def _positive_number(value, field_label):
    if value is None or value == "":
        raise ValueError(f"开启膜叠膜时必须填写{field_label}(cm)")
    if isinstance(value, bool):
        raise ValueError(f"{field_label}必须是大于0的数字，单位cm")

    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_label}必须是大于0的数字，单位cm")

    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{field_label}必须是大于0的数字，单位cm")
    return number
