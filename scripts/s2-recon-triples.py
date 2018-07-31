#!/usr/bin/env python3
# 
# Translate and reconcile triples, and split properties where necessary
# Usage:
# $ python3 s2-*.py

import datetime
import time
from translate import Translator


# Timestamp
utc_datetime0 = datetime.datetime.utcnow()
utc_datetime = utc_datetime0.strftime("%Y-%m-%d %H:%M:%S")
time_now = utc_datetime0.strftime("%Y-%m-%d_%H-%M-%S")


def translate_text(input_text, from_lang, to_lang):
    """ Translate natural language text using the `translate` library
    which uses the MyMemory data source. If limited, other SOTA machine 
    or expert translation must be applied.
    return: text: str - resulting translated text """
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    text = translator.translate(input_text)
    return text


def write_triples(filename, write_data):
    """ Create triples (S, P, O) and write to file
    return: None """
    with open(filename, 'a') as f1:
        f1.write(write_data)


def recon_triples_CLI(input_data, output_filename):
    """ Interactive CLI to finetune reconciliation.
    For small datasets, manually adjusting the triples may be faster.
    return: None """
    triples = open(input_data).readlines()

    # Iterate over the translated triples
    count = 0
    for ln in triples:
        ln2 = ln.strip().split('\t')  # strip out newline
        sub  = ln2[0]
        pred = ln2[1]
        pred_site = pred.split('/')[0]  # just the URL i.e. source of the prop.
        pred_prop = pred.split('/')[1]  # just the property, after URL protocol
        obj  = ln2[2]

        # Starting interactive CLI
        count += 1
        print('\n[*] Triple #' + str(count) + ' :>>> ' + ln)
        ans1 = input('[?] Edit triple? y/n :>>> ')
        if ans1 == 'y':
            while True:
                ans2 = input('[!] Enter new property & object pairs, delimited by ":". Exit with "x" \n')
                # Set exit condition
                if ans2 == 'x':
                    break
                else:
                    # Perhaps another loop to confirm the write, or excessive
                    edit_text = ans2.split(':')
                    edit_pred = edit_text[0].strip()
                    edit_obj  = edit_text[1].strip()
                    write_triples(output_filename, sub + '\t' + pred_site + '/' + edit_pred 
                                  + '\t' + edit_obj + '\n')
                    print('[i] Written :> ' + ans2)
        else: 
            write_triples(output_filename, sub + '\t' + pred + '\t' + obj + '\n')
    # Done


def main():
    """ Main script operations
    return: None """
    # Open triples file
    triples = open('output-demo').readlines()

    # Setting up new file
    output_file = 'output-trans-' + time_now
    output_file2 = 'output-trans-2-' + time_now 
    
    # Output translated triples
    for ln in triples:
        ln2 = ln.strip().split('\t')  # strip out newline
        sub  = ln2[0]
        pred = ln2[1]
        pred_site = pred.split('/')[0]  # just the URL i.e. source of the prop.
        pred_prop = pred.split('/')[1]  # just the property, after URL protocol
        obj  = ln2[2]

        # Not translating EN labels from EN search services
        if 'google.com' in pred_site:
            # Write same triples for now
            triple_same = sub + '\t' + pred + '\t' + obj + '\n'
            write_triples(output_file, triple_same)
        # Machine translating other sources of data
        if 'naver.com' in pred_site:
            pred_prop_trans = translate_text(pred_prop, 'ko', 'en')
            obj_trans = translate_text(obj, 'ko', 'en')
            triple_trans = sub + '\t' + pred_site + '/' + pred_prop_trans + '\t' + obj_trans + '\n'
            write_triples(output_file, triple_trans)
        if 'yandex.ru' in pred_site:
            pred_prop_trans = translate_text(pred_prop, 'ru', 'en')
            obj_trans = translate_text(obj, 'ru', 'en')
            triple_trans = sub + '\t' + pred_site + '/' + pred_prop_trans + '\t' + obj_trans + '\n'
            write_triples(output_file, triple_trans)
        if 'baidu.com' in pred_site:
            pred_prop_trans = translate_text(pred_prop, 'zh', 'en')
            obj_trans = translate_text(obj, 'zh', 'en')
            triple_trans = sub + '\t' + pred_site + '/' + pred_prop_trans + '\t' + obj_trans + '\n'
            write_triples(output_file, triple_trans)
    """ """
    # Start interactive CLI to reconcile triples
    recon_triples_CLI(output_file, output_file2)
    # Using the demo data:
    # recon_triples_CLI('output-demo-trans-1', 'output-demo-trans-2')



if __name__ == "__main__":
    main()
