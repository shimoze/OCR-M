MODELS_CONFIG = {
    "v4": {
        "mobile": {
            "det": {
                "default": "ch",   # детектор почти всегда общий
            },
            "rec": {
                "ch": "ch",
                "en": "en",
                "ru": "ru",
                "latin": "latin"
            }
        },
        "server": {
            "det": {
                "default": "ch",
            },
            "rec": {
                "ch": "ch",
                "en": "en",
                "ru": "ru",
                "latin": "latin"
            }
        }
    },

    "v5": {
        "mobile": {
            "det": {
                "default": "ch",
            },
            "rec": {
                "ch": "ch",
                "en": "en"
            }
        },
        "server": {
            "det": {
                "default": "ch",
            },
            "rec": {
                "ch": "ch",
                "en": "en"
            }
        }
    }
}