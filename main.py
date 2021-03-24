from check_injections import CheckInjections

analyzer = CheckInjections()
analyzer.reformat('logs.csv', 'only_attacks.csv')

