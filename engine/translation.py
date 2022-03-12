# -*- coding: iso-8859-1 -*-
"""
Functions that helps doing translations
"""

CURRENT_LANGUAGE = "en"

"""
Add the following lines to use the translation

import engine.translation
_ = engine.translation.translate
translated text = _("msg.key") 
"""

def translate(key, language = CURRENT_LANGUAGE):
    if key in translations_dict and language in translations_dict[key]:
        return translations_dict[key][language]
    else:
        return key

translations_dict = {
    "test": {
        "fr": "test-fr",
        "en": "test-en"
    },
    "welcome.loading.menu": {
        "fr": "Creation du menu...",
        "en": "Create the menu..."
    },
    "welcome.loading.music": {
        "fr": "Chargement de la musique...",
        "en": "Loading music..."
    },
    "welcome.loading.1st-board": {
        "fr": "Chargement du premier plateau...",
        "en": "Loading first board..."
    },
    "welcome.loading.widgets": {
        "fr": "Chargement des widgets...",
        "en": "Loading widgets..."
    },
    "welcome.loading.done": {
        "fr": "Termine !",
        "en": "Done !"
    },
    "action.on_simple_object.take": {
        "fr": "Prendre",
        "en": "Take"
    },
    "action.on_simple_object.cancel": {
        "fr": "Annuler",
        "en": "Cancel"
    },
    "inventory.widget.objects-count": {
        "fr": "objets",
        "en": "items"
    }
    
}
