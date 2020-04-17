# fincase_semantic_parser

How to train the parser (bash):

    python3 cli_parser.py train --dataset data/train.csv --data-type tsv --config config.json

How to apply the parser to a utf-8 text file, with items separated by newline (bash):
    
    python3 cli_parser.py predict --in-file tests/small_test.tsv --config config.json --out-file tests/small_test_result.tsv

This command should write a tab-separated file with result of parsing.

How to apply the parser in interactive mode (python3):
    
    from semantic_parser import SemanticParser
    parser = SemanticParser('config.json')
    print(parser.parse('предлагаю нежилое помещение на 1 этаже, общий вход со двора'))
    
This code should print a dictionary like

    {'entrance_placement': 'yard', 'purpose': 'non_residential', 'floor': 1}


How to run in Ubuntu for PostgreSQL:


cd "Рабочий стол"/semantic_parser-master
python3 cli_parser.py predictpostgresql --table "buildings_lease"
python3 cli_parser.py predictpostgresql --table "businesses"
python3 cli_parser.py predictpostgresql --table "businesses_lease"
python3 cli_parser.py predictpostgresql --table "garages_lease1"
python3 cli_parser.py predictpostgresql --table "buildings_lease"
python3 cli_parser.py predictpostgresql --table "garages"
python3 cli_parser.py predictpostgresql --table "garages_lease"
python3 cli_parser.py predictpostgresql --table "buildings_offices_shoppings_free_lease"
python3 cli_parser.py predictpostgresql --table "buildings_industrials_warehouses_lease"
python3 cli_parser.py predictpostgresql --table "placements_depr"
python3 cli_parser.py predictpostgresql --table "placements_depr_lease"
python3 cli_parser.py predictpostgresql --table "buildings"
python3 cli_parser.py predictpostgresql --table "buildings_lease"
python3 cli_parser.py predictpostgresql --table "placements_lease"
python3 cli_parser.py predictpostgresql --table "shoppings_lease"
python3 cli_parser.py predictpostgresql --table "shoppings"
python3 cli_parser.py predictpostgresql --table "placements"
python3 cli_parser.py predictpostgresql --table "industrials_warehouses"
python3 cli_parser.py predictpostgresql --table "buildings_industrials_warehouses"
python3 cli_parser.py predictpostgresql --table "buildings_offices_shoppings_free"
python3 cli_parser.py predictpostgresql --table "industrials_warehouses_lease"
python3 cli_parser.py predictpostgresql --table "offices_lease"
python3 cli_parser.py predictpostgresql --table "offices"
python3 cli_parser.py predictpostgresql --table "warehouses"
python3 cli_parser.py predictpostgresql --table "warehouses_lease"
python3 cli_parser.py predictpostgresql --table "industrials"
python3 cli_parser.py predictpostgresql --table "industrials_lease"
python3 cli_parser.py predictpostgresql --table "lands"
