#!/usr/bin/env python3
# 
# Compile the i18nPropScore_[ln] stats and triples
# Usage:
# $ python3 s3-*.py

import datetime



# Timestamp
utc_datetime0 = datetime.datetime.utcnow()
utc_datetime = utc_datetime0.strftime("%Y-%m-%d %H:%M:%S")
time_now = utc_datetime0.strftime("%Y-%m-%d_%H-%M-%S")


def write_triples(filename, write_data):
    """ Create triples (S, P, O) and write to file
    return: None """
    with open(filename, 'a') as f1:
        f1.write(write_data)


def main():
    """ Main script operations
    return: None """
    # Open triples file
    # Using the demo data:s
    triples = open('output-demo-trans-2').readlines()

    # Setting up new file
    output_file = 'output-trans-i18nPropScore-' + time_now

    # Algo for the i18nPropScore as per paper:
    # Determine `s_l = r / t` for each 'property'
    # where s_l is the localness score
    # r is the presence of the property in a lang (0 or 1)
    # t is the total times property is present across `l` langs
    # => higher scores mean more 'local' 
    # => lower scores means more 'universal', unless '0'
    
    prop_dict = {}

    # Iterate over triples
    for ln in triples:
        ln2 = ln.strip().split('\t')  # strip out newline
        sub  = ln2[0]
        pred = ln2[1]
        pred_site = pred.split('/')[0]  # just the URL i.e. source of the prop.
        pred_prop = pred.split('/')[1]  # just the property, after URL protocol
        obj  = ln2[2]

        # Add property if not present
        if pred_prop not in prop_dict:
            prop_dict[pred_prop] = {'en': 0, 'ko': 0, 'ru': 0, 'zh': 0, 'total': 0}
            # Ex: {'Albums' {'en': 1, 'ko': 0, 'ru': 0, 'zh': 1} ...}
        else:
            # print('Duplicate found, not added.')
            pass

        # Get 'r' and 't'
        # Refactor: use dict of sources and languages to scale more
        if 'google' in pred_site:
            prop_dict[pred_prop]['en'] += 1
            prop_dict[pred_prop]['total'] += 1
        if 'naver' in pred_site:
            prop_dict[pred_prop]['ko'] += 1
            prop_dict[pred_prop]['total'] += 1
        if 'yandex' in pred_site:
            prop_dict[pred_prop]['ru'] += 1
            prop_dict[pred_prop]['total'] += 1
        if 'baidu'  in pred_site:
            prop_dict[pred_prop]['zh'] += 1
            prop_dict[pred_prop]['total'] += 1
    # print(prop_dict)

    # languages are hardcoded for current implementation
    langs = ['en', 'ko', 'ru', 'zh']

    # Calculating i18nPropScore per property and language:
    for prop in prop_dict:
        for lang in langs:
            # Calculate i18nPropScore, `s_l = r / t`
            r_val = 0
            if prop_dict[prop][lang] > 0:
                r_val = 1
            t_val = prop_dict[prop]['total']
            # print(r_val)
            # print(t_val)

            prop_score = r_val / t_val

            triple = prop + '\t' + 'i18nPropScore_' + lang + '\t' + str(prop_score) + '\n'
            # print(triple)
            write_triples(output_file, triple)
            # For the demo data:
            # write_triples('output-demo-trans-i18nPropScore', triple)


if __name__ == "__main__":
    main()
