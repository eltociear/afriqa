"""
Script is based on this package: https://github.com/nidhaloff/deep-translator/tree/a694c92b6741fc9c3200835b64be2fd910cd761b
How to use: python translation_script/translate_queries.py --questions_file_path translation_script/test.csv --source hausa --pivot english --output_file_path translation_script/twi_translated.csv
"""

import os
import argparse
import pandas as pd
from tqdm.auto import tqdm
from deep_translator import GoogleTranslator

TARGET_LANG = {
    "bemba": "auto",
    "bem": "auto",
    "fon": "auto",
    "hausa": "ha",
    "hau": "ha",
    "igbo": "ig",
    "ibo": "ig",
    "kinyarwanda": "rw",
    "kin": "rw",
    "twi": "ak",
    "yoruba": "yo",
    "yor": "yo",
    "swahili": "sw",
    "swa": "sw",
    "wolof": "auto",
    "wol": "auto",
    "zulu": "zu",
    "zul": "zu",
}

PIVOT_LANG = {
    "english": "en",
    "french": "fr"
}

def google_translate(translation_sentence: list, source_lang: str, target_lang) -> str:
    """
    Translate a sentence from source language to target language
    :param translation_sentence: sentence to be translated
    :param source_lang: source language
    :param target_lang: target language
    :return: translated sentence
    """
    translator = GoogleTranslator(source=PIVOT_LANG[source_lang], target=TARGET_LANG[target_lang])
    result = []
    for text in translation_sentence:
        try:
            translated = translator.translate(text=text)
        except Exception as e:
            translated = text
        result.append(translated)
    
    return result



def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Translate source language to pivot language"
    )
    parser.add_argument(
        "--questions_file_path",
        type=str,
        required=True,
        help="File path to the file containing the source language data",
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="original language of the data to be translated",
        choices=TARGET_LANG.keys(),
    )
    parser.add_argument(
        "--pivot",
        type=str,
        required=True,
        default="english",
        help="language in which to make translation to",
        choices=PIVOT_LANG.keys(),
    )
    parser.add_argument(
        "--output_file_path",
        type=str,
        required=True,
        help="path to store the translated file",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    assert os.path.exists(
        args.questions_file_path
    ), f"The input annotation file: '{args.input_annotation_file}' does not exist"

    if args.questions_file_path.endswith("csv"):
        lang_df = pd.read_csv(args.questions_file_path, sep=",", header=0, dtype=object)
    elif args.questions_file_path.endswith("tsv"):
        lang_df = pd.read_csv(args.questions_file_path, sep="\t", header=0, dtype=object)
    questions = lang_df["Original question in African language"].to_list()
    progress_bar = tqdm(range(len(questions)))

    print("Starting Transalation ...")
    for i, text in enumerate(questions):
        translated = GoogleTranslator(source=TARGET_LANG[args.source], target=PIVOT_LANG[args.pivot]).translate(
            text=text
        )
        lang_df.loc[i, "Translated Question in English"] = translated
        progress_bar.update(1)

    if args.output_file_path.endswith("tsv"):
        print("saving to file ")
        print(args.output_file_path)
        lang_df.to_csv(args.output_file_path, sep="\t", index=False)
    elif args.output_file_path.endswith("csv"):
        print("saving to file ")
        print(args.output_file_path)
        lang_df.to_csv(args.output_file_path, index=False)
    print("Translation Completed")


if __name__ == "__main__":
    main()
