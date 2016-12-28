#!/usr/bin/env python
# vim: set fileencoding=UTF-8 filetype=python :
#
#  When the configuration file is loaded, several automatic transformations
#  are applied:
#
# 1) '{cfg_abs_path}' as a substring of atomic attributes is replaced by
#    an absolute path of the configuration files.  This can be used to
#    make the configuration file independent of the location of programs
#    using the configuration file.
#
# or better use the as_project_path function

from dm.dddstate import DeterministicDiscriminativeDialogueState
from dm.dummypolicy import DummyDialoguePolicy
from utils.config import as_project_path

config = {
    'DM': {
        'debug': True,
        'input_timeout': 3.0,  # in seconds
        'type': 'basic',
        'epilogue': {
            # if set to None, no question is asked
            'final_question': None,
            # if set to None, no code is given
            # if set to a valid url, a code is given and reported to the url as
            # "url.format(code=code)"
            'final_code_url': None,
            # minimum turn count that must be reached for the code giveaway
            'final_code_min_turn_count': 0,
            'final_code_text_min_turn_count_not_reached': None,
            # the message is generated as "final_code_text.format(code=code)"
            'final_code_text': None,
            'final_code_text_repeat': None,
            # initialise the seed of the code generation algorithm
            'code_seed': 1,
        },
        'basic': {
            'debug': True,
            'silence_timeout': 10.0,  # in seconds
        },
        'ontology': as_project_path('resources/ontology.py'),
        'dialogue_state': {
            'type': DeterministicDiscriminativeDialogueState,
        },
        'dialogue_policy': {
            'type': DummyDialoguePolicy,
        },
        'DeterministicDiscriminativeDialogueState': {
            'type': 'MDP',  # 'UFAL_DSTC_1.0_approx',
        },
    },
    'Hub': {
        'history_file': 'hub_history_shub.txt',
        'history_length': 1000,
    }
}
