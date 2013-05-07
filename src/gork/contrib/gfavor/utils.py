# -*- coding: utf-8 -*-
from gfavor.settings import *


def build_message(count):
    if count == 0:
        return ''
    if count == 1:
        return FAV_COUNT_SINGLE % 1
    if int(str(count)[-1:]) in FAV_COUNT_PLURAL_SPECIAL_LASTNUMBERS:
        return FAV_COUNT_PLURAL_SPECIAL % count
    return FAV_COUNT_PLURAL % count
