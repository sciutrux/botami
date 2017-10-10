#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# Read configuration file
import json
from collections import namedtuple

with open("configuration.json") as json_file:
        config_data = json.load(json_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

bot_name = config_data.botName
database = config_data.database
read_only = False
if config_data.readOnly: read_only = True

# Uncomment the following lines to enable verbose logging
import logging
logging.basicConfig(level=logging.ERROR)

# Setup chatbot
bot = ChatBot(
    bot_name,
    storage_adapter='chatterbot.storage.'+config_data.storageAdapter,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': config_data.specificResponseAdapter.input_text,
            'output_text': config_data.specificResponseAdapter.output_text
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': config_data.lowConfidenceAdapter.threshold,
            'default_response': config_data.lowConfidenceAdapter.default_response
        }
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    database=database,
    read_only=read_only
)

trainer = config_data.trainer

# Train chatbot with list, corpus or none
if trainer == 'list':

    conversation = [
        'Hi!',
        'Hello!',
        'How are you?',
        'I\'m fine, thank you',
        'Nice to meet you.',
        'Thank you.',
        'See you soon!'
    ]
    bot.set_trainer(ListTrainer)
    bot.train(conversation)

elif trainer == 'corpus':

    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train(
        # 'chatterbot.corpus.english.greetings',
        # 'chatterbot.corpus.english.conversations'
        'chatterbot.corpus.english'
    )

name = input(bot_name + ': ' + config_data.nameInquiry + ' ')
print(bot_name + ': ' + config_data.initialGreeting)

while True:
    try:
        sentence = input(name + ': ')
        response = bot.get_response(sentence)
        print(bot_name + ': ' + response.text)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
