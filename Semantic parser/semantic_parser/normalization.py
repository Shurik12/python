
ALLOWED_TARGETS = {
    'Жилое/Не Жилое': [False, True],
    'Линия затройки': ['Первая линия', 'Внутриквартальная'],
    'Наличие витринных окон': [False, True],
    'Наличие коммунальных платежей': [False, True],
    'Тип входа': [
        'Отдельный с улицы',
        'Общий с улицы',
        'Отдельный со двора',
        'Общий со двора'
    ],
    'Тип отделки': [
        'Типовой ремонт',
        'Под чистовую отделку',
        'Дизайнерский ремонт',
        'Требуется косметический ремонт',
        'Требуется капитальный ремонт',
        'Офисная отделка'
    ],
    'ндс вкл/невкл': ['Ндс включен', 'Ндс не включен']
}

UNKNOWN_VALUE = 'unknown'

WORD_SYNSET = {
    'Тип входа': {
        'обший': 'общий',
        'отдельно': 'отдельный', 
        'отдельной': 'отдельный', 
        'отдельныйс': 'отдельный с',
        'улица': 'улицы'
    }, 
    'Линия затройки': {
        'внутриквартальное': 'внутриквартальная'
    }, 
    'Тип отделки': {
        'ремнт': 'ремонт', 
        'требует': 'требуется', 
        'ремонта': 'ремонт'
    }
}

TARGET_SYNSET = {
    'Линия затройки': {
        'Первая': 'Первая линия'
    },
    'Тип отделки': {
        'Типовой': 'Типовой ремонт',
        'Чистовая отделка': 'Под чистовую отделку',
        'Без ремонт': 'Без отделки'
    }
}


name2code = {
    "Тип входа": 'entrance_type',
    "Наличие витринных окон": 'display_window',
    "Линия затройки": 'building_line',
    "Тип отделки": 'renovation',
    "Жилое/Не Жилое": 'purpose',
    "Наличие коммунальных платежей": 'communal_included',
    "ндс вкл/невкл": 'vat_included'
}


def normalize_target(target_value, target_name=None, only_allowed=False):
    if isinstance(target_value, str):
        target_value = target_value.lower().strip().replace('.', '')
        words = target_value.split()
        new_words = []
        synset = WORD_SYNSET.get(target_name, {})
        for w in words:
            new_words.append(synset.get(w, w))
        target_value = ' '.join(new_words).capitalize()
    synset = TARGET_SYNSET.get(target_name, {})
    target_value = synset.get(target_value, target_value)
    if only_allowed:
        assert target_name, 'To leave only allowed values, target name is required.'
        if target_value not in ALLOWED_TARGETS[target_name]:
            target_value = UNKNOWN_VALUE
        target_value = str(target_value)
    return target_value
