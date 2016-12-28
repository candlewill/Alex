#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is PEP8-compliant. See http://www.python.org/dev/peps/pep-0008/.

"""
This is an example implementation of a dummy yet funny dialogue policy.
"""

from dm.base import DialoguePolicy
from slu.da import DialogueAct, DialogueActItem
from out.time_zone import GoogleTimeFinder

from datetime import datetime

print("dummypolicy Starting....")

print(DialoguePolicy)


class DummyDialoguePolicy(DialoguePolicy):
    """
    This is a trivial policy just to demonstrate basic functionality of
    a proper DM.
    """

    def __init__(self, cfg, ontology):
        super(DummyDialoguePolicy, self).__init__(cfg, ontology)

        self.das = []  # 用户对话行为列表
        self.last_system_dialogue_act = None
        self.time = GoogleTimeFinder()

    def gather_time_info(self, ds, accepted_slots):
        """Handles if in_city specified it handles properly filled in_state slot. If needed, a Request DA is formed for missing in_state slot.

        Returns Reqest DA and in_state
        If the request DA is empty, the search for current_time may be commenced immediately.

        :param ds: The current dialogue state,
        """
        req_da = DialogueAct()

        in_state_val = ds['in_state'].mpv() if 'in_state' in accepted_slots else 'none'
        in_city_val = ds['in_city'].mpv() if 'in_city' in accepted_slots else 'none'

        if in_city_val != 'none' and in_state_val == 'none':
            in_states = self.ontology.get_compatible_vals('city_state', in_city_val)
            if not in_states or not len(in_states):
                print("WARNING: there is no state compatible with this city: " + in_city_val)
            elif len(in_states) == 1:
                in_state_val = in_states.pop()

        if in_city_val == 'none' and in_state_val == 'none':
            in_state_val = self.ontology.get_default_value('in_state')
            in_city_val = self.ontology.get_default_value('in_city')

        if in_state_val == 'none':
            req_da = DialogueAct("request(in_state)")  # we don't know which state to choose

        lon = None
        lat = None
        if in_city_val != 'none' and in_state_val != 'none' and in_state_val in self.ontology['addinfo']['state']:
            cities = self.ontology['addinfo']['state'][in_state_val]
            if cities and in_city_val in cities:
                lat = cities[in_city_val]['lat']
                lon = cities[in_city_val]['lon']

        return req_da, in_city_val, in_state_val, lon, lat

    def check_city_state_conflict(self, in_city, in_state):
        """Check for conflicts in the given city and state. Return an apology() DA if the state and city is incompatible.

        :param in_city: city slot value
        :param in_state: state slot value
        :rtype: DialogueAct
        :return: apology dialogue act in case of conflict, or None
        """

        if not self.ontology.is_compatible('city_state', in_city, in_state):
            apology_da = DialogueAct('apology()&inform(cities_conflict="incompatible")')
            apology_da.extend(DialogueAct('inform(in_city="%s")&inform(in_state="%s")' % (in_city, in_state)))
            return apology_da
        return None

    def get_current_time(self, in_city, in_state, longitude, latitude):

        place = in_city + "," + in_state if in_city != 'none' else in_state
        if longitude and latitude:
            cur_time, time_zone = self.time.get_time(place=place, lat=latitude, lon=longitude)
        else:
            cur_time, time_zone = self.time.get_time(place=place)
        if cur_time is None:
            default_time = datetime.now()
            default_state = self.ontology.get_default_value('in_state')
            d_time = default_time.strftime("%I:%M:%p")
            if in_state is not default_state:
                return DialogueAct('apology()&inform(in_state="%s")&inform(current_time=%s)&iconfirm(in_state=%s)' % (
                    in_state, d_time, default_state))
            else:
                return DialogueAct('inform(current_time=%s)&iconfirm(in_state="%s")' % (d_time, default_state))

        res_da = DialogueAct()
        res_da.append(DialogueActItem('iconfirm', 'in_state', in_state))
        res_da.append(DialogueActItem('inform', 'current_time', cur_time.strftime("%I:%M:%p")))
        res_da.append(DialogueActItem('inform', 'time_zone', time_zone))

        return res_da

    def get_current_time_res_da(self, ds, accepted_slots, state_changed):
        """Generates a dialogue act informing about the current time.
        :rtype: DialogueAct
        """

        req_da, in_city, in_state, lon, lat = self.gather_time_info(ds, accepted_slots)

        if len(req_da):
            return req_da

        # check for valid input
        if in_city != 'none':
            apology_da = self.check_city_state_conflict(in_city, in_state)
            if apology_da is not None:
                return apology_da

        # if state_changed:
        res_da = self.get_current_time(in_city, in_state, lon, lat)
        # else:
        #     res_da = self.backoff_action(ds)
        return res_da

    def get_da(self, dialogue_state):

        # These facts are used in the dialog-controlling conditions that follow.
        # They are named so that the dialog-controlling code is more readable.o
        ludait_prob, last_user_dai_type = dialogue_state["ludait"].mph()  # 无论用户说什么都先更新ludait槽位
        if ludait_prob < 1e-7:
            last_user_dai_type = 'none'

        # all slots being requested by the user
        slots_being_requested = dialogue_state.get_slots_being_requested(0.5)
        # all slots being confirmed by the user
        slots_being_confirmed = dialogue_state.get_slots_being_confirmed(0.5)
        # all slots supplied by the user but not implicitly confirmed
        noninformed_slots = dialogue_state.get_slots_being_noninformed(0.5)
        # all slots deemed to be accepted
        accepted_slots = dialogue_state.get_accepted_slots(0.5)
        # all slots that should be confirmed
        slots_tobe_confirmed = dialogue_state.get_slots_tobe_confirmed(0.5, 0.5)
        #  filter out all the slots that are not defined by the ontology to be confirmed
        slots_tobe_confirmed = {k: v for k, v in slots_tobe_confirmed.items() if
                                k in self.ontology.slots_system_confirms()}
        # all slots for which the policy can use ``select`` DAI
        slots_tobe_selected = dialogue_state.get_slots_tobe_selected(0.5)
        #  filter out all the slots that are not defined by the ontology to be selected
        slots_tobe_selected = {k: v for k, v in slots_tobe_selected.items() if
                               k in self.ontology.slots_system_selects()}
        # all slots changed by a user in the last turn
        changed_slots = dialogue_state.get_changed_slots(0.5)
        # did the state changed at all?
        has_state_changed = dialogue_state.has_state_changed(0.5)

        fact = {
            'max_turns_exceeded': dialogue_state.turn_number > 10,
            'dialog_begins': len(self.das) == 0,
            'user_did_not_say_anything': last_user_dai_type == "silence",
            'user_said_bye': "lta_bye" in accepted_slots,
            'we_did_not_understand': last_user_dai_type == "null" or last_user_dai_type == "other",
            'user_wants_help': last_user_dai_type == "help",
            'user_thanked': last_user_dai_type == "thankyou",
            'user_wants_restart': last_user_dai_type == "restart",
            'user_wants_us_to_repeat': last_user_dai_type == "repeat",
            'there_is_something_to_be_selected': bool(slots_tobe_selected),
            'there_is_something_to_be_confirmed': bool(slots_tobe_confirmed),
            'user_wants_to_know_the_time': 'current_time' in
                                           slots_being_requested,
            'user_wants_to_know_the_weather': dialogue_state[
                'lta_task'].test('weather', 0.5),
            'user_wants_to_find_the_platform': dialogue_state[
                'lta_task'].test('find_platform', 0.5),
        }

        # topic-independent behavior
        if fact['max_turns_exceeded']:
            # Hang up if the talk has been too long
            res_da = DialogueAct('bye()&inform(toolong="true")')

        elif fact['dialog_begins']:
            # NLG("Dobrý den. Jak Vám mohu pomoci")
            res_da = DialogueAct("hello()")

        elif fact['user_did_not_say_anything']:
            # at this moment the silence and the explicit null act
            # are treated the same way: NLG("")
            silence_time = dialogue_state['silence_time']

            if silence_time > self.cfg['DM']['basic']['silence_timeout']:
                res_da = DialogueAct('inform(silence_timeout="true")')
            else:
                res_da = DialogueAct("silence()")
            dialogue_state["ludait"].reset()

        elif fact['user_said_bye']:
            # NLG("Na shledanou.")
            res_da = DialogueAct("bye()")
            dialogue_state["ludait"].reset()
            dialogue_state["lta_bye"].reset()

        elif fact['we_did_not_understand']:
            # NLG("Sorry, I did not understand. You can say...")
            res_da = DialogueAct("notunderstood()")
            dialogue_state["ludait"].reset()

        elif fact['user_wants_help']:
            # NLG("Help.") based on context
            res_da = DialogueAct("help(%s)")
            # res_da = DialogueAct("help()")
            dialogue_state["ludait"].reset()

        elif fact['user_thanked']:
            # NLG("Díky.")
            if not changed_slots:  # plain thank you, nothing else said
                dialogue_state.restart()
            res_da = DialogueAct('inform(cordiality="true")&hello()')
            dialogue_state["ludait"].reset()

        elif fact['user_wants_restart']:
            # NLG("Dobře, zančneme znovu. Jak Vám mohu pomoci?")
            dialogue_state.restart()
            res_da = DialogueAct("restart()&hello()")
            dialogue_state["ludait"].reset()

        elif fact['user_wants_us_to_repeat']:
            # NLG - use the last dialogue act
            res_da = DialogueAct("irepeat()")
            dialogue_state["ludait"].reset()

        # .....

        elif fact['user_wants_to_know_the_time']:
            # Respond to questions about current time
            # TODO: allow combining with other questions?
            res_da = self.get_current_time_res_da(dialogue_state, accepted_slots, has_state_changed)

        # topic-dependent
        elif fact["user_wants_to_know_the_weather"]:
            # implicitly confirm all changed slots
            pass

        else:
            # NLG("Can I help you with anything else?")
            res_da = DialogueAct("reqmore()")
            dialogue_state.slots["ludait"].reset()

        self.last_system_dialogue_act = res_da

        # record the system dialogue acts
        self.das.append(self.last_system_dialogue_act)
        return self.last_system_dialogue_act
