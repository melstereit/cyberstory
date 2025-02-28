#!/usr/bin/env python3

import configparser
import os
import sys

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain_openai import OpenAI
from openai import RateLimitError

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Konfigurationsdatei
CONFIG_FILE = 'config.ini'

def get_llm(llm_choice):
    if llm_choice == "openai":
        return OpenAI(temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))
    elif llm_choice == "huggingface":
        return HuggingFaceHub(repo_id="google/flan-t5-xxl", huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
    else:
        raise ValueError(f"Unbekanntes LLM: {llm_choice}")

def get_ai_greeting(name, llm_choice):
    try:
        llm = get_llm(llm_choice)

        prompt = PromptTemplate(
            input_variables=["name"],
            template="Generiere eine kreative und freundliche Begrüßung für {name}."
        )

        response = llm.invoke(prompt.format(name=name))
        return response.strip()

    except RateLimitError:
        return f"Entschuldigung, {name}. Das API-Kontingent für {llm_choice} ist derzeit aufgebraucht. Bitte versuchen Sie es später erneut oder wählen Sie ein anderes LLM."

    except Exception as e:
        return f"Es tut uns leid, {name}. Ein unerwarteter Fehler ist aufgetreten: {str(e)}"

def get_or_set_llm_choice():
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'LLM' in config and 'choice' in config['LLM']:
            llm_choice = config['LLM']['choice']
            print(f"Verwende gespeichertes LLM: {llm_choice}")
            return llm_choice

    llm_choice = input("Welches LLM möchten Sie verwenden? (openai/huggingface): ").lower()
    while llm_choice not in ["openai", "huggingface"]:
        print("Ungültige Auswahl. Bitte wählen Sie 'openai' oder 'huggingface'.")
        llm_choice = input("Welches LLM möchten Sie verwenden? (openai/huggingface): ").lower()

    # Speichern der Auswahl in der config.ini Datei
    config['LLM'] = {'choice': llm_choice}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    print(f"LLM-Auswahl '{llm_choice}' wurde in {CONFIG_FILE} gespeichert.")

    return llm_choice

def main():
    try:
        llm_choice = get_or_set_llm_choice()

        if len(sys.argv) > 1:
            name = " ".join(sys.argv[1:])
        else:
            name = input("Bitte geben Sie Ihren Namen ein: ")

        greeting = get_ai_greeting(name, llm_choice)
        print(greeting)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()