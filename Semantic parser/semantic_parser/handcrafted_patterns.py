ENTRANCE_RE = '(вы?ход(|ом|ами|а|ы|н.. групп.)(\sи витринное остекление)?)'

NOT_INCLUDED = '(оплачива[юе]тся отдельно|не вход[яи]т в стоимость аренды|без уч[её]та|не включ(ая|ает|ен[ыоа]?)|без)( в себя)?'  # noqa
INCLUDED = '((уже )?(включа([ею]т|я)|включен[ыо]?|вход[ия]т|с уч[её]том)( в себя)?)'

RATE = '(цен.|ставк.|стоимост.)'
RENT_RATE = '({r} (аренды|арендной платы)|арендн.. {r}|{r}|арендн.. плат.)'.format(r=RATE)
ROUBLE = '(р(уб(л(ей|ь))?)?)'
RATE_VALUE = '[0-9 ]*'+ ROUBLE+'?( в (месяц|год))?( за( 1)?( кв)? (м|метр))?'
RENT_RATE_WITH_VALUE = RENT_RATE + RATE_VALUE

INCLUDED_TEMPLATE = '.*(' + RENT_RATE_WITH_VALUE +  ' ' + INCLUDED + '( вс[её] с)? {what}|{what} ' + INCLUDED + ' в ' + RENT_RATE_WITH_VALUE + ')'  # noqa
NOT_INCLUDED_TEMPLATE = '.*(' + NOT_INCLUDED + '\s*{what}|{what}\s*' + NOT_INCLUDED + ')'

NDS = 'ндс'

OTHER_SERVICES = '(предоставление юридического адреса|эксплуатация)'
EXPENCE = '(затраты|расходы|платежи|услуги|оплаты)'
ANY_COMMUNAL = '({exp} (на|за) (электричество|электроэнергию|отопление|освещение|воду)|((эксплуатационные|коммунальные) и )?(эксплуатационные|коммунальные) {exp})'.format(exp=EXPENCE)  # noqa

COMMUNAL = '(({other},*\s*)*{any_communal}+)'.format(other=OTHER_SERVICES, any_communal=ANY_COMMUNAL)
NDS_WITH_COMMUNAL = '('+COMMUNAL+' )?(и )?' + NDS + '( и)?( ' + COMMUNAL+')?'
COMMUNAL_WITH_NDS = '('+NDS+' )?(и )?' + COMMUNAL + '( и)?( ' + NDS+')?'

NEEDED = '(требует(ся)?|необходимо?|нуждается в|нужен|под)( провести| сделать)?( как минимум)?( мелкий)?'
NEEDED_PATTERN = '.*' + NEEDED + '\s*{what}'

AREA = '(\s*(зал)?\s*\d+\s*(кв.\s*м|метров|м2?).?\s*)'
FIRST_FLOOR = '((?!(\-|минус))\s*(?!\d)(1-й|1|перв..)( ?этаж)?.?)'
BASEMENT_OR_GROUND = '((подвал|цоколь?)(но. помещени.)?)'

NAMEDLIST_TEMPLATE = '.*{}\s*\-*\s*{}\s*,?\s*и?\s*{}\s*\-?\s*{}'

RECENT = '(сделан|новый|выполнен|завершен|недавно|закончил(и|ся)|закончен|свеж(ий|его))'

regexes = {
    'entrance': {
        'yard': '.*' + ENTRANCE_RE + ' ([св]о?|на)(\s*(территори.|сторон.))?\s*(двор|жк|жило..? комплекс)',
        'street': '.*' + ENTRANCE_RE + ' (с|со стороны|на|к) улиц',
        'both': '((c|на|со стороны) улиц. и (cо?|во|на|со стороны) двор|(cо?|во|на|со стороны) двор.? и (c|на|со стороны) улиц.)'  # noqa
    },
    'entrance_type': {
        'separate': [
            '.*отдельн(ый|ые|ым|ыми|ых)\s+' + ENTRANCE_RE,
            '.*{entr}\s+(\d\s+)?отдельн(ый|ые|ым|ыми|ых)'.format(entr=ENTRANCE_RE)
        ],
        'joint': ['.*общ(ий|ие|им|ими|их)\s' + ENTRANCE_RE, '.*{entr}\s+общ(ий|ие|им|ими|их)'.format(entr=ENTRANCE_RE)],
    }, 
    'hasshopwindows': {
        'display_window': ['.*витрин', '.*витринн.. (окна|остекление)']
    }, 
    'houselinetype': {
        'first': '.*(перв|1)\-? ?(ая|ой|я)? лини(я|и)',
        'secondary': '.*(перв|1)\-? ?(ая|ой|я)? второстепенн.. лини(я|и)',
        'inner': ['.*(втор|2)\-? ?(ая|ой|я)? лини(я|и)'],
    }, 
    'conditiontype': {
        "standard": [
            '.*(типов|стандартн).. ((евро)?ремонт|отделк)',
            '.*(после|выполнен| с|свежий) косметическ...? (ремонт|отделк)'
        ],
        "designer": '.*дизайнерск.. ((евро)?ремонт|отделк)',
        "office": '.*офисн.. ((евро)?ремонт|отделк)',
        "capital_needed": NEEDED_PATTERN.format(what='(капитальный ремонт|кап.? ?ремонт)'),
        "clean_needed": '.*под чистовую',
        "cosmetic_needed": NEEDED_PATTERN.format(what='косметическ...? (ремонт|отделк)'),
        "some": [
            "помещение (отделано|отремонтировано)",
            '.*не требует(ся)? ремонт', '.*ремонта? не требует(ся)?',
            '.*{} ремонт'.format(RECENT)
        ],
        "some_needed":  [
            '.*((под|требуется) (отделк|ремонт)(?!( обуви| одежды| ювелирных| сотовых| телефонов|н(ую|ая) мастерск))|частично отремонтирован)',  # noqa
            '.*shell\s*core',
            '.*(?!не) требует (отделк|ремонт)',
            '.* без отделки'
        ]
    }, 
    'isbuildingliving': {
        'non_residential': [
            '.*нежилое',
            '(торговое помещение|отдел в магазине|в .*магазине сдается отдел|в (тц|торговом центре)|торговая площадь)',
            r'.*\bпод (магазин|кафе|ресторан|банк|пекарн|автосервис|автомойк|офис|салон|супермаркет|универсам|(не)?продуктов|(не)?продовольствен|аптек|мастерск|студи|шоу)'
        ],
        'residential': ['(.* жилое)|(оборудовано под хостел)', '.*как жилое', 'жиль[её]']
    }, 
    'communal_included': {
        'included': [
            INCLUDED_TEMPLATE.format(what=COMMUNAL_WITH_NDS),
            '.*( с|(?!не ) [ув]ключ...?|стоимость вход.ит|(?!не )вкл.?)\:?( стоимость)? (коммуна|ку|к\/у|комм.?\s*платежи)',  # noqa
            '.*ком(мунальные)?.? (платежи|услуги|ку|к\/у)( уже)? (включен|входя)',
            '.*(все платежи включены|вс[её] включено)'
        ],
        'not_included': [
            NOT_INCLUDED_TEMPLATE.format(what=COMMUNAL_WITH_NDS),
            '.*по сч[её]тчикам',
            '.*по факту потребления',
            '.*\+\s*{}'.format(COMMUNAL)
        ]
    }, 
    'vattype': { 
        'included': [INCLUDED_TEMPLATE.format(what=NDS_WITH_COMMUNAL), '.*(c|включая) ндс'],
        'not_included': [NOT_INCLUDED_TEMPLATE.format(what=NDS_WITH_COMMUNAL), '.*(без|\+) ндс'],
        'usn': r'.*\bусн\b',
    }, 
    'floornumber': {
        'first': ['.*(?!(\-|минус))\s*(?!\d)(перв|1)\s*\-?\s*(ый|ом|й|м)?\s*этаж', r'.*\b1(\s*\/\s*\d+)?\s*этаж'],
        'second': ['.*(?!(\-|минус))\s*(?!\d)(втор|2)\s*\-?\s*(ой|ом|й|м)?\s*этаж', r'.*\b2(\s*\/\s*\d+)?\s*этаж'],
        'fpb': [
            r'.*(?!(\-|минус))\s*(перв..|1) этаж.*\b(подвал|цоколь)',
            '.*на (1|первом) этаже и в (подвал|цокол)',
            NAMEDLIST_TEMPLATE.format(FIRST_FLOOR, AREA, BASEMENT_OR_GROUND, AREA),
            NAMEDLIST_TEMPLATE.format(AREA, FIRST_FLOOR, AREA, BASEMENT_OR_GROUND),
            NAMEDLIST_TEMPLATE.format(BASEMENT_OR_GROUND, AREA, FIRST_FLOOR, AREA),
            NAMEDLIST_TEMPLATE.format(AREA, BASEMENT_OR_GROUND, AREA, FIRST_FLOOR),
        ],
        'basement': r'.*(\bподвал|\-(1|перв..)этаж)',
        'ground': '.*(цоколь|полуподвал)',
        'building': '.*(отдельно стояще|отдельно. здани)',
        'multiple': ['.*уровнево', '.*(1-?й?м?) этаж.*(2-?й?м?) этаж', '{} .*антресол'.format(FIRST_FLOOR)],
        'higher': '.*(\d\d+|[2-9])\s*эт'
    }
}

FEATURE_EXPRESSIONS = [
    ['building_with_separate_entrance', '.*(ангар)'],
    ['two_levels__0', '.*(на (2-?х?|двух) этажах)'],
    ['cosmetic', '.*косметическ...? ремонт'],
    ['after_cap', 'после (кап.?|капитального)\s?ремонта']
]

for label_name, label_expressions in regexes.items():
    for class_name, class_expressions in label_expressions.items():
        if isinstance(class_expressions, str):
            class_expressions = [class_expressions]
        for i, expression in enumerate(class_expressions):
            FEATURE_EXPRESSIONS.append(['{}__{}__{}'.format(label_name, class_name, i), expression])
