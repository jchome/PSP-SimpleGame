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
    "menu.item.play": {
        "fr": "Jouer maintenant",
        "en": "Play the game"
    },
    "menu.item.options": {
        "fr": "Options",
        "en": "Options"
    },
    "menu.item.credits": {
        "fr": "Credits",
        "en": "Credits"
    },
    "menu.item.language": {
        "fr": "Langue",
        "en": "Language"
    },
    "menu.item.french": {
        "fr": "Francais",
        "en": "French"
    },
    "menu.item.english": {
        "fr": "Anglais",
        "en": "English"
    },
    "menu.item.back": {
        "fr": "Retour",
        "en": "Back"
    },
    "menu.item.exit": {
        "fr": "Quitter",
        "en": "Exit the game"
    },
    "action.on_simple_object.title": {
        "fr": "Actions sur ",
        "en": "Actions on "
    },
    "action.on_simple_object.take": {
        "fr": "Ramasser",
        "en": "Take"
    },
    "action.on_bonus.take": {
        "fr": "Boire/Manger",
        "en": "Drink/Eat"
    },
    "action.on_simple_object.cancel": {
        "fr": "Annuler",
        "en": "Cancel"
    },
    "inventory.widget.objects-count": {
        "fr": "objets",
        "en": "items"
    },
    "inventory.title": {
        "fr": "Inventaire",
        "en": "Inventory"
    },
    "inventory.action.interaction": {
        "fr": "Interagir",
        "en": "Interact"
    },
    "inventory.action.exit": {
        "fr": "Quitter",
        "en": "Exit"
    },
    "inventory.nothing_selected": {
        "fr": "Aucune selection...",
        "en": "Nothing selected..."
    },
    "category.title.object":{
        "fr": "Objets",
        "en": "Objects"
    },
    "category.title.craft":{
        "fr": "Connaissance",
        "en": "Knowledge"
    }

    
}
