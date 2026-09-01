

class RotationType:
    RT_LWH = 0
    RT_LHW = 1
    RT_WLH = 2
    RT_WHL = 3
    RT_HLW = 4
    RT_HWL = 5

    ALL = [RT_LWH, RT_LHW, RT_WLH, RT_WHL, RT_HLW, RT_HWL]
    # un upright or un updown
    Notupdown = [RT_LWH, RT_WLH]


class Axis:
    Length = 1
    Width = 0
    Height = 2

    ALL = [Length, Width, Height]

