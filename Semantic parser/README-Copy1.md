# fincase_semantic_parser

How to train the parser (bash):

    python cli_parser.py train --dataset data/train.csv --data-type tsv --config config.json

How to apply the parser to a utf-8 text file, with items separated by newline (bash):
    
    python cli_parser.py predict --in-file tests/small_test.tsv --config config.json --out-file tests/small_test_result.tsv

This command should write a tab-separated file with result of parsing.

How to apply the parser in interactive mode (python3):
    
    from semantic_parser import SemanticParser
    parser = SemanticParser('config.json')
    print(parser.parse('предлагаю нежилое помещение на 1 этаже, общий вход со двора'))
    
This code should print a dictionary like

    {'entrance_placement': 'yard', 'purpose': 'non_residential', 'floor': 1}
