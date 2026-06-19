# ============================================
# FILE: pixel_sync/i18n.py
# VERSION: 2.0.0
# UPDATED: 2026-06-19
# ============================================

from pixel_sync.settings import LANGUAGE

if LANGUAGE == "ja":
    from pixel_sync.lang.ja import WORDS

elif LANGUAGE == "en":
    from pixel_sync.lang.en import WORDS

else:
    from pixel_sync.lang.ja import WORDS


def tr(key):

    return WORDS.get(key, key)